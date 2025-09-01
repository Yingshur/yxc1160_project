from datetime import time, datetime
import os

from dominate.svg import title
from flask import current_app as app
from app.models import Version, CurrentVersion, NewVersion, Emperor, Artifact, Image, Literature, Architecture, War
import csv
from app import app
from app.new_file import db
import uuid
import threading

def to_csv_function_1(user_name, title):
    #dir_old_version = os.path.join(os.getcwd(), "old_versions")
    #os.makedirs(r"C:\Users\verit\PycharmProjects\yxc1160 project\old_versions", exist_ok=True)
    unique_number = uuid.uuid4().hex
    time_ = datetime.now().strftime('%Y%m%d_%H%M%S')
    dir_old_versions = os.environ.get("BACKUP_DIR", os.path.join(os.getcwd(), "old_versions"))
    os.makedirs(dir_old_versions, exist_ok=True)
    with (app.app_context()):
        for name_of_table, table in db.metadata.tables.items():
            if name_of_table in (Emperor.__tablename__, Image.__tablename__, Artifact.__tablename__, Literature.__tablename__, Architecture.__tablename__, War.__tablename__):
                rows_ = db.session.execute(table.select()).all()
                columns = [column_.name for column_ in table.columns]
                file_name = os.path.join(dir_old_versions,
                                         f"{name_of_table}_{unique_number}.csv")
                with open(file_name, "w", newline="", encoding="utf-8-sig") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(columns)
                    for row in rows_:
                        writer.writerow(row)
        old_version = Version(username=user_name, created_at=time_, unique=unique_number, title = title)
        db.session.add(old_version)
        current_version = db.session.query(CurrentVersion).first()
        if current_version:
            current_version.username = user_name
            current_version.time_version = time_
        db.session.commit()



def to_csv_function_overwrite(user_name):
    #dir_old_version = os.path.join(os.getcwd(), "old_versions")
    #os.makedirs(r"C:\Users\verit\PycharmProjects\yxc1160 project\old_versions", exist_ok=True)
    time_ = datetime.now().strftime('%Y%m%d_%H%M%S')
    dir_old_versions = os.environ.get("BACKUP_DIR", os.path.join(os.getcwd(), "new_versions"))
    os.makedirs(dir_old_versions, exist_ok=True)
    unique_number = uuid.uuid4().hex
    with (app.app_context()):
        for name_of_table, table in db.metadata.tables.items():
            if name_of_table in (Emperor.__tablename__, Image.__tablename__, Artifact.__tablename__, Literature.__tablename__, Architecture.__tablename__, War.__tablename__):
                rows_ = db.session.execute(table.select()).all()
                columns = [column_.name for column_ in table.columns]
                file_name = os.path.join(dir_old_versions,
                                         f"{name_of_table}_{unique_number}.csv")
                with open(file_name, "w", newline="", encoding="utf-8-sig") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(columns)
                    for row in rows_:
                        writer.writerow(row)
        #current_version_ = db.session.query(NewVersion).first()
        current_version_1 = NewVersion(username=user_name, time_version=time_, unique = unique_number)
        db.session.add(current_version_1)
        db.session.commit()


def to_csv(username, _title_):
    threading.Thread(target=to_csv_function_1, args=(username,_title_,)).start()

def to_csv_overwrite(username):
    threading.Thread(target=to_csv_function_overwrite, args=(username,)).start()