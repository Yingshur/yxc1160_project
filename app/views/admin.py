from flask import abort
from random import randint
from app.decorators.management_functions import admin_only
from flask import render_template, redirect, url_for, flash
from app.models import User, Emperor, \
    Verification, Invitation, Image, TemporaryEmperor, TemporaryImage, War, TemporaryWar, Architecture, TemporaryArchitecture, Literature, TemporaryLiterature, Artifact, TemporaryArtifact, LogBook, Deletion, Version, CurrentVersion, NewVersion
from app.forms import ChooseForm, LoginForm, ChangePasswordForm, ChangeEmailForm, RegisterForm, RegisterEmail, \
    AdminCodeForm, InvitationCodeForm, AllEmperorForm, WarForm, ArchitectureForm, ImageEditForm, ImageUploadForm, LiteratureForm, ArtifactForm, DeleteForm, ChatForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app.new_file import db
from app.mixed.version_control import to_csv_function_1, to_csv_function_overwrite, to_csv, to_csv_overwrite
from app.mixed.images_handling import save_uploaded_images, approval_add_image, gallery_upload, gallery_upload_addition
from flask import Blueprint
import os
from app.mixed.delete_unused_images import delete_unused_images

admin_bp = Blueprint("admin_bp", __name__)


@admin_bp.route("/admin", endpoint = "admin")
@login_required
@admin_only
def admin():
    # if current_user.role != "Admin":
    #     return redirect(url_for('home'))
    form = ChooseForm()
    q = db.select(User)
    user_lst = db.session.scalars(q)
    #q = db.select(Enrollment)

    return render_template('admin.html', title="Admin", user_lst=user_lst, form=form, choose_form = form)


@admin_bp.route("/admin/manage_additions", methods = ['GET', 'POST'], endpoint = "manage_additions")
@admin_only
@login_required
def manage_additions():
    add_list = db.session.query(TemporaryEmperor).filter(TemporaryEmperor.old_id == -1).all()
    add_list_1 =  db.session.query(TemporaryWar).filter(TemporaryWar.old_id == -1).all()
    add_list_2 = db.session.query(TemporaryArchitecture).filter(TemporaryArchitecture.old_id ==-1).all()
    add_list_3 = db.session.query(TemporaryLiterature).filter(TemporaryLiterature.old_id == -1).all()
    add_list_4 = db.session.query(TemporaryArtifact).filter(TemporaryArtifact.old_id == -1).all()
    return render_template('manage_additions.html', title = "Manage additions", add_list = add_list, add_list_1 = add_list_1, add_list_2 = add_list_2, add_list_3 = add_list_3, add_list_4 = add_list_4)



@admin_bp.route("/admin/manage_edits", methods = ['GET', 'POST'], endpoint = "manage_edits")
@admin_only
@login_required
def manage_edits():
    edit_list = db.session.query(TemporaryEmperor).filter(TemporaryEmperor.old_id != -1).all()
    edit_list_1 = db.session.query(TemporaryWar).filter(TemporaryWar.old_id !=-1).all()
    edit_list_2 = db.session.query(TemporaryArchitecture).filter(TemporaryArchitecture.old_id != -1).all()
    edit_list_3 = db.session.query(TemporaryLiterature).filter(TemporaryLiterature.old_id != -1).all()
    edit_list_4 = db.session.query(TemporaryArtifact).filter(TemporaryArtifact.old_id != -1).all()
    return render_template('manage_edits.html', title = "Manage edits", edit_list = edit_list, edit_list_1 = edit_list_1, edit_list_2 = edit_list_2, edit_list_3 = edit_list_3, edit_list_4 = edit_list_4)


@admin_bp.route('/delete_user', methods=['POST'], endpoint = "delete_user")
@admin_only
def delete_user():
    form = ChooseForm()
    if form.validate_on_submit():
        u = db.session.get(User, int(form.choice.data))
        q = db.select(User).where((User.role == "Admin") & (User.id != u.id))
        first = db.session.scalars(q).first()
        if not first:
            flash("You can't delete your own account if there are no other admin users!", "danger")
        elif u.id == current_user.id:
            logout_user()
            db.session.delete(u)
            db.session.commit()
            return redirect(url_for('home_bp.home'))
        else:
            db.session.delete(u)
            db.session.commit()
    return redirect(url_for('admin_bp.admin'))



@admin_bp.route('/invitation_code/<int:id>', methods=['POST', 'GET'], endpoint = "invitation_code")
@admin_only
def invitation_code(id):
    form = ChooseForm()
    q = db.select(User)
    user_lst = db.session.scalars(q)
    code = randint(10**15, 10**16-1)
    new_data = Invitation(code = code, user_id = id)
    flash("invitation code generated successfully", "success")

    db.session.add(new_data)
    db.session.commit()
    return render_template("admin.html", title = "Admin", user_lst = user_lst, form = form)



@admin_bp.route('/toggle_user_type', methods=['POST'], endpoint = "toggle_user_type")
@admin_only
def toggle_user_type():
    form = ChooseForm()
    if form.validate_on_submit():
        u = db.session.get(User, int(form.choice.data))
        if u.user_type == "user":
            u.user_type = "Authorised"
        elif u.user_type == "Authorised":
            u.user_type = "user"
        db.session.commit()
    return redirect(url_for('admin_bp.admin'))


@admin_bp.route('/admin/de_admin/<int:id>', methods=['POST', 'GET'], endpoint = "de_admin")
@admin_only
@login_required
def de_admin(id):
    if current_user.user_type == "Autocrat":
        to_csv(current_user.username)
        form = ChooseForm()
        q = db.select(User)
        user_lst = db.session.scalars(q)
        user = db.session.get(User, id)
        user.role = "Normal"
        flash("User role has now been changed to normal", "success")
        db.session.commit()
        to_csv_overwrite(current_user.username)
    else:
        abort(403)
    return redirect(url_for('admin_bp.admin'))
    #return render_template("admin.html", title = "Admin", user_lst = user_lst, form = form)


@admin_bp.route("/delete_unused_images_/", methods = ["GET", "POST"], endpoint = "delete_unused_images_")
@admin_only
def delete_unused_images_():
    delete_unused_images()
    return redirect(url_for('admin_bp.admin'))