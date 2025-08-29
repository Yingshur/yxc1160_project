from itertools import cycle
from folium.plugins import MarkerCluster
from markupsafe import Markup
from app.decorators.management_functions import admin_only
from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory,session, jsonify
from app.mixed.emails import verification_email, confirmation_email, approval_email, new_confirmation_email, rejection_email
import folium
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

architecture_bp = Blueprint("architecture_bp", __name__)

@architecture_bp.route('/art_selection', endpoint = "art_selection")
def art_selection():
    return render_template("art_selection.html", title = "Roman Culture")


@architecture_bp.route("/admin/manage_edits/edit_info_architecture/<int:id>", methods = ['GET', 'POST'], endpoint = "edit_info_architecture")
@admin_only
@login_required
def edit_info_architecture(id):
    architecture_edit = db.session.get(TemporaryArchitecture, id)
    return render_template("edit_add_info_architecture.html", building = architecture_edit, title = "Preview")


@architecture_bp.route("/admin/manage_additions/add_info_architecture/<int:id>", methods = ['GET', 'POST'], endpoint = "add_info_architecture")
@admin_only
@login_required
def add_info_architecture(id):
    architecture_add = db.session.get(TemporaryArchitecture, id)
    return render_template("edit_add_info_architecture.html", building = architecture_add, title = "Preview")

@architecture_bp.route("/delete_architecture_/<int:id>", methods = ['GET', 'POST'], endpoint = "delete_architecture_")
@admin_only
def delete_architecture_(id):
    delete_architecture_ = db.session.get(Architecture, id)
    to_csv(current_user.username, delete_architecture_.title)
    if delete_architecture_.images:
        delete_images_ = delete_architecture_.images
        for image in delete_images_:
            db.session.delete(image)
    db.session.delete(delete_architecture_)
    db.session.commit()
    to_csv_overwrite(current_user.username)
    return redirect(url_for('architecture_bp.architecture_info'))


@architecture_bp.route('/art_selection/architecture_info', methods= ['GET', 'POST'], endpoint = "architecture_info")
def architecture_info():
    form = ArchitectureForm()
    buildings_lst = db.session.query(Architecture).all()
    buildings_map = folium.Map(location=[41.008333, 28.98], zoom_start=3)

    colors = cycle(['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
                    'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
                    'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray'])
    names = sorted({ building.location for building in buildings_lst if building.location})
    building_colors = {name: next(colors) for name in names}
    cluster = MarkerCluster().add_to(buildings_map)

    for building in buildings_lst:
        if building.latitude is not None and building.longitude is not None:
            color = building_colors.get(building.location, 'gray')
            folium.Marker(location= [building.latitude, building.longitude],
                          tooltip=building.title,
                          popup=folium.Popup(f"<b>{building.title}</b><br>{building.construction_completed}<br>{building.building_type}", max_width=300),
                          icon=folium.Icon(color=color)
            ).add_to(cluster)
    building_html = buildings_map._repr_html_()

    return render_template('architecture_info.html', title = "Architecture", buildings_lst = buildings_lst, architecture_html =Markup(building_html) , new_form = form, form_open = False)



@architecture_bp.route('/art_selection/architecture_info/architecture_info_detail/<int:id>', methods= ['GET', 'POST'], endpoint = "architecture_info_detail")
def architecture_info_detail(id):
    form_1 = ImageUploadForm()
    form_2 = ImageEditForm()
    architecture_first = db.session.get(Architecture, id)
    form = ArchitectureForm(obj=architecture_first)
    images = db.session.query(Image).filter(Image.architecture_id == id).all()
    form.edit.data = architecture_first.id
    return render_template('architecture_info_detail.html', title = "Architecture Info", new_form = form, new_form_1 = form_1, new_form_2 = form_2,form_open = False ,form_open_1 = False,form_open_2 = False ,building = architecture_first, images = images)


