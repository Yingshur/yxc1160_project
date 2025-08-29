
from app.decorators.management_functions import admin_only
from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory,session, jsonify
from app.mixed.emails import verification_email, confirmation_email, approval_email, new_confirmation_email, rejection_email
import folium
from app.models import User, Emperor, \
    Verification, Invitation, Image, TemporaryEmperor, TemporaryImage, War, TemporaryWar, Architecture, TemporaryArchitecture, Literature, TemporaryLiterature, Artifact, TemporaryArtifact, LogBook, Deletion, Version, CurrentVersion, NewVersion
from app.forms import ChooseForm, LoginForm, ChangePasswordForm, ChangeEmailForm, RegisterForm, RegisterEmail, \
    AdminCodeForm, InvitationCodeForm, AllEmperorForm, WarForm, ArchitectureForm, ImageEditForm, ImageUploadForm, LiteratureForm, ArtifactForm, DeleteForm, ChatForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
from app.new_file import db
from app.mixed.version_control import to_csv_function_1, to_csv_function_overwrite, to_csv, to_csv_overwrite
from app.mixed.images_handling import save_uploaded_images, approval_add_image, gallery_upload, gallery_upload_addition
from flask import Blueprint
import os
from app.mixed.delete_unused_images import delete_unused_images

artifact_bp = Blueprint("artifact_bp", __name__)


@artifact_bp.route("/admin/manage_additions/edit_info_artifact/<int:id>", methods = ['GET', 'POST'], endpoint = "edit_info_artifact")
@admin_only
@login_required
def edit_info_artifact(id):
    artifact_edit = db.session.get(TemporaryArtifact, id)
    return render_template("edit_add_info_artifact.html", artifact = artifact_edit , title = "Preview")


@artifact_bp.route("/admin/manage_additions/add_info_artifact/<int:id>", methods = ['GET', 'POST'], endpoint = "add_info_artifact")
@admin_only
@login_required
def add_info_artifact(id):
    artifact_add = db.session.get(TemporaryArtifact, id)
    return render_template("edit_add_info_artifact.html", artifact = artifact_add, title = "Preview")


@artifact_bp.route("/delete_artifacts_/<int:id>", methods = ['GET', 'POST'], endpoint="delete_artifacts_")
@admin_only
def delete_artifacts_(id):
    delete_artifacts_ = db.session.get(Artifact, id)
    to_csv(current_user.username, delete_artifacts_.title)
    if delete_artifacts_.images:
        delete_images_ = delete_artifacts_.images
        for image in delete_images_:
            db.session.delete(image)
    db.session.delete(delete_artifacts_)
    db.session.commit()
    to_csv_overwrite(current_user.username)
    return redirect(url_for('artifact_bp.artifact_info'))


@artifact_bp.route('/art_selection/artifact_info', methods= ['GET', 'POST'], endpoint = "artifact_info")
def artifact_info():
    form = ArtifactForm()
    artifact_lst = db.session.query(Artifact).all()
    return render_template('artifact_info.html', title = "Artifact",artifact_lst = artifact_lst, new_form = form, form_open = False)


@artifact_bp.route('/art_selection/artifact_info/artifact_info_detail/<int:id>', methods= ['GET', 'POST'], endpoint = "artifact_info_detail")
def artifact_info_detail(id):
    artifact_first = db.session.get(Artifact, id)
    form_1 = ImageUploadForm()
    form_2 = ImageEditForm()
    images = db.session.query(Image).filter(Image.artifact_id == id).all()
    form = ArtifactForm(obj=artifact_first)
    form.edit.data = artifact_first.id
    return render_template('artifact_info_detail.html', title = "Artifact information",artifact = artifact_first, new_form = form, new_form_1 = form_1, new_form_2 = form_2, images =images, form_open = False, form_open_1 = False, form_open_2 = False)


