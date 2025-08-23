import os

from flask import flash

from app import app
from app.new_file import db
from app.models import Image, TemporaryImage

def delete_unused_images():
    folder = app.config["UPLOAD_FOLDER"]
    files_in_db = {img.filename for img in db.session.query(Image.filename).all()}
    files_in_folder = set(os.listdir(folder))
    unused_files = files_in_folder - files_in_db
    all_temporary_images = db.session.query(TemporaryImage).all()
    if not all_temporary_images:
        for file in unused_files:
            path = os.path.join(folder, file)
            try:
                os.remove(path)
            except Exception as e:
                flash(f"Error: {e}", "danger")
    else:
        flash("Please review existing requests!", "warning")
    return None



