
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
from app.new_file import db
from sqlalchemy import or_, and_
from app.mixed.version_control import to_csv_function_1, to_csv_function_overwrite, to_csv, to_csv_overwrite
from app.mixed.images_handling import save_uploaded_images, approval_add_image, gallery_upload, gallery_upload_addition
from flask import Blueprint

war_bp = Blueprint("war_bp", __name__)


@war_bp.route('/wars_selection', endpoint = "wars_selection")
def wars_selection():
    return render_template("wars-selection.html", title = "Type of Wars")


@war_bp.route('/wars_selection/foreign_wars', methods= ['GET', 'POST'], endpoint = "foreign_wars_1")
def foreign_wars_1():
    form = WarForm()
    wars_lst = db.session.query(War).filter(and_(War.war_type == "Foreign War")).all()
    war_map = folium.Map(location=[41.008333, 28.98], zoom_start=3)

    colors = cycle(['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
                    'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
                    'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray'])
    names = sorted({ war.war_name for war in wars_lst if war.war_name})
    war_colors = {name: next(colors) for name in names}
    cluster = MarkerCluster().add_to(war_map)

    for war in wars_lst:
        if war.latitude is not None and war.longitude is not None:
            color = war_colors.get(war.war_name, 'gray')
            folium.Marker(location= [war.latitude, war.longitude],
                          tooltip=war.title,
                          popup=folium.Popup(f"<b>{war.title}</b><br>{war.war_name}<br>{war.dates}", max_width=300),
                          icon=folium.Icon(color=color)
            ).add_to(cluster)
    war_html = war_map._repr_html_()

    return render_template('foreign_war_1.html', title = "Foreign Wars", wars_lst = wars_lst, war_html =Markup(war_html) , form_open = False, new_form = form)


@war_bp.route('/wars_selection/civil_wars', methods= ['GET', 'POST'], endpoint = "civil_wars")
def civil_wars():
    form = WarForm()
    wars_lst = db.session.query(War).filter(War.war_type == "Civil War").all()
    war_map = folium.Map(location=[41.008333, 28.98], zoom_start=3)

    colors = cycle(['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
                    'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
                    'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray'])
    names = sorted({war.war_name for war in wars_lst if war.war_name})
    war_colors = {name: next(colors) for name in names}
    cluster = MarkerCluster().add_to(war_map)

    for war in wars_lst:
        if war.latitude is not None and war.longitude is not None:
            color = war_colors.get(war.war_name, 'gray')
            folium.Marker(location=[war.latitude, war.longitude],
                          tooltip=war.title,
                          popup=folium.Popup(f"<b>{war.title}</b><br>{war.war_name}<br>{war.dates}", max_width=300),
                          icon=folium.Icon(color=color)
                          ).add_to(cluster)
    war_html = war_map._repr_html_()
    return render_template('civil_wars.html', title = "Civil Wars", wars_lst = wars_lst, war_html =Markup(war_html) , form_open = False, new_form = form)


@war_bp.route("/admin/manage_additions/add_info_war/<int:id>", methods = ['GET', 'POST'], endpoint = "add_info_war")
@admin_only
@login_required
def add_info_war(id):
    war_add = db.session.get(TemporaryWar, id)
    return render_template("edit_add_info_war.html", war = war_add, title = "Preview")


@war_bp.route("/manage_edits_additions_users/war_info_edit_user/<int:id>", methods = ['GET', 'POST'], endpoint = "war_info_edit_user")
@login_required
def war_info_edit_user(id):
    war_first = db.session.get(TemporaryWar, id)
    form = WarForm(obj=war_first)
    form.edit.data = war_first.id
    return render_template("war_info_edit_user.html",war = war_first, form_open = False, title="War edit/addition information", new_form=form)



@war_bp.route("/admin/manage_edits/edit_info_war/<int:id>", methods = ['GET', 'POST'], endpoint = "edit_info_war")
@admin_only
@login_required
def edit_info_war(id):
    war_edit = db.session.get(TemporaryWar, id)
    return render_template("edit_add_info_war.html", war = war_edit, title = "Preview")


@war_bp.route("/delete_wars_/<int:id>", methods = ['GET', 'POST'], endpoint = "delete_wars_")
@admin_only
def delete_wars_(id):
    delete_wars__ = db.session.get(War, id)
    to_csv(current_user.username, delete_wars__.title)
    if delete_wars__.war_type == "Civil War":
        db.session.delete(delete_wars__)
        if delete_wars__.images:
            delete_images_ = delete_wars__.images[0]
            db.session.delete(delete_images_)
        delete_log = LogBook(original_id=id, title=delete_wars__.title,
                             username=current_user.username)
        db.session.add(delete_log)
        db.session.commit()
        to_csv_overwrite(current_user.username)
        return redirect(url_for("war_bp.civil_wars"))
    elif delete_wars__.war_type == "Foreign War":
        db.session.delete(delete_wars__)
        if delete_wars__.images:
            delete_images_ = delete_wars__.images[0]
            db.session.delete(delete_images_)
        delete_log = LogBook(original_id=id, title=delete_wars__.title,
                             username=current_user.username)
        db.session.add(delete_log)
        db.session.commit()
        to_csv_overwrite(current_user.username)
        return redirect(url_for("war_bp.foreign_wars_1"))
    return redirect(request.referrer)