@artifact_bp.route("/add_new_artifact", methods = ['POST', 'GET'], endpoint = "add_new_artifact")
@login_required
def add_new_artifact():
    form = ArtifactForm()
    artifact_lst = db.session.query(Artifact).all()
    if form.validate_on_submit() and int(form.edit.data) == -1:
        if current_user.role == "Admin":
            column_names = [column.name for column in Artifact.__table__.columns if column.name != "id"]
            new_artifact = Artifact(
                **{column: getattr(form, column).data for column in column_names if hasattr(form, column)})
            db.session.add(new_artifact)
            new_log_35 = LogBook(original_id=new_artifact.id, title=new_artifact.title,
                                 username=current_user.username)
            to_csv(current_user.username, new_artifact.title)
            db.session.add(new_log_35)
            db.session.commit()
            # print(form.portrait.data.filename)
            if form.image.data:
                save_uploaded_images(file=form.image.data, obj_id=new_artifact.id, field_name="artifact_id", model=Image)
                db.session.commit()
            to_csv_overwrite(current_user.username)
            return redirect(url_for("artifact_bp.artifact_info"))
        else:
            column_names = [column.name for column in TemporaryArtifact.__table__.columns if column.name != "id"]
            temporary_artifact_edit = TemporaryArtifact(**{column: getattr(form, column).data for column in column_names if hasattr(form, column)}, old_id = int(form.edit.data), username = current_user.username)
            db.session.add(temporary_artifact_edit)
            db.session.commit()
            if form.image.data:
                id_data = db.session.query(TemporaryArtifact).filter_by(username = current_user.username).order_by(TemporaryArtifact.id.desc()).first()
                save_uploaded_images(file=form.image.data, obj_id=id_data.id, field_name="temporary_artifact_id", model=TemporaryImage, form_data=form, temporary=True)
                db.session.commit()
                confirmation_email(temporary_artifact_edit.id)
            return redirect(url_for("artifact_bp.artifact_info"))
    return render_template('artifact_info.html', title = "Artifact", artifact_lst = artifact_lst , form_open = True, new_form = form )



@artifact_bp.route('/edit_artifact/<int:id>', methods = ['POST', 'GET'], endpoint = "edit_artifact")
@login_required
def edit_artifact(id):
    artifact_first = db.session.get(Artifact, id)
    form = ArtifactForm()
    form_1 = ImageUploadForm()
    form_2 = ImageEditForm()
    images = db.session.query(Image).filter(Image.artifact_id == id).all() or []
    if request.method == "GET":
        form = ArtifactForm(obj=artifact_first, data={"edit": artifact_first.id})
    if form.validate_on_submit():
        if current_user.role == "Admin":
            artifact_new_edit = db.session.get(Artifact, int(form.edit.data))
            to_csv(current_user.username, artifact_new_edit.title)
            form.populate_obj(artifact_new_edit)
            new_log_37 = LogBook(original_id=artifact_new_edit.id, title=artifact_new_edit.title, username=current_user.username)
            db.session.add(new_log_37)
            if form.image.data:
                save_uploaded_images(file=form.image.data, obj_id=artifact_new_edit.id, field_name="artifact_id", model=Image)
            db.session.commit()
            to_csv_overwrite(current_user.username)
            return redirect(url_for('artifact_bp.artifact_info_detail', id=artifact_new_edit.id))
        else:
            column_names = [column.name for column in TemporaryArtifact.__table__.columns if column.name != "id"]
            temporary_edit = TemporaryArtifact(
                **{column: getattr(form, column).data for column in column_names if hasattr(form, column)}, old_id = int(form.edit.data), username = current_user.username)
            db.session.add(temporary_edit)
            db.session.commit()
            if form.image.data:
                id_data = db.session.query(TemporaryArtifact).filter_by(username = current_user.username).order_by(TemporaryArtifact.id.desc()).first()
                save_uploaded_images(file=form.image.data, obj_id=id_data.id, field_name="temporary_artifact_id", model=TemporaryImage, form_data=form, temporary=True)
            db.session.commit()
            confirmation_email(id)
            return redirect(url_for('artifact_bp.artifact_info_detail', id=artifact_first.id))
    return render_template("artifact_info_detail.html", id=artifact_first.id, form_open = True, form_1 = False, form_2 = False,artifact = artifact_first, new_form = form, new_form_1 = form_1, new_form_2 = form_2,title = "Artifact information", images = images)
    #return render_template("war_info.html", war = war, title = "Battle information")


@artifact_bp.route('/edit_artifact_users/<int:id>', methods = ['POST', 'GET'], endpoint = "edit_artifact_users")
@login_required
def edit_artifact_users(id):
    artifact_first = db.session.get(TemporaryArtifact, id)
    form = ArtifactForm()
    if request.method == "GET":
        form = ArtifactForm(obj=artifact_first, data={"edit": artifact_first.id})
    if form.validate_on_submit():
        artifact_new_edit = db.session.get(TemporaryArtifact, int(form.edit.data))
        form.populate_obj(artifact_new_edit)
        if form.image.data:
            save_uploaded_images(file=form.image.data, obj_id=artifact_new_edit.id, field_name="temporary_artifact_id",
                                 model=TemporaryImage, form_data=form, temporary=True)
        if artifact_first.status != "Pending":
            artifact_new_edit.status = "Pending"
            confirmation_email(id=artifact_first.id)
        db.session.commit()
        return redirect(url_for('artifact_bp.artifact_info_edit_user', id=artifact_first.id))
    return render_template("artifact_info_edit_user.html", artifact = artifact_first, new_form = form, form_open = True, title = "Editing requests")



