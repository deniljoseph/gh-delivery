# Deploy the Delivery app on Fly.io (no Docker knowledge or Docker install needed)

Fly.io runs apps as containers internally, but you never run Docker yourself: `fly deploy` uploads the project and
builds it on Fly's servers using the `Dockerfile` already in the folder.

## 1. One-time setup (Windows PowerShell)
```powershell
iwr https://fly.io/install.ps1 -useb | iex     # installs the fly command (restart PowerShell after)
fly auth signup                                 # or: fly auth login  (a payment card is required)
```

## 2. Prepare the project
1. Extract the project, open PowerShell in the folder (the one containing `fly.toml`).
2. Edit `fly.toml`: set `app = "your-unique-name"` (letters, numbers, dashes) and `primary_region`
   (run `fly platform regions` and pick the closest to Dubai).

## 3. Create app, volume and secrets
```powershell
fly apps create your-unique-name
fly volumes create wfms_data --size 1 --region fra          # same region as primary_region
fly secrets set SECRET_KEY="<long random text>" ADMIN_PASSWORD="<strong password>"
```
The volume holds the SQLite database, uploads, archived PDFs and backups. A volume belongs to ONE machine, so run exactly one machine.

## 4. Deploy
```powershell
fly deploy --ha=false
fly status
fly logs
```
Open `https://your-unique-name.fly.dev` (or `fly open`). Log in as `admin` with your ADMIN_PASSWORD.
Drivers use `/driver/login`.

## 5. Move your existing data
On the old system download the full ZIP backup (`/backup/zip`), then on the new site open `/restore` and upload it.

## 6. Updating later
Replace the changed files, then run `fly deploy --ha=false` again. Data on the volume stays.

## 7. Backups
- Download the ZIP backup from the app regularly.
- Fly takes automatic volume snapshots (check `fly volumes snapshots list -a your-unique-name`).

## 8. Useful commands
```powershell
fly logs                     # live logs
fly ssh console              # shell inside the machine (data in /data)
fly secrets list
fly scale count 1            # make sure only ONE machine exists
fly apps destroy your-unique-name   # delete everything (careful)
```

## 9. Notes
- Fly has no Dubai region; choose the nearest. Check current pricing at fly.io/docs/about/pricing.
- Keep to one machine with SQLite. Running two machines would give each its own volume and separate data.
- Custom domain later: `fly certs add yourdomain.com`.
