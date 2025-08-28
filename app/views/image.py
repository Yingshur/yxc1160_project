from app.decorators.management_functions import admin_only
from flask import  redirect, url_for, flash, request
from app.models import Image
from app.forms import ArchitectureForm, ImageEditForm, ImageUploadForm, LiteratureForm, ArtifactForm, DeleteForm, ChatForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app.new_file import db
from urllib.parse import urlsplit
from sqlalchemy import or_, and_
from app import app
import csv
from huggingface_hub import InferenceClient
from app.mixed.version_control import to_csv_function_1, to_csv_function_overwrite, to_csv, to_csv_overwrite
from app.mixed.images_handling import save_uploaded_images, approval_add_image, gallery_upload, gallery_upload_addition
from flask import Blueprint
import os
from app.mixed.delete_unused_images import delete_unused_images

image_bp = Blueprint("image_bp", __name__)


@image_bp.route("/edit_an_image/<int:id>", methods = ['GET', 'POST'], endpoint = "edit_an_image")
@login_required
def edit_an_image(id):
    form = ImageEditForm()
    form_1 = ArchitectureForm()
    form_2 = ImageUploadForm()
    if (current_user.user_type == "Authorised" or current_user.role == "Admin") and form.validate_on_submit():
        if form.validate_on_submit():
            to_csv(current_user.username)
            photo = db.session.query(Image).filter_by(id=form.id_number.data).first()
            if photo:
                if photo.architecture_id:
                    gallery_upload(form, photo, category="architecture")
                    db.session.commit()
                    to_csv_overwrite(current_user.username)
                    flash("Successfully edited", "success")
                    return redirect(url_for('architecture_bp.architecture_info_detail', id=id))
                elif photo.literature_id:
                    gallery_upload(form, photo, category="literature")
                    db.session.commit()
                    to_csv_overwrite(current_user.username)
                    flash("Successfully edited", "success")
                    return redirect(url_for('literature_bp.literature_info_detail', id=id))
                elif photo.artifact_id:
                    gallery_upload(form, photo, category="artifact")
                    db.session.commit()
                    to_csv_overwrite(current_user.username)
                    flash("Successfully edited", "success")
                    return redirect(url_for('artifact_bp.artifact_info_detail', id=id))
            else:
                flash("Invalid ID number", "danger")
                return redirect(request.referrer)
    flash("Invalid details, please resubmit the form", "warning")
    return redirect(request.referrer)


@image_bp.route('/add_an_image/<int:id>/<string:category>/', methods = ['GET', 'POST'], endpoint = "add_an_image")
@login_required
def add_an_image(id, category):
    form = ImageUploadForm()
    form_1 = ArchitectureForm()
    form_2 = ImageEditForm()
    if current_user.user_type == "Authorised" or current_user.role == "Admin":
        if form.validate_on_submit():
            to_csv(current_user.username)
            if category == "architecture":
                gallery_upload_addition(form, category, obj_id=id)
                flash("Successfully uploaded", "success")
                to_csv_overwrite(current_user.username)
                return redirect(url_for('architecture_bp.architecture_info_detail', id=id))
            elif category == "literature":
                gallery_upload_addition(form, category, obj_id=id)
                flash("Successfully uploaded", "success")
                to_csv_overwrite(current_user.username)
                return redirect(url_for('literature_bp.literature_info_detail', id=id))
            elif category == "artifact":
                gallery_upload_addition(form, category, obj_id=id)
                flash("Successfully uploaded", "success")
                to_csv_overwrite(current_user.username)
                return redirect(url_for('artifact_bp.artifact_info_detail', id=id))
    flash("Invalid details, please resubmit the form", "warning")
    return redirect(request.referrer)


@image_bp.route("/delete_image/<int:id>", methods = ["POST"], endpoint ="delete_image")
@admin_only
def delete_image(id):
    image_for_deletion = db.session.get(Image, id)
    if image_for_deletion:
        to_csv(current_user.username)
        db.session.delete(image_for_deletion)
        db.session.commit()
        to_csv_overwrite(current_user.username)
    return redirect(request.referrer)
