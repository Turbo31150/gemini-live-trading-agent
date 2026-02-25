# Gemini Live Trading Agent — Cloud Run Dockerfile
# Multi-stage build: lightweight Python runtime

FROM python:3.12-slim AS runtime

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY public/ ./public/

# Cloud Run sets PORT env var
ENV PORT=8080
ENV HOST=0.0.0.0
ENV DEV_MODE=false

EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/health')" || exit 1

# Run with uvicorn
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--ws-max-size", "16777216"]
