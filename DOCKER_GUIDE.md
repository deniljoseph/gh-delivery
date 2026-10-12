# Geometry Home Delivery Management – Docker Deployment Guide

## What was changed in the project

| File | Change |
|---|---|
| `app.py` | One line: the secure-cookie / proxy setting can also be switched on with `BEHIND_HTTPS_PROXY=1` (needed only when you serve the app over HTTPS behind a reverse proxy). Default behaviour unchanged. |
| `Dockerfile` | **New.** Python 3.12-slim, gunicorn (2 workers, same command as Railway), non-root user, `/health` healthcheck, timezone `Asia/Dubai`. |
| `docker-compose.yml` | **New.** App + PostgreSQL 16 (recommended). Two volumes: `pgdata` (database) and `appdata` (uploads, PDF archive, backups). |
| `docker-compose.sqlite.yml` | **New.** Single container, SQLite + files in one volume. |
| `.dockerignore`, `.env.docker.example` | **New.** |

The app already supported `DATA_DIR`, `DATABASE_URL`, `SECRET_KEY` and `ADMIN_PASSWORD`, so almost nothing else had to change. On first start it copies the bundled logos, signature and company stamps into the data volume.

## 1. Prerequisites
- Docker Engine 24+ with the Compose plugin (`docker compose version`), or Docker Desktop on Windows/Mac
- Port 5000 free (or set `APP_PORT`)

## 2. Configure
```bash
cd gh-delivery
cp .env.docker.example .env
```
Edit `.env`:
- `SECRET_KEY` – `openssl rand -hex 32` (without it everyone is logged out on every restart)
- `POSTGRES_PASSWORD` – `openssl rand -hex 16`
- `ADMIN_PASSWORD` – password for the first `admin` user (only read when the database is empty; if blank it is `admin123`)
- `BEHIND_HTTPS_PROXY` – keep `0` for plain http on a LAN; set `1` only when users access it via HTTPS through a reverse proxy

## 3A. Deploy with PostgreSQL (recommended)
```bash
docker compose up -d --build
docker compose ps
docker compose logs -f app
```
Open **http://SERVER_IP:5000**. Tables and the three companies (GHM, GHT, TRA) are created automatically.

## 3B. Deploy with SQLite (simple)
```bash
docker compose -f docker-compose.sqlite.yml up -d --build
```
Use only one of 3A/3B (same port).

## 4. First login
Log in as `admin` with your `ADMIN_PASSWORD` (or `admin123`). Change the password straight away, then check Settings → Companies, Signatories and Users.

Drivers use **http://SERVER_IP:5000/driver/login** on their phones. Create each login under Drivers → Create login.

## 5. Moving data from another install (e.g. the Railway or local one)
The app's own backup/restore works between SQLite and PostgreSQL:
1. On the old system, log in as admin and download the backup (`/backup/zip` – full ZIP with database + files).
2. On the new system, open **/restore** (admin) and upload that file.

## 6. Daily operations
```bash
docker compose logs -f app       # logs
docker compose restart app       # restart
docker compose down              # stop, keep data
docker compose down -v           # stop AND DELETE ALL DATA
docker compose up -d --build     # update after code changes
```

## 7. Backups
- In the app (admin): download the full ZIP backup regularly and keep copies off the server.
- Database dump (PostgreSQL mode):
```bash
docker compose exec -T db pg_dump -U delivery delivery > backup_$(date +%F).sql
cat backup_2026-10-10.sql | docker compose exec -T db psql -U delivery delivery   # restore
```
- Files volume (uploads, archived PDFs):
```bash
docker run --rm -v gh-delivery_appdata:/data -v "$PWD":/out alpine tar czf /out/appdata_$(date +%F).tgz -C /data .
```
(Volume name is `<folder>_appdata`; see `docker volume ls`.)

## 8. HTTPS / internet access
Put a reverse proxy in front (Caddy example):
```
delivery.yourdomain.com {
    reverse_proxy localhost:5000
}
```
Then set `BEHIND_HTTPS_PROXY=1` in `.env`, change the port mapping to `"127.0.0.1:5000:5000"`, and run `docker compose up -d`. Do not set `BEHIND_HTTPS_PROXY=1` on plain http – logins would fail because the cookie is marked secure.

## 9. Troubleshooting
| Symptom | Fix |
|---|---|
| `set SECRET_KEY in .env` | `.env` missing or empty |
| Can't log in after enabling HTTPS flag | You are on plain http; set `BEHIND_HTTPS_PROXY=0` |
| Logos/stamps missing in PDFs | Make sure the `appdata` volume is mounted (use the provided compose files) |
| App restarting | `docker compose logs app`; usually wrong DB password (stored in `pgdata` from first start) |
| Port in use | set `APP_PORT=8080` in `.env` |
| Large restore fails | Upload limit is 512 MB; behind a proxy raise its body-size limit too |