@architecture_bp.route("/add_new_architecture", methods = ['POST', 'GET'], endpoint = "add_new_architecture")
@login_required
def add_new_architecture():
    form = ArchitectureForm()
    buildings_lst = db.session.query(Architecture).all()
    buildings_map = folium.Map(location=[41.008333, 28.98], zoom_start=3)

    colors = cycle(['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
                    'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
                    'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray'])
    names = sorted({building.location for building in buildings_lst if building.location})
    building_colors = {name: next(colors) for name in names}
    cluster = MarkerCluster().add_to(buildings_map)

    for building in buildings_lst:
        if building.latitude is not None and building.longitude is not None:
            color = building_colors.get(building.location, 'gray')
            folium.Marker(location=[building.latitude, building.longitude],
                          tooltip=building.title,
                          popup=folium.Popup(
                              f"<b>{building.title}</b><br>{building.construction_completed}<br>{building.building_type}",
                              max_width=300),
                          icon=folium.Icon(color=color)
                          ).add_to(cluster)
    building_html = buildings_map._repr_html_()
    if form.validate_on_submit() and int(form.edit.data) == -1:
        if current_user.role == "Admin":
            column_names = [column.name for column in Architecture.__table__.columns if column.name != "id"]
            new_architecture = Architecture(
                **{column: getattr(form, column).data for column in column_names if hasattr(form, column)})
            db.session.add(new_architecture)
            new_log_16 = LogBook(original_id=new_architecture.id, title=new_architecture.title,
                                username=current_user.username)
            to_csv(current_user.username, new_architecture.title)
            db.session.add(new_log_16)
            db.session.commit()
            # print(form.portrait.data.filename)
            if form.image.data:
                save_uploaded_images(file=form.image.data, obj_id=new_architecture.id, field_name="architecture_id", model=Image)
                db.session.commit()
            to_csv_overwrite(current_user.username)
            return redirect(url_for("architecture_bp.architecture_info"))
        else:
            column_names = [column.name for column in TemporaryArchitecture.__table__.columns if column.name != "id"]
            temporary_architecture_edit = TemporaryArchitecture(
                **{column: getattr(form, column).data for column in column_names if hasattr(form, column)}, old_id = int(form.edit.data), username = current_user.username)
            db.session.add(temporary_architecture_edit)
            db.session.commit()
            if form.image.data:
                id_data = db.session.query(TemporaryArchitecture).filter_by(username = current_user.username).order_by(TemporaryArchitecture.id.desc()).first()
                save_uploaded_images(file=form.image.data, obj_id=id_data.id, field_name="temporary_architecture_id",
                                     model=TemporaryImage, form_data=form, temporary=True)
                db.session.commit()
                confirmation_email(id = temporary_architecture_edit.id)
            return redirect(url_for("architecture_bp.architecture_info"))
    return render_template('architecture_info.html', title = "Architecture", buildings_lst = buildings_lst , architecture_html =Markup(building_html), form_open = True, new_form = form )


@architecture_bp.route('/edit_architecture/<int:id>', methods = ['POST', 'GET'], endpoint = "edit_architecture")
@login_required
def edit_architecture(id):
    architecture_first = db.session.get(Architecture, id)
    form = ArchitectureForm()
    form_1 = ImageUploadForm()
    form_2 = ImageEditForm()
    images = db.session.query(Image).filter(Image.architecture_id == id).all() or []
    if request.method == "GET":
        form = ArchitectureForm(obj=architecture_first, data={"edit": architecture_first.id})
    if form.validate_on_submit():
        if current_user.role == "Admin":
            architecture_new_edit = db.session.get(Architecture, int(form.edit.data))
            form.populate_obj(architecture_new_edit)
            new_log_18 = LogBook(original_id=id, title=architecture_new_edit.title,
                                 username=current_user.username)
            to_csv(current_user.username, architecture_new_edit.title)
            db.session.add(new_log_18)
            if form.image.data:
                save_uploaded_images(file=form.image.data, obj_id=architecture_new_edit.id, field_name="architecture_id",
                                     model=Image)
            db.session.commit()
            to_csv_overwrite(current_user.username)
            return redirect(url_for('architecture_bp.architecture_info_detail', id=architecture_new_edit.id))
        else:
            column_names = [column.name for column in TemporaryArchitecture.__table__.columns if column.name != "id"]
            temporary_edit = TemporaryArchitecture(
                **{column: getattr(form, column).data for column in column_names if hasattr(form, column)}, old_id = int(form.edit.data), username = current_user.username)
            db.session.add(temporary_edit)
            db.session.commit()
            if form.image.data:
                id_data = db.session.query(TemporaryArchitecture).filter_by(username = current_user.username).order_by(TemporaryArchitecture.id.desc()).first()
                save_uploaded_images(file=form.image.data, obj_id=id_data.id, field_name="temporary_architecture_id", model=TemporaryImage, form_data=form, temporary=True)
            db.session.commit()
            confirmation_email(id = id)
            return redirect(url_for('architecture_bp.architecture_info_detail', id=architecture_first.id))
    return render_template("architecture_info_detail.html", id=architecture_first.id, form_open = True, building = architecture_first, new_form = form, new_form_1 = form_1, new_form_2 = form_2,title = "Architecture information", form_open_1 = False, form_open_2 = False, images = images)
    #return render_template("war_info.html", war = war, title = "Battle information")


