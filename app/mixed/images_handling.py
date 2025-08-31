import uuid

from dominate.tags import caption

from app.new_file import db
from app.models import User, Emperor, \
    Verification, Invitation, Image, TemporaryEmperor, TemporaryImage, War, TemporaryWar, Architecture, TemporaryArchitecture, Literature, TemporaryLiterature, Artifact, TemporaryArtifact, LogBook, Deletion, Version, CurrentVersion, NewVersion
import os
from app import app
from werkzeug.utils import secure_filename
from flask import url_for
from flask_login import current_user
from app.mixed.emails import new_confirmation_email


def save_uploaded_images(file, obj_id, field_name, model, form_data = None, temporary = False):
    file_name = secure_filename(file.filename)
    uuid_ = uuid.uuid4().hex[:8]
    file_name = f"{uuid_}_{file_name}"
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    new_path_for_uploading = path_for_uploading.replace('\\', '/')
    file.save(new_path_for_uploading)
    if temporary == False:
        photo = db.session.query(model).filter_by(**{field_name: obj_id}).order_by(
            model.id.asc()).first()
        if not photo:
            photo = model()
            setattr(photo, field_name, obj_id)
            db.session.add(photo)
        photo.filename = file_name
        photo.url = url_for("static", filename=f"images/uploaded_photos/{file_name}")
    else:
        photo = db.session.query(model).filter_by(**{field_name: obj_id}).order_by(
            model.id.asc()).first()
        if not photo:
            photo = model(username = current_user.username, old_id = int(form_data.edit.data), filename = file_name, url = url_for("static", filename=f"images/uploaded_photos/{file_name}"), **{field_name: obj_id})
            setattr(photo, field_name, obj_id)
            db.session.add(photo)
            db.session.commit()
        photo.filename = file_name
        photo.url = url_for("static", filename=f"images/uploaded_photos/{file_name}")
    db.session.commit()
    if current_user.role == "Admin":
        new_log_record = LogBook(original_id=photo.id, title=file_name, username=current_user.username)
        db.session.add(new_log_record)
    db.session.commit()
    return photo

def approval_add_image(temporary, obj_id, field_name, model):
    file_name = secure_filename(f"{temporary.temporary_images[0].filename}")
    photo = db.session.query(model).filter_by(**{field_name: obj_id}).order_by(
        model.id.asc()).first()
    if not photo:
        photo = model(**{field_name: obj_id})
        db.session.add(photo)
    photo.filename = file_name
    photo.url = url_for("static", filename=f"images/uploaded_photos/{file_name}")
    db.session.commit()
    new_log_record = LogBook(original_id=photo.id, title=file_name, username=current_user.username)
    db.session.add(new_log_record)
    db.session.delete(temporary.temporary_images[0])
    db.session.commit()

def gallery_upload(form, photo, category):
    if not form.image.data:
        return None
    file_name = secure_filename(form.image.data.filename)
    uuid_ = uuid.uuid4().hex[:8]
    file_name = f"{uuid_}_{file_name}"
    path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    new_path_for_uploading = path_for_uploading.replace('\\', '/')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    form.image.data.save(new_path_for_uploading)
    photo.filename = file_name
    photo.url = url_for('static', filename=f"images/uploaded_photos/{file_name}")
    photo.caption = form.caption.data
    db.session.add(photo)
    record = LogBook(original_id=photo.id, title=file_name,
                            username=current_user.username)
    db.session.add(record)
    db.session.commit()
    if current_user.user_type == "Authorised":
        new_confirmation_email(id=photo.id, category=category)
    return photo

def gallery_upload_addition(form, category, obj_id = None):
    if not form.image.data:
        return None
    file_name = secure_filename(form.image.data.filename)
    uuid_ = uuid.uuid4().hex[:8]
    file_name = f"{uuid_}_{file_name}"
    path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    new_path_for_uploading = path_for_uploading.replace('\\', '/')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    all_sections = {"architecture" : "architecture_id",
                    "literature": "literature_id",
                    "artifact": "artifact_id"
    }
    category_name = all_sections.get(category)
    form.image.data.save(new_path_for_uploading)
    photo = Image(filename = file_name, url = url_for('static', filename=f"images/uploaded_photos/{file_name}"), caption = form.caption.data, **{category_name: obj_id})
    db.session.add(photo)
    db.session.commit()
    if current_user.user_type == "Authorised":
        new_confirmation_email(id=photo.id, category=category)
    id_data = db.session.query(Image).filter(getattr(Image, category_name)==obj_id).order_by(Image.id.desc()).first()
    record = LogBook(original_id=id_data.id, title=file_name,
                            username=current_user.username)
    db.session.add(record)
    db.session.commit()
    return photo



