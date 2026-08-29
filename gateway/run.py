"""Start and supervise the Nginx gateway and internal Streamlit process."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

GATEWAY_DIR = Path(__file__).resolve().parent
NGINX_TEMPLATE = GATEWAY_DIR / "nginx.conf.template"
NGINX_CONFIG = Path("/tmp/pitzer-nginx.conf")
STREAMLIT_HEALTH_URL = "http://127.0.0.1:8501/app/_stcore/health"
STREAMLIT_STARTUP_TIMEOUT_SECONDS = 60.0


def _write_nginx_config(port: int) -> None:
    """Render the Cloud Run port into the otherwise immutable Nginx configuration."""

    template = NGINX_TEMPLATE.read_text(encoding="utf-8")
    NGINX_CONFIG.write_text(template.replace("__PORT__", str(port)), encoding="utf-8")


def _terminate(processes: tuple[subprocess.Popen[bytes], ...]) -> None:
    """Forward container termination to both child processes and wait briefly."""

    for process in processes:
        if process.poll() is None:
            process.terminate()
    deadline = time.monotonic() + 8
    for process in processes:
        remaining = max(0.0, deadline - time.monotonic())
        try:
            process.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            process.kill()


def _wait_for_streamlit(
    process: subprocess.Popen[bytes],
    timeout: float = STREAMLIT_STARTUP_TIMEOUT_SECONDS,
) -> None:
    """Wait for Streamlit before opening the public Nginx port.

    Cloud Run considers the container ready as soon as something accepts connections on
    ``PORT``. Starting Nginx first can therefore send cold-start traffic to Streamlit before
    its private listener exists. Keeping Nginx stopped until this health check succeeds makes
    Cloud Run's startup probe the single readiness gate for both processes.
    """

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        return_code = process.poll()
        if return_code is not None:
            raise RuntimeError(f"Streamlit exited during startup with code {return_code}.")

        try:
            with urlopen(STREAMLIT_HEALTH_URL, timeout=0.5) as response:  # noqa: S310
                if response.status == 200:
                    return
        except (TimeoutError, URLError):
            time.sleep(0.1)

    raise TimeoutError(f"Streamlit did not become healthy within {timeout:g} seconds.")


def main() -> int:
    """Run both services until either exits, then stop the complete container cleanly."""

    port = int(os.environ.get("PORT", "8080"))
    _write_nginx_config(port)

    streamlit = subprocess.Popen(
        [
            "streamlit",
            "run",
            "streamlit_app.py",
            "--server.address=127.0.0.1",
            "--server.port=8501",
            "--server.baseUrlPath=app",
            "--server.headless=true",
            "--server.fileWatcherType=none",
            "--browser.gatherUsageStats=false",
        ]
    )

    try:
        _wait_for_streamlit(streamlit)
    except Exception:
        _terminate((streamlit,))
        raise

    nginx = subprocess.Popen(
        ["nginx", "-c", str(NGINX_CONFIG), "-g", "daemon off;"]
    )
    processes = (streamlit, nginx)

    stopping = False

    def stop_children(_signum: int, _frame: object) -> None:
        nonlocal stopping
        if not stopping:
            stopping = True
            _terminate(processes)

    signal.signal(signal.SIGTERM, stop_children)
    signal.signal(signal.SIGINT, stop_children)

    try:
        while all(process.poll() is None for process in processes):
            time.sleep(0.25)
    finally:
        _terminate(processes)

    for process in processes:
        if process.returncode:
            return process.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