@architecture_bp.route('/edit_architecture_users/<int:id>', methods = ['POST', 'GET'], endpoint = "edit_architecture_users")
@login_required
def edit_architecture_users(id):
    architecture_first = db.session.get(TemporaryArchitecture, id)
    form = ArchitectureForm()

    if request.method == "GET":
        form = ArchitectureForm(obj=architecture_first, data={"edit": architecture_first.id})
    if form.validate_on_submit():
        architecture_new_edit = db.session.get(TemporaryArchitecture, int(form.edit.data))
        form.populate_obj(architecture_new_edit)
        if form.image.data:
            save_uploaded_images(file=form.image.data, obj_id=architecture_new_edit.id, field_name="temporary_architecture_id",
                                 model=TemporaryImage, form_data=form, temporary=True)
        if architecture_first.status != "Pending":
            architecture_new_edit.status = "Pending"
            confirmation_email(id=architecture_first.id)
        db.session.commit()
        return redirect(url_for('architecture_bp.architecture_info_edit_user', id=architecture_first.id))
    return render_template("architecture_info_edit_user.html", building = architecture_first, new_form = form, form_open = True, title = "Editing requests")


@architecture_bp.route("/approve_architecture_edit/<int:id>", methods = ['GET', 'POST'], endpoint = "approve_architecture_edit")
@admin_only
def approve_architecture_edit(id):
    try:
        architecture_first = db.session.get(TemporaryArchitecture, id)
        new_architecture = db.session.get(Architecture, int(architecture_first.old_id))
        to_csv(current_user.username, new_architecture.title)
        column_names = [column.name for column in Architecture.__table__.columns if column.name not in ("id", "old_id")]
        for column in column_names:
            setattr(new_architecture, column, getattr(architecture_first, column))
        user = db.session.query(User).filter_by(username=architecture_first.username).first()
        new_log_20 = LogBook(original_id=id, title=new_architecture.title,
                             username=current_user.username)
        db.session.add(new_log_20)
        if architecture_first.temporary_images:
            approval_add_image(architecture_first, obj_id=new_architecture.id, field_name="architecture_id", model=Image)
        approval_email(user_email=user.email, emperor_title=new_architecture.title)
        db.session.delete(architecture_first)
        db.session.commit()
        to_csv_overwrite(current_user.username)
    except Exception as e:
        flash("Article no longer available due to version change!", "warning")
    return redirect(url_for('admin_bp.manage_edits'))


@architecture_bp.route("/approve_architecture_add/<int:id>", methods=['GET', 'POST'], endpoint = "approve_architecture_add")
@admin_only
def approve_architecture_add(id):
    add_architecture = db.session.get(TemporaryArchitecture, id)
    column_names = [column.name for column in Architecture.__table__.columns if column.name != "id"]
    new_architecture = Architecture(
        **{column: getattr(add_architecture, column) for column in column_names if hasattr(add_architecture, column)})
    to_csv(current_user.username, new_architecture.title)
    user = db.session.query(User).filter_by(username = add_architecture.username).first()
    db.session.add(new_architecture)
    db.session.commit()
    new_log_2200 = LogBook(original_id=new_architecture.id, title=new_architecture.title,
                         username=current_user.username)
    db.session.add(new_log_2200)
    if add_architecture.temporary_images:
        approval_add_image(add_architecture, obj_id=new_architecture.id, field_name="architecture_id", model=Image)
    approval_email(user_email=user.email, emperor_title=add_architecture.title)
    db.session.delete(add_architecture)
    db.session.commit()
    to_csv_overwrite(current_user.username)
    return redirect(url_for('admin_bp.manage_additions'))



@architecture_bp.route("/reject_architecture_add_edit/<int:id>", methods = ['GET', 'POST'], endpoint = "reject_architecture_add_edit")
@admin_only
def reject_architecture_add_edit(id):
    add_architecture = db.session.get(TemporaryArchitecture, id)
    add_architecture.status = "Reject"
    user = db.session.query(User).filter_by(username = add_architecture.username).first()
    rejection_email(user_email=user.email, emperor_title=add_architecture.title)
    db.session.commit()
    return redirect(request.referrer)


@architecture_bp.route("/admin_delete_architecture/<int:id>", methods = ['GET', 'POST'], endpoint = "admin_delete_architecture")
@admin_only
def admin_delete_architecture(id):
    delete_architecture_temporary = db.session.get(TemporaryArchitecture, id)
    if delete_architecture_temporary.temporary_images:
        delete_image_temporary = delete_architecture_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_architecture_temporary)
    db.session.commit()
    return redirect(request.referrer)


@architecture_bp.route("/manage_edits_additions_users/architecture_info_edit_user/<int:id>", methods = ['GET', 'POST'], endpoint = "architecture_info_edit_user")
@login_required
def architecture_info_edit_user(id):
    #war_first = db.session.get(TemporaryWar, id)
    architecture_first = db.session.get(TemporaryArchitecture, id)
    form = ArchitectureForm(obj=architecture_first)
    form.edit.data = architecture_first.id
    return render_template("architecture_info_edit_user.html",building = architecture_first, form_open = False, title="Architecture edit/addition information", new_form=form)

