# Deploy the Delivery Management System on Railway

Use a **new Railway project** (or at least a new Postgres database) – do not share the invoicing app's database.

## 1. Push to GitHub
Create a private repo and push this folder (`.gitignore` already excludes local databases, backups and generated PDFs).

## 2. Create the service
Railway → **New Project → Deploy from GitHub repo** → pick the repo.
`railway.json`, `nixpacks.toml` and `Procfile` configure the build, start command (gunicorn) and the `/health` check.

## 3. Add PostgreSQL
Project → **New → Database → Add PostgreSQL**. Then in your web service → **Variables** → **New Variable → Add Reference**
→ choose `DATABASE_URL` from the Postgres service. Tables and the three companies are created automatically on first start.

## 4. Add a Volume (keeps logos, signatures, stamps, the PDF archive and backups)
Web service → **Volumes** (or right-click the canvas → *Volume*) → **Add Volume** → mount path `/data`.
Railway then sets `RAILWAY_VOLUME_MOUNT_PATH` and the app uses it automatically. On first start the bundled logo,
signature and stamps are copied into the volume.
Without a volume, uploads and archived PDFs are lost on every redeploy (PDFs are regenerated on demand, but uploaded
images are not).

## 5. Variables (web service → Variables)
| Variable | Required | Notes |
|---|---|---|
| `DATABASE_URL` | yes | Reference from the Postgres service |
| `SECRET_KEY` | yes | `python -c "import secrets; print(secrets.token_hex(32))"` – without it everyone is logged out on each restart |
| `ADMIN_PASSWORD` | recommended | Password of the first `admin` user. Only read when the database is empty |
| `DATA_DIR` | no | Only if you mount the volume somewhere unusual |
| `PORT` | auto | Set by Railway |

## 6. Generate a domain
Web service → **Settings → Networking → Generate Domain**. Open it and log in as `admin`
(password = `ADMIN_PASSWORD`, or `admin123` if you did not set one – change it immediately under *Change password*).

## Driver portal
Drivers use `https://<your-domain>/driver/login` (add it to their phone's home screen). Create each driver's login under
**Drivers → Create login**. Nothing else to configure on Railway.

## After deploying
1. **Settings → Companies**: check addresses, phone numbers and the delivery note prefixes.
2. **Signatories & Stamps**: confirm the signatory (name, position, phone) and the stamp for each company.
3. **Users**: create delivery-department accounts (role *Delivery User*).
4. **Backup / Restore**: download a full ZIP backup regularly – it includes the database, images and every PDF.

## Troubleshooting
| Problem | Fix |
|---|---|
| Healthcheck fails / deploy loops | Check the deploy logs; usually `DATABASE_URL` reference missing |
| Logged out constantly | `SECRET_KEY` not set |
| Logo / stamp missing after redeploy | No volume attached (step 4) – re-upload after attaching it |
| `permission denied` writing files | Volume mounted but not writable: set variable `RAILWAY_RUN_UID=0` on the service |
| Want to start from your invoicing data | Not applicable – separate app. Use Backup / Restore only between delivery-note instances |

## Local development
```
pip install -r requirements_local.txt
python app.py          # SQLite, http://localhost:5000
```
