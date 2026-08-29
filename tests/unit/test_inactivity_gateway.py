from pathlib import Path

ROOT = Path(__file__).parents[2]


def test_gateway_closes_streamlit_after_ten_inactive_minutes() -> None:
    shell = (ROOT / "gateway/static/index.html").read_text(encoding="utf-8")

    assert "10 * 60 * 1000" in shell
    assert 'frame.src = "about:blank"' in shell
    assert 'frame.src = "/app/"' in shell
    assert "visibilitychange" in shell
    assert "sessionStorage" in shell
    assert "localStorage" not in shell
    assert "SameSite=Strict; Max-Age=60" in shell


def test_nginx_proxies_streamlit_http_websocket_and_health_routes() -> None:
    config = (ROOT / "gateway/nginx.conf.template").read_text(encoding="utf-8")

    assert "listen __PORT__;" in config
    assert "location /app/" in config
    assert "proxy_set_header Upgrade $http_upgrade;" in config
    assert "proxy_set_header Connection $connection_upgrade;" in config
    assert "location = /_stcore/health" in config
    assert "access_log off;" in config
    assert "access_log /dev/stdout;" not in config


def test_container_uses_gateway_process_supervisor() -> None:
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")

    assert "apt-get install --no-install-recommends --yes nginx" in dockerfile
    assert 'CMD ["python", "gateway/run.py"]' in dockerfile


def test_gateway_waits_for_streamlit_before_opening_public_port() -> None:
    supervisor = (ROOT / "gateway/run.py").read_text(encoding="utf-8")

    readiness_call = supervisor.index("_wait_for_streamlit(streamlit)")
    nginx_start = supervisor.index("nginx = subprocess.Popen")

    assert "http://127.0.0.1:8501/app/_stcore/health" in supervisor
    assert readiness_call < nginx_start