@war_bp.route("/wars_selection/war_info/<int:id>", methods=['GET','POST'], endpoint = "war_info_foreign_1")
def war_info_foreign_1(id):
    #m_e = db.session.query(Emperor).filter_by(dynasty = 'Macedonian').all()
    war_first = db.session.get(War, id)
    form = WarForm(obj=war_first)
    form.edit.data = war_first.id
    return render_template("war_info.html", war = war_first, title = "Battle information", new_form = form, form_open = False)


@war_bp.route("/add_new_war_1/<string:war_category>", methods = ['POST', 'GET'], endpoint = "add_new_war_1")
@login_required
def add_new_war_1(war_category):
    form = WarForm()
    if war_category == "foreign":
        war_type = "Foreign War"
        template = "foreign_war_1.html"
        redirect_ = "war_bp.foreign_wars_1"
        page_title = "Foreign War"
    else:
        war_type = "Civil War"
        template = "civil_wars.html"
        redirect_ = "war_bp.civil_wars"
        page_title = "Civil War"
    wars_lst = db.session.query(War).filter(War.war_type == war_type).all()
    war_map = folium.Map(location=[41.008333, 28.98], zoom_start=3)

    colors = cycle(['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
                    'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
                    'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray'])
    names = sorted({war.war_name for war in wars_lst if war.war_name})
    war_colors = {name: next(colors) for name in names}
    cluster = MarkerCluster().add_to(war_map)
    for war in wars_lst:
        if war.latitude is not None and war.longitude is not None:
            color = war_colors.get(war.war_name, 'gray')
            folium.Marker(location=[war.latitude, war.longitude],
                          tooltip=war.title,
                          popup=folium.Popup(f"<b>{war.title}</b><br>{war.war_name}<br>{war.dates}", max_width=300),
                          icon=folium.Icon(color=color)
                          ).add_to(cluster)
    war_html = war_map._repr_html_()
    if form.validate_on_submit() and int(form.edit.data) == -1:
        if current_user.role == "Admin":
            column_names = [column.name for column in War.__table__.columns if column.name != "id"]
            new_war = War(
                **{column: getattr(form, column).data for column in column_names if hasattr(form, column)})
            to_csv(current_user.username, new_war.title)
            db.session.add(new_war)
            db.session.commit()
            new_log_4 = LogBook(original_id=new_war.id, title=new_war.title, username=current_user.username)
            db.session.add(new_log_4)
            # print(form.portrait.data.filename)
            if form.image.data:
                save_uploaded_images(file=form.image.data, obj_id=new_war.id, field_name="war_id",
                                     model=Image)
                db.session.commit()
            to_csv_overwrite(current_user.username)
            return redirect(url_for(redirect_))
        else:
            column_names = [column.name for column in TemporaryWar.__table__.columns if column.name != "id"]
            temporary_war_edit = TemporaryWar(
                **{column: getattr(form, column).data for column in column_names if hasattr(form, column)}, old_id = int(form.edit.data), username = current_user.username)
            db.session.add(temporary_war_edit)
            db.session.commit()
            id_data = db.session.query(TemporaryWar).filter_by(username=current_user.username).order_by(
                TemporaryWar.id.desc()).first()
            if form.image.data:
                save_uploaded_images(file=form.image.data, obj_id=id_data.id, field_name="temporary_war_id",model=TemporaryImage, form_data=form, temporary=True)
                db.session.commit()
            confirmation_email(id = id_data.id)
            flash("Request successfully uploaded, please wait for approval", "success" )
            return redirect(url_for(redirect_))
    return render_template(template, title = page_title, wars_lst = wars_lst, war_html =Markup(war_html), form_open = True, new_form = form )


@war_bp.route('/edit_war/<int:id>', methods = ['POST', 'GET'], endpoint = "edit_war")
@login_required
def edit_war(id):
    war_first = db.session.get(War, id)
    form = WarForm()
    if request.method == "GET":
        form = WarForm(obj=war_first, data={"edit": war_first.id})
    if form.validate_on_submit():
        if current_user.role == "Admin":
            war_new_edit = db.session.get(War, int(form.edit.data))
            form.populate_obj(war_new_edit)
            new_log_6 = LogBook(original_id=war_new_edit.id, title=war_new_edit.title, username=current_user.username)
            to_csv(current_user.username, war_new_edit.title)
            db.session.add(new_log_6)
            if form.image.data:
                save_uploaded_images(file=form.image.data, obj_id=war_new_edit.id, field_name="war_id",model=Image)
            db.session.commit()
            to_csv_overwrite(current_user.username)
            return redirect(url_for('war_bp.war_info_foreign_1', id=war_first.id))
        else:
            column_names = [column.name for column in TemporaryWar.__table__.columns if column.name != "id"]
            temporary_edit = TemporaryWar(
                **{column: getattr(form, column).data for column in column_names if hasattr(form, column)},
                old_id=int(form.edit.data), username=current_user.username)
            db.session.add(temporary_edit)
            db.session.commit()
            id_data = db.session.query(TemporaryWar).filter_by(username=current_user.username).order_by(
                TemporaryWar.id.desc()).first()
            if form.image.data:
                save_uploaded_images(file=form.image.data, obj_id=id_data.id, field_name="temporary_war_id", model=TemporaryImage, form_data=form, temporary=True)
            db.session.commit()
            confirmation_email(id=id_data.id)
            flash("Request successfully uploaded, please wait for approval", "success" )
            return redirect(url_for('war_bp.war_info_foreign_1', id=war_first.id))
    war_first = db.session.get(War, id)
    return render_template("war_info.html", id=war_first.id, form_open = True, war = war_first, new_form = form, title = "Battle information")


