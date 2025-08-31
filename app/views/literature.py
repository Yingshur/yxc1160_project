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



literature_bp = Blueprint("literature_bp", __name__)


@literature_bp.route("/admin/manage_additions/edit_info_literature/<int:id>", methods = ['GET', 'POST'], endpoint = "edit_info_literature")
@admin_only
@login_required
def edit_info_literature(id):
    literature_edit = db.session.get(TemporaryLiterature, id)
    return render_template("edit_add_info_literature.html", book = literature_edit , title = "Preview")


@literature_bp.route("/admin/manage_additions/add_info_literature/<int:id>", methods = ['GET', 'POST'], endpoint = "add_info_literature")
@admin_only
@login_required
def add_info_literature(id):
    literature_add = db.session.get(TemporaryLiterature, id)
    return render_template("edit_add_info_literature.html", book = literature_add, title = "Preview")



@literature_bp.route("/delete_literature_/<int:id>", methods = ['GET', 'POST'], endpoint = "delete_literature_")
@admin_only
def delete_literature_(id):
    delete_literature_ = db.session.get(Literature, id)
    to_csv(current_user.username, delete_literature_.title)
    if delete_literature_.images:
        delete_images_ = delete_literature_.images
        for image in delete_images_:
            db.session.delete(image)
    db.session.delete(delete_literature_)
    delete_log = LogBook(original_id=id, title=delete_literature_.title,
                         username=current_user.username)
    db.session.add(delete_log)
    db.session.commit()
    to_csv_overwrite(current_user.username)
    return redirect(url_for('literature_bp.literature_info'))


@literature_bp.route('/art_selection/literature_info', methods= ['GET', 'POST'], endpoint = "literature_info")
def literature_info():
    form = LiteratureForm()
    literature_lst = db.session.query(Literature).all()
    return render_template('literature_info.html', title = "Literature",literature_lst = literature_lst, new_form = form, form_open = False)


@literature_bp.route('/art_selection/literature_info/literature_info_detail/<int:id>', methods= ['GET', 'POST'], endpoint = "literature_info_detail")
def literature_info_detail(id):
    literature_first = db.session.get(Literature, id)
    form_1 = ImageUploadForm()
    form_2 = ImageEditForm()
    form = LiteratureForm(obj=literature_first)
    images = db.session.query(Image).filter(Image.literature_id == id).all()
    form.edit.data = literature_first.id
    return render_template('literature_info_detail.html', title = "Literature information",book = literature_first, new_form = form, new_form_1 = form_1, new_form_2 = form_2, images =images, form_open = False, form_open_1 = False, form_open_2 = False)


@literature_bp.route("/add_new_literature", methods = ['POST', 'GET'], endpoint = "add_new_literature")
@login_required
def add_new_literature():
    form = LiteratureForm()
    literature_lst = db.session.query(Literature).all()
    if form.validate_on_submit() and int(form.edit.data) == -1:
        if current_user.role == "Admin":
            column_names = [column.name for column in Literature.__table__.columns if column.name != "id"]
            new_literature = Literature(
                **{column: getattr(form, column).data for column in column_names if hasattr(form, column)})
            db.session.add(new_literature)
            new_log_26 = LogBook(original_id=new_literature.id, title=new_literature.title,
                                 username=current_user.username)
            to_csv(current_user.username, new_literature.title)
            db.session.add(new_log_26)
            db.session.commit()
            # print(form.portrait.data.filename)
            if form.image.data:
                save_uploaded_images(file=form.image.data, obj_id=new_literature.id,
                                     field_name="literature_id",
                                     model=Image)
                db.session.commit()
            to_csv_overwrite(current_user.username)
            return redirect(url_for("literature_bp.literature_info"))
        else:
            column_names = [column.name for column in TemporaryLiterature.__table__.columns if column.name != "id"]
            temporary_literature_edit = TemporaryLiterature(
                **{column: getattr(form, column).data for column in column_names if hasattr(form, column)}, old_id = int(form.edit.data), username = current_user.username)
            db.session.add(temporary_literature_edit)
            db.session.commit()
            id_data = db.session.query(TemporaryLiterature).filter_by(username=current_user.username).order_by(
                TemporaryLiterature.id.desc()).first()
            if form.image.data:
                save_uploaded_images(file=form.image.data, obj_id=id_data.id, field_name="temporary_literature_id", model=TemporaryImage, form_data=form, temporary=True)
                db.session.commit()
            confirmation_email(id_data.id)
            flash("Request successfully uploaded, please wait for approval", "success" )
            return redirect(url_for("literature_bp.literature_info"))
    return render_template('literature_info.html', title = "Literature", literature_lst = literature_lst , form_open = True, new_form = form )