@artifact_bp.route("/approve_artifact_edit/<int:id>", methods = ['GET', 'POST'], endpoint = "approve_artifact_edit")
@admin_only
def approve_artifact_edit(id):
    try:
        artifact_first = db.session.get(TemporaryArtifact, id)
        new_artifact = db.session.get(Artifact, int(artifact_first.old_id))
        to_csv(current_user.username, new_artifact.title)
        column_names = [column.name for column in Artifact.__table__.columns if column.name not in ("id", "old_id")]
        for column in column_names:
            setattr(new_artifact, column, getattr(artifact_first, column))
        user = db.session.query(User).filter_by(username=artifact_first.username).first()
        new_log_39 = LogBook(original_id=id, title=new_artifact.title,
                             username=current_user.username)
        db.session.add(new_log_39)
        if artifact_first.temporary_images:
            approval_add_image(artifact_first, obj_id=new_artifact.id, field_name="artifact_id", model=Image)
        approval_email(user_email=user.email, emperor_title=new_artifact.title)
        db.session.delete(artifact_first)
        db.session.commit()
        to_csv_overwrite(current_user.username)
    except Exception as e:
        flash("Article no longer available due to version change!", "warning")
    return redirect(url_for('admin_bp.manage_edits'))


@artifact_bp.route("/approve_artifact_add/<int:id>", methods=['GET', 'POST'], endpoint = "approve_artifact_add")
@admin_only
def approve_artifact_add(id):
    add_artifact = db.session.get(TemporaryArtifact, id)
    column_names = [column.name for column in Artifact.__table__.columns if column.name != "id"]
    new_artifact = Artifact(
        **{column: getattr(add_artifact, column) for column in column_names if hasattr(add_artifact, column)})

    user = db.session.query(User).filter_by(username = add_artifact.username).first()
    db.session.add(new_artifact)
    db.session.commit()
    new_log_4100 = LogBook(original_id=new_artifact.id, title=new_artifact.title,
                         username=current_user.username)
    to_csv(current_user.username, new_artifact.title)
    db.session.add(new_log_4100)
    if add_artifact.temporary_images:
        approval_add_image(add_artifact, obj_id=new_artifact.id, field_name="artifact_id", model=Image)
    approval_email(user_email=user.email, emperor_title=add_artifact.title)
    db.session.delete(add_artifact)
    db.session.commit()
    to_csv_overwrite(current_user.username)
    return redirect(url_for('admin_bp.manage_additions'))


@artifact_bp.route("/reject_artifact_add_edit/<int:id>", methods = ['GET', 'POST'], endpoint = "reject_artifact_add_edit")
@admin_only
def reject_artifact_add_edit(id):
    add_artifact = db.session.get(TemporaryArtifact, id)
    add_artifact.status = "Reject"
    user = db.session.query(User).filter_by(username = add_artifact.username).first()
    rejection_email(user_email=user.email, emperor_title=add_artifact.title)
    db.session.commit()
    return redirect(request.referrer)


@artifact_bp.route("/admin_delete_artifact/<int:id>", methods = ['GET', 'POST'], endpoint ="admin_delete_artifact")
@admin_only
def admin_delete_artifact(id):
    delete_artifact_temporary = db.session.get(TemporaryArtifact, id)
    if delete_artifact_temporary.temporary_images:
        delete_image_temporary = delete_artifact_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_artifact_temporary)
    db.session.commit()
    return redirect(request.referrer)


@artifact_bp.route("/manage_edits_additions_users/artifact_info_edit_user/<int:id>", methods = ['GET', 'POST'], endpoint = "artifact_info_edit_user")
@login_required
def artifact_info_edit_user(id):
    #war_first = db.session.get(TemporaryWar, id)
    artifact_first = db.session.get(TemporaryArtifact, id)
    form = ArtifactForm(obj=artifact_first)
    form.edit.data = artifact_first.id
    return render_template("artifact_info_edit_user.html",artifact = artifact_first, form_open = False, title="Artifacts edit/addition information", new_form=form)
