# Free hosting on PythonAnywhere (no credit card) – Delivery app

Free "Beginner" account: 1 web app at `https://YOURUSER.pythonanywhere.com`, 512 MB disk, files persist, HTTPS included.
Limits to know: no SSH, no scheduled/always-on tasks, 1 web worker, and you must click the "Run until ..." button on the Web tab
before the free app expires (monthly; check the date shown on the Web tab). Limits can change - see pythonanywhere.com/pricing.

## 1. Sign up
pythonanywhere.com -> Pricing & signup -> **Create a Beginner account** (no card). Your username becomes part of the URL.

## 2. Upload the project
1. Files tab -> upload `gh-delivery-docker.zip` into `/home/YOURUSER/`.
2. Open a **Bash console** (Consoles tab) and run:
```bash
cd ~
unzip -q gh-delivery-docker.zip
rm gh-delivery-docker.zip
mkdir -p ~/gh-data
```
You now have `/home/YOURUSER/gh-delivery`.

## 3. Create the Python environment
Still in the Bash console:
```bash
mkvirtualenv --python=python3.12 ghenv
pip install -r ~/gh-delivery/requirements_pythonanywhere.txt
```
(If `python3.12` is not offered, use the newest version available, 3.11 or later.)
Check disk use with `du -sh ~` (limit 512 MB).

## 4. Create the web app
1. Web tab -> **Add a new web app** -> Next -> **Manual configuration** -> pick the same Python version.
2. On the Web tab set **Virtualenv** to `/home/YOURUSER/.virtualenvs/ghenv`.
3. Click the **WSGI configuration file** link, delete everything inside, paste the contents of `pa_wsgi.py`
   (from the project folder), edit YOURUSER, SECRET_KEY and ADMIN_PASSWORD, and Save.
4. (Optional, faster) Static files: URL `/static/` -> directory `/home/YOURUSER/gh-delivery/static`.
5. Click the green **Reload** button.

Open `https://YOURUSER.pythonanywhere.com` and log in as `admin` with your ADMIN_PASSWORD.
Drivers: `https://YOURUSER.pythonanywhere.com/driver/login`.

## 5. Move existing data
Download the full ZIP backup from the old install (`/backup/zip`), then open `/restore` on the new site and upload it.
If the file is large, check it stays within the free 512 MB disk.

## 6. Updating later
Upload changed files (Files tab) into `/home/YOURUSER/gh-delivery/` (same folders), then press **Reload** on the Web tab.

## 7. Keep it alive
- Press **Run until ...** on the Web tab before the expiry date (set a phone reminder).
- Download a ZIP backup from the app weekly; the PDF archive grows over time, so watch the 512 MB disk.

## 8. Troubleshooting
| Problem | Fix |
|---|---|
| Error page | Web tab -> **Error log** link |
| `No module named ...` | Virtualenv path not set, or pip install failed (re-run step 3) |
| Cannot log in | `BEHIND_HTTPS_PROXY` must be 1 on https; clear site cookies |
| Disk full | `du -sh ~/gh-data/*`; delete old archived PDFs/backups |
