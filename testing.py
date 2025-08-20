import threading
from turtledemo.penrose import start
import uuid
import os
import csv
import requests
import time
from app import db, app
from app.models import Emperor, Image, War, Artifact, Architecture, Literature, LogBook
from playwright.sync_api import sync_playwright

urls = ["https://yxc1160project-production.up.railway.app/", "https://yxc1160project-production.up.railway.app/dynasties", "https://yxc1160project-production.up.railway.app/dynasties/macedonians", "https://yxc1160project-production.up.railway.app/art_selection/architecture_info", "https://yxc1160project-production.up.railway.app/art_selection/architecture_info/architecture_info_detail/1?", "https://yxc1160project-production.up.railway.app/dynasties/macedonians"]
urls_1 = ["https://yxc1160project-production.up.railway.app/account", "https://yxc1160project-production.up.railway.app/admin", "https://yxc1160project-production.up.railway.app/admin/manage_edits", "https://yxc1160project-production.up.railway.app/admin/manage_additions"]
basedir = os.path.abspath(os.path.dirname(__file__))

from datetime import datetime




def to_csv_total():
    dir_regular_backup = os.environ.get("BACKUP_DIR", os.path.join(os.getcwd(), "regular_backup"))
    os.makedirs(dir_regular_backup, exist_ok=True)
    time = datetime.now().strftime('%Y%m%d_%H%M%S')
    with (app.app_context()):
        for name_of_table, table in db.metadata.tables.items():
            rows_ = db.session.execute(table.select()).all()
            columns = [column_.name for column_ in table.columns]
            file_name = os.path.join(dir_regular_backup,
                                     f"{name_of_table}_{time}.csv")
            with open(file_name, "w", newline="", encoding="utf-8-sig") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(columns)
                for row in rows_:
                    writer.writerow(row)

threading.Thread(target=to_csv_total).start()

for url in urls:
    try:
        r = requests.get(url, timeout=10)
        print(f"{time.ctime()} - {r.status_code} - OK")
    except requests.RequestException:
        print(f"{time.ctime()} - NOT WORKING")






url_2 = "http://yxc1160project-production.up.railway.app/"
r = requests.get(url_2, allow_redirects=True)
if r.url.startswith("https://"):
    print("HTTP is redirected to HTTPS")
else:
    print("Insecure HTTP access is allowed")




for url in urls_1:
    r = requests.get(url, allow_redirects=False)
    if r.status_code in [401, 403, 500]:
        print(f"Access blocked, code {r.status_code}")

    elif "/login" in r.headers.get("Location", "") or "gone wrong" in r.text:
        print("Access blocked by 'login-only'")
    else:
        print("Unauthorised success succeeds")


for url in urls:
    try:
        start_ = time.time()
        response = requests.get(url, timeout=10)
        end = time.time()
        print(f"Status code: {response.status_code}")
        print(f"Load time: {end - start_:.3f} seconds")
    except requests.RequestException as e:
        print(f"ERROR: {e}")



for url in urls:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        start_ = time.time()
        page.goto(url, wait_until="load")
        end = time.time()
        print(f"Full page takes {end - start_:.3f} seconds.")



#with app.app_context():
    #start_ = time.time()
    #rows = db.session.query(Emperor).all()
    #rows_1 = db.session.query(Image).all()
    #rows_2 = db.session.query(War).all()
    #rows_3 = db.session.query(Architecture).all()
    #rows_4 = db.session.query(Literature).all()
    #rows_5 = db.session.query(Artifact).all()
    #print(f"Data table took {time.time() - start_:.3f} seconds for {len(rows)} rows.")

