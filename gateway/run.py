"""Start and supervise the Nginx gateway and internal Streamlit process."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

GATEWAY_DIR = Path(__file__).resolve().parent
NGINX_TEMPLATE = GATEWAY_DIR / "nginx.conf.template"
NGINX_CONFIG = Path("/tmp/pitzer-nginx.conf")


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