@literature_bp.route('/edit_literature/<int:id>', methods = ['POST', 'GET'], endpoint = "edit_literature")
@login_required
def edit_literature(id):
    literature_first = db.session.get(Literature, id)
    form = LiteratureForm()
    form_1 = ImageUploadForm()
    form_2 = ImageEditForm()
    images = db.session.query(Image).filter(Image.literature_id == id).all() or []
    if request.method == "GET":
        form = LiteratureForm(obj=literature_first, data={"edit": literature_first.id})
    if form.validate_on_submit():
        if current_user.role == "Admin":
            literature_new_edit = db.session.get(Literature, int(form.edit.data))
            form.populate_obj(literature_new_edit)
            new_log_28 = LogBook(original_id=literature_new_edit.id, title=literature_new_edit.title,
                                 username=current_user.username)
            to_csv(current_user.username, literature_new_edit.title)
            db.session.add(new_log_28)
            if form.image.data:
                save_uploaded_images(file=form.image.data, obj_id=literature_new_edit.id, field_name="literature_id", model=Image)
            db.session.commit()
            to_csv_overwrite(current_user.username)
            return redirect(url_for('literature_bp.literature_info_detail', id=literature_new_edit.id))
        else:
            column_names = [column.name for column in TemporaryLiterature.__table__.columns if column.name != "id"]
            temporary_edit = TemporaryLiterature(
                **{column: getattr(form, column).data for column in column_names if hasattr(form, column)}, old_id = int(form.edit.data), username = current_user.username)
            db.session.add(temporary_edit)
            db.session.commit()
            id_data = db.session.query(TemporaryLiterature).filter_by(username=current_user.username).order_by(
                TemporaryLiterature.id.desc()).first()
            if form.image.data:
                save_uploaded_images(file=form.image.data, obj_id=id_data.id, field_name="temporary_literature_id", model=TemporaryImage, form_data=form, temporary=True)
            db.session.commit()
            confirmation_email(id_data.id)
            flash("Request successfully uploaded, please wait for approval", "success" )
            return redirect(url_for('literature_bp.literature_info_detail', id=literature_first.id))
    return render_template("literature_bp.literature_info_detail.html", id=literature_first.id, form_open = True, form_1 = False, form_2 = False,book = literature_first, new_form = form, new_form_1 = form_1, new_form_2 = form_2,title = "Literature information", images = images)
    #return render_template("war_info.html", war = war, title = "Battle information")


@literature_bp.route('/edit_literature_users/<int:id>', methods = ['POST', 'GET'], endpoint = "edit_literature_users")
@login_required
def edit_literature_users(id):
    literature_first = db.session.get(TemporaryLiterature, id)
    form = LiteratureForm()
    if request.method == "GET":
        form = LiteratureForm(obj=literature_first, data={"edit": literature_first.id})
    if form.validate_on_submit():
        literature_new_edit = db.session.get(TemporaryLiterature, int(form.edit.data))
        form.populate_obj(literature_new_edit)
        if form.image.data:
            save_uploaded_images(file=form.image.data, obj_id=literature_new_edit.id, field_name="temporary_literature_id",
                                 model=TemporaryImage, form_data=form, temporary=True)
        if literature_first.status != "Pending":
            literature_new_edit.status = "Pending"
            confirmation_email(id=literature_first.id)
        db.session.commit()
        return redirect(url_for('literature_bp.literature_info_edit_user', id=literature_first.id))
    return render_template("literature_info_edit_user.html", book = literature_first, new_form = form, form_open = True, title = "Editing requests")


