FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PITZER_PROJECT_ROOT=/app \
    PORT=8080 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

# Nginx serves the inactivity-aware shell and proxies the Streamlit WebSocket. It runs inside
# the same Cloud Run container and does not create another service or billable resource.
RUN apt-get update \
    && apt-get install --no-install-recommends --yes nginx \
    && rm -rf /var/lib/apt/lists/*

# Install an immutable application wheel, then run both processes as an unprivileged user. The
# explicit project root keeps repository-owned runtime data discoverable after installation.
RUN useradd --create-home --uid 10001 appuser

COPY --chown=appuser:appuser pyproject.toml README.md LICENSE ./
COPY --chown=appuser:appuser src ./src
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir .

COPY --chown=appuser:appuser streamlit_app.py ./
COPY --chown=appuser:appuser .streamlit ./.streamlit
COPY --chown=appuser:appuser assets ./assets
COPY --chown=appuser:appuser data ./data
COPY --chown=appuser:appuser gateway ./gateway

USER appuser

EXPOSE 8080

# The supervisor renders Cloud Run's injected PORT into Nginx, starts Streamlit privately on
# port 8501, and forwards termination signals to both processes.
CMD ["python", "gateway/run.py"]
