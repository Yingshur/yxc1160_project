import os
from datetime import datetime
import csv
from app.new_file import db
from flask import current_app


def to_csv_total():
    dir_regular_backup = os.environ.get("BACKUP_DIR", os.path.join(os.getcwd(), "regular_backup"))
    os.makedirs(dir_regular_backup, exist_ok=True)
    time = datetime.now().strftime('%Y%m%d_%H%M%S')
    with current_app.app_context():
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