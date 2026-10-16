# Paste the contents of this file into your PythonAnywhere WSGI file
# (Web tab -> "WSGI configuration file"), replacing everything in it.
# Replace YOURUSER with your PythonAnywhere username.
import os, sys

PROJECT = '/home/YOURUSER/gh-delivery'
os.environ['DATA_DIR'] = '/home/YOURUSER/gh-data'            # database, uploads, PDF archive, backups
os.environ['SECRET_KEY'] = 'PUT-A-LONG-RANDOM-TEXT-HERE'
os.environ['ADMIN_PASSWORD'] = 'PUT-A-STRONG-PASSWORD-HERE'  # only used the first time (empty database)
os.environ['BEHIND_HTTPS_PROXY'] = '1'                       # site is served over https

if PROJECT not in sys.path:
    sys.path.insert(0, PROJECT)

from app import app as application   # noqa: E402
