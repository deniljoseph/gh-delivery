FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=Asia/Dubai

RUN apt-get update && apt-get install -y --no-install-recommends tzdata curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py db.py ./
COPY static ./static
COPY templates ./templates

# Non-root user. /data holds uploads, PDF archive, backups (and the SQLite file in SQLite mode)
RUN useradd -m appuser && mkdir -p /data && chown -R appuser /app /data
USER appuser

ENV PORT=5000 \
    DATA_DIR=/data
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD curl -fs http://localhost:${PORT}/health || exit 1

CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT} --workers 2 --timeout 120 --preload --access-logfile -"]