@war_bp.route('/edit_wars_users/<int:id>', methods = ['POST', 'GET'], endpoint = "edit_wars_users")
@login_required
def edit_wars_users(id):
    war_first = db.session.get(TemporaryWar, id)
    form = WarForm()
    if request.method == "GET":
        form = WarForm(obj=war_first, data={"edit": war_first.id})
    if form.validate_on_submit():
        war_new_edit = db.session.get(TemporaryWar, int(form.edit.data))
        form.populate_obj(war_new_edit)
        if form.image.data:
            save_uploaded_images(file=form.image.data, obj_id=war_new_edit.id, field_name="temporary_war_id",
                                 model=TemporaryImage, form_data=form, temporary=True)
        db.session.commit()
        if war_first.status != "Pending":
            war_first.status = "Pending"
            confirmation_email(id=war_first.id)
        db.session.commit()
        return redirect(url_for('war_bp.war_info_edit_user', id=war_first.id))
    return render_template("war_info_edit_user.html", war = war_first, new_form = form, form_open = True, title = "Editing requests")


@war_bp.route("/approve_war_edit/<int:id>", methods = ['GET', 'POST'], endpoint = "approve_war_edit")
@admin_only
def approve_war_edit(id):
    try:
        war_first = db.session.get(TemporaryWar, id)
        new_war = db.session.get(War, int(war_first.old_id))
        to_csv(current_user.username, new_war.title)
        column_names = [column.name for column in War.__table__.columns if column.name not in ("id", "old_id")]
        for column in column_names:
            setattr(new_war, column, getattr(war_first, column))
        user = db.session.query(User).filter_by(username=war_first.username).first()
        new_log_8 = LogBook(original_id=id, title=new_war.title,
                            username=current_user.username)
        db.session.add(new_log_8)
        if war_first.temporary_images:
            approval_add_image(war_first, obj_id=new_war.id, field_name="war_id", model=Image)
        approval_email(user_email=user.email, emperor_title=new_war.title)
        db.session.delete(war_first)
        db.session.commit()
        to_csv_overwrite(current_user.username)
    except Exception as e:
        flash("Article no longer available due to version change!", "warning")
    return redirect(url_for('admin_bp.manage_edits'))


@war_bp.route("/approve_war_add/<int:id>", methods=['GET', 'POST'], endpoint = "approve_war_add")
@admin_only
def approve_war_add(id):
    add_war = db.session.get(TemporaryWar, id)
    column_names = [column.name for column in War.__table__.columns if column.name != "id"]
    new_war = War(**{column: getattr(add_war, column) for column in column_names if hasattr(add_war, column)})
    to_csv(current_user.username, new_war.title)
    user = db.session.query(User).filter_by(username = add_war.username).first()
    db.session.add(new_war)
    db.session.commit()
    new_log_1000 = LogBook(original_id=new_war.id, title=new_war.title,
                        username=current_user.username)
    db.session.add(new_log_1000)
    if add_war.temporary_images:
        approval_add_image(add_war, obj_id=new_war.id, field_name="war_id", model=Image)
    approval_email(user_email=user.email, emperor_title=new_war.title)
    db.session.delete(add_war)
    db.session.commit()
    to_csv_overwrite(current_user.username)
    return redirect(url_for('admin_bp.manage_additions'))


@war_bp.route("/reject_war_add_edit/<int:id>", methods = ['GET', 'POST'], endpoint = "reject_war_add_edit")
def reject_war_add_edit(id):
    add_war = db.session.get(TemporaryWar, id)
    add_war.status = "Reject"
    user = db.session.query(User).filter_by(username = add_war.username).first()
    rejection_email(user_email=user.email, emperor_title=add_war.title)
    db.session.commit()
    return redirect(request.referrer)


@war_bp.route("/admin_delete_war/<int:id>", methods = ['GET', 'POST'])
@admin_only
def admin_delete_war(id):
    delete_war_temporary = db.session.get(TemporaryWar, id)
    if delete_war_temporary.temporary_images:
        delete_image_temporary = delete_war_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_war_temporary)
    db.session.commit()
    return redirect(request.referrer)