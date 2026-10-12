# Geometry Home – Delivery Management System

Delivery & pickup management companion to the GH invoicing system. Same stack (Flask, SQLite locally / PostgreSQL on Railway,
ReportLab PDFs), same look, same company / client / signatory / stamp / user setup.

## Run locally (Windows)
1. Install Python 3.10+ (tick "Add to PATH").
2. Double-click `START.bat` → http://localhost:5000
3. Login `admin` / `admin123` → change the password straight away.

Manual: `pip install -r requirements_local.txt` then `python app.py`.

## Deploy (Railway)
See **RAILWAY_DEPLOY.md** (Postgres + Volume + 3 variables).

## What's new in the Delivery Management System
* **Dispatch Board (Delivery Notes page)** – jobs are split into a section per driver (plus *Unassigned*), grouped by day.
  Office staff set the day's **priority** by dragging a job by its handle (or with the ▲▼ buttons). Drop a job into another
  driver's list to **reassign** it. Order saves instantly and is exactly what the driver sees (stop 1, 2, 3 …). The old table is
  one click away (*Table* button).
* **Pickups** – *New → Pickup* (or the Delivery / Pickup switch on the form). A pickup has a **Collect from** (name, phone, address,
  map link) and a **Deliver to** address. Own number series `GHM-PU-2026-0001`, own PDF (“Pickup & Delivery Note”).
  In the driver portal pickups have their own **Pickups** tab: *Mark as collected* first (handed-over-by + remarks), then the drop-off
  step unlocks and the driver marks it delivered. The office sees when it was collected and when it was delivered.
* **Driver portal sort & filter by date** – chips for Today / Tomorrow / Next 7 days / All dates, a custom from–to range, and sorting by
  Priority (office order), earliest date or latest date. The *Done* tab filters by delivered date.
* **Auto-saved, editable clients** – client details (name, phone, invoice address, shipping address, Google Map location) save
  **as you type**: change any of those fields on a delivery/pickup note and the client record is created or updated straight away
  ("✓ saved to Clients"). Saving the note also updates it. Details you change replace the saved ones; fields left blank never erase
  saved data. Typing a different name creates a new client rather than renaming the selected one. Everything is editable on the
  **Clients** page (now with shipping address and map link, and open to office staff; only admins can archive). The party you collect
  a pickup from is saved the same way. A driver typed into a note is saved automatically. Saved names auto-fill the rest of the form.
* **Delivered date & time for the office** – every place a delivered job is shown (board, table, note page, dashboard) shows the
  delivery date **and time**, who marked it and who received it. When marking delivered from the office you can set the time.
* **9 colour themes** (Classic, Ocean, Forest, Royal, Sunset, Crimson, Teal, Gold, Slate) × light/dark. Palette button in the top bar
  (office), the driver portal and the login pages. Remembered per device.

## What it does
* Delivery notes numbered per company: `GHM-DN-2026-0001`, `GHT-DN-2026-0001`, `TRA-DN-2026-0001`
  (prefix editable under Settings → Companies).
* Layout follows the ALAYA VILLA sample: Invoice No / Order No / Project / Date, Mr/Ms / Tel / Location,
  invoice + shipping address, description of goods (SL#, item, qty, unit), vehicle + driver, four signature boxes,
  notes & terms, receiver Name/Tel/Date, "Thanks & Regards" with signatory, signature and company stamp.
* **Show prices & VAT** switch per note: when on, the PDF adds AMOUNT / TOTAL AMOUNT columns, Total, VAT %, Net payable
  and amount in words (calculated by the system – nothing to protect in a spreadsheet formula).
* Paste items straight from Excel (Item | Qty | Unit).
* Saved drivers (name, contact, vehicle) – pick one and the three fields fill in.
* Delivery status: Pending / Delivered (date + received by) / Cancelled; dashboard lists notes pending 3+ days.
* Duplicate a note, edit it, delete it (soft delete – numbers are never reused).
* Every PDF is archived in `Delivery Notes Archive/<year>/`.
* Full ZIP backup / restore, audit log.

## Driver portal (separate login for each driver)
* Drivers page → **Create login** for a driver (username + password). The driver signs in at **`/driver/login`** on their phone.
* On a delivery note pick the **Assigned driver** and (optionally) paste the **Location (Google Map link)**.
* The driver sees only *their own* pending deliveries: project, customer, shipping address, items, a **Navigate** button
  (opens the Google Map link; if none was added it searches the shipping address), a **Call customer** button, and
  **Mark as delivered** (must enter who received the goods; remarks optional). Drivers cannot see anything else.
* Delivered notes show who marked them and when, in the delivery note page and on the driver's Delivered tab.
* Removing a driver disables their login.

## Marking delivered from the office
Staff with the *Mark as delivered* permission get a tick button on every pending row in Delivery Notes
(date, received by, remarks), or can use the status box on the note page.

## Users
* **Admin** – everything.
* **Delivery user** – delivery notes and drivers only. Per-user switches: create, edit, mark delivered, delete,
  and "see all notes" (otherwise they only see notes they created). New users default to create + edit + mark delivered + see all.

## Default notes & terms
Settings → *Default Notes & Terms* holds the text printed at the bottom of every new note (taken from the sample).
It can still be edited on each individual note.

Developer credit appears only inside the application interface, never on PDFs.