@literature_bp.route("/approve_literature_edit/<int:id>", methods = ['GET', 'POST'], endpoint = "approve_literature_edit")
@admin_only
def approve_literature_edit(id):
    try:
        literature_first = db.session.get(TemporaryLiterature, id)
        new_literature = db.session.get(Literature, int(literature_first.old_id))
        to_csv(current_user.username, new_literature.title)
        column_names = [column.name for column in Literature.__table__.columns if column.name not in ("id", "old_id")]
        for column in column_names:
            setattr(new_literature, column, getattr(literature_first, column))
        user = db.session.query(User).filter_by(username=literature_first.username).first()
        new_log_30 = LogBook(original_id=id, title=new_literature.title,
                             username=current_user.username)
        db.session.add(new_log_30)
        if literature_first.temporary_images:
            approval_add_image(literature_first, obj_id=new_literature.id, field_name="literature_id", model=Image)
        approval_email(user_email=user.email, emperor_title=new_literature.title)
        db.session.delete(literature_first)
        db.session.commit()
        to_csv_overwrite(current_user.username)
    except Exception as e:
        flash("Article no longer available due to version change!", "warning")
    return redirect(url_for('admin_bp.manage_edits'))


@literature_bp.route("/approve_literature_add/<int:id>", methods=['GET', 'POST'], endpoint = "approve_literature_add")
@admin_only
def approve_literature_add(id):
    add_literature = db.session.get(TemporaryLiterature, id)
    column_names = [column.name for column in Literature.__table__.columns if column.name != "id"]
    new_literature = Literature(
        **{column: getattr(add_literature, column) for column in column_names if hasattr(add_literature, column)})
    user = db.session.query(User).filter_by(username = add_literature.username).first()
    to_csv(current_user.username, new_literature.title)
    db.session.add(new_literature)
    db.session.commit()
    new_log_3200 = LogBook(original_id=new_literature.id, title=new_literature.title,
                         username=current_user.username)
    db.session.add(new_log_3200)
    if add_literature.temporary_images:
        approval_add_image(add_literature, obj_id=new_literature.id, field_name="literature_id", model=Image)
    approval_email(user_email=user.email, emperor_title=add_literature.title)
    db.session.delete(add_literature)
    db.session.commit()
    to_csv_overwrite(current_user.username)
    return redirect(url_for('admin_bp.manage_additions'))


@literature_bp.route("/reject_literature_add_edit/<int:id>", methods = ['GET', 'POST'], endpoint = "reject_literature_add_edit")
@admin_only
def reject_literature_add_edit(id):
    add_literature = db.session.get(TemporaryLiterature, id)
    add_literature.status = "Reject"
    user = db.session.query(User).filter_by(username = add_literature.username).first()
    rejection_email(user_email=user.email, emperor_title=add_literature.title)
    db.session.commit()
    return redirect(request.referrer)


@literature_bp.route("/admin_delete_literature/<int:id>", methods = ['GET', 'POST'], endpoint = "admin_delete_literature")
@admin_only
def admin_delete_literature(id):
    delete_literature_temporary = db.session.get(TemporaryLiterature, id)
    if delete_literature_temporary.temporary_images:
        delete_image_temporary = delete_literature_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_literature_temporary)
    db.session.commit()
    return redirect(request.referrer)


@literature_bp.route("/manage_edits_additions_users/literature_info_edit_user/<int:id>", methods = ['GET', 'POST'], endpoint = "literature_info_edit_user")
@login_required
def literature_info_edit_user(id):
    #war_first = db.session.get(TemporaryWar, id)
    literature_first = db.session.get(TemporaryLiterature, id)
    form = LiteratureForm(obj=literature_first)
    form.edit.data = literature_first.id
    return render_template("literature_info_edit_user.html",book = literature_first, form_open = False, title="Literature edit/addition information", new_form=form)
