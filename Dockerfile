FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PITZER_PROJECT_ROOT=/app \
    PORT=8080 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

# Install an immutable application wheel, then run it as an unprivileged user. The explicit
# project root above keeps repository-owned runtime data discoverable after installation.
RUN useradd --create-home --uid 10001 appuser

COPY --chown=appuser:appuser pyproject.toml README.md LICENSE ./
COPY --chown=appuser:appuser src ./src
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir .

COPY --chown=appuser:appuser streamlit_app.py ./
COPY --chown=appuser:appuser .streamlit ./.streamlit
COPY --chown=appuser:appuser assets ./assets
COPY --chown=appuser:appuser data ./data

USER appuser

EXPOSE 8080

# Cloud Run injects PORT. The shell form is intentional so the variable is expanded at
# container start, while exec preserves correct signal handling for graceful shutdown.
CMD ["sh", "-c", "exec streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=${PORT:-8080} --server.headless=true --server.fileWatcherType=none --browser.gatherUsageStats=false"]
