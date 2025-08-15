from os import write
from flask import abort
from itertools import cycle
import uuid
from functools import wraps
import os
from random import randint

from folium.plugins import MarkerCluster
from markupsafe import Markup
from werkzeug.utils import secure_filename
from app import signer, TOKEN_MAX_AGE, verification_email, confirmation_email, approval_email, rejection_email, new_confirmation_email
from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory,session, jsonify
#from unicodedata import category
#from urllib3.connection import port_by_scheme
import folium
from app import app
from app.models import User, Emperor, \
    Verification, Invitation, Image, TemporaryEmperor, TemporaryImage, War, TemporaryWar, Architecture, TemporaryArchitecture, Literature, TemporaryLiterature, Artifact, TemporaryArtifact, LogBook, Deletion
from app.forms import ChooseForm, LoginForm, ChangePasswordForm, ChangeEmailForm, RegisterForm, RegisterEmail, \
    AdminCodeForm, InvitationCodeForm, AllEmperorForm, WarForm, ArchitectureForm, ImageEditForm, ImageUploadForm, LiteratureForm, ArtifactForm, DeleteForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app.new_file import db
from urllib.parse import urlsplit
from sqlalchemy import or_, and_
import csv
import io
import datetime
import random
import json
from sqlalchemy.exc import IntegrityError
#import google.generativeai as genai
def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != "Admin":
            return abort(403)
        return func(*args, **kwargs)
    return wrapper





@app.route("/logbook", methods=["GET", "POST"])
@login_required
def logbook():
    logbook = db.session.query(LogBook).all()
    return render_template('logbook.html', title = "Logbook", logbook =logbook)




@app.route("/")
def home():
    return render_template('home.html', title="Roman Empire")
@app.route("/dynasties")
def dynasties():
    return render_template('dynasties.html', title = "Dynasties")




@app.route("/dynasties/macedonians", methods=['GET','POST'])
def macedonians():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Macedonian').all()
    #query_email = db.session.query(Verification).filter_by(email=email_data).first()
    #macedonian_lst = db.session.scalars(m).all()
    #, form_open = False
    return render_template('macedonians.html', title = "Macedonian dynasty", macedonian_lst = macedonian_lst, form_open = False ,new_form = form, article_title = "Macedonian Dynasty (867-1056)")


@app.route("/dynasties/doukas", methods=['GET','POST'])
def doukas():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Doukas').all()
    #query_email = db.session.query(Verification).filter_by(email=email_data).first()
    #macedonian_lst = db.session.scalars(m).all()
    #, form_open = False
    return render_template('doukas.html', title = "Doukas dynasty", macedonian_lst = macedonian_lst, form_open = False ,new_form = form, article_title = "Doukas Dynasty (1059-1081)")




@app.route("/dynasties/komnenos", methods=['GET','POST'])
def komnenos():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Komnenos').all()
    #query_email = db.session.query(Verification).filter_by(email=email_data).first()
    #macedonian_lst = db.session.scalars(m).all()
    #, form_open = False
    return render_template('komnenos.html', title = "Komnenos dynasty", macedonian_lst = macedonian_lst, form_open = False ,new_form = form, article_title = "Komnenos Dynasty (1081-1185)")



@app.route("/dynasties/angelos", methods=['GET','POST'])
def angelos():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Angelos').all()
    #query_email = db.session.query(Verification).filter_by(email=email_data).first()
    #macedonian_lst = db.session.scalars(m).all()
    #, form_open = False
    return render_template('angelos.html', title = "Angelos dynasty", macedonian_lst = macedonian_lst, form_open = False ,new_form = form, article_title = "Angelos Dynasty (1185-1204)")




@app.route("/dynasties/palaiologos", methods=['GET','POST'])
def palaiologos():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Palaiologos').all()
    #query_email = db.session.query(Verification).filter_by(email=email_data).first()
    #macedonian_lst = db.session.scalars(m).all()
    #, form_open = False
    return render_template('palaiologos.html', title = "Palaiologos dynasty", macedonian_lst = macedonian_lst, form_open = False ,new_form = form, article_title = "Palaiologos Dynasty (1259-1453)")




@app.route('/art_selection')
def art_selection():
    return render_template("art_selection.html", title = "Roman Culture")


@app.route('/wars_selection')
def wars_selection():
    return render_template("wars-selection.html", title = "Type of Wars")



@app.route('/wars_selection/foreign_wars', methods= ['GET', 'POST'])
def foreign_wars_1():
    form = WarForm()
    foreign_wars_lst = db.session.query(War).filter(and_(War.war_type == "Foreign War")).all()
    war_map = folium.Map(location=[41.008333, 28.98], zoom_start=3)

    colors = cycle(['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
                    'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
                    'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray'])
    names = sorted({ war.war_name for war in foreign_wars_lst if war.war_name})
    war_colors = {name: next(colors) for name in names}
    cluster = MarkerCluster().add_to(war_map)

    for war in foreign_wars_lst:
        if war.latitude is not None and war.longitude is not None:
            color = war_colors.get(war.war_name, 'gray')
            folium.Marker(location= [war.latitude, war.longitude],
                          tooltip=war.title,
                          popup=folium.Popup(f"<b>{war.title}</b><br>{war.war_name}<br>{war.dates}", max_width=300),
                          icon=folium.Icon(color=color)
            ).add_to(cluster)
    war_html = war_map._repr_html_()

    return render_template('foreign_war_1.html', title = "Foreign Wars", foreign_wars_lst = foreign_wars_lst, war_html =Markup(war_html) , form_open = False, new_form = form)




@app.route('/wars_selection/civil_wars', methods= ['GET', 'POST'])
def civil_wars():
    form = WarForm()
    civil_wars_lst = db.session.query(War).filter(War.war_type == "Civil War").all()
    war_map = folium.Map(location=[41.008333, 28.98], zoom_start=3)

    colors = cycle(['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
                    'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
                    'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray'])
    names = sorted({war.war_name for war in civil_wars_lst if war.war_name})
    war_colors = {name: next(colors) for name in names}
    cluster = MarkerCluster().add_to(war_map)

    for war in civil_wars_lst:
        if war.latitude is not None and war.longitude is not None:
            color = war_colors.get(war.war_name, 'gray')
            folium.Marker(location=[war.latitude, war.longitude],
                          tooltip=war.title,
                          popup=folium.Popup(f"<b>{war.title}</b><br>{war.war_name}<br>{war.dates}", max_width=300),
                          icon=folium.Icon(color=color)
                          ).add_to(cluster)
    war_html = war_map._repr_html_()
    return render_template('civil_wars.html', title = "Civil Wars", foreign_wars_lst = civil_wars_lst, war_html =Markup(war_html) , form_open = False, new_form = form)



@app.route("/admin/manage_additions", methods = ['GET', 'POST'])
@admin_only
@login_required
def manage_additions():
    add_list = db.session.query(TemporaryEmperor).filter(TemporaryEmperor.old_id == -1).all()
    add_list_1 =  db.session.query(TemporaryWar).filter(TemporaryWar.old_id == -1).all()
    add_list_2 = db.session.query(TemporaryArchitecture).filter(TemporaryArchitecture.old_id ==-1).all()
    add_list_3 = db.session.query(TemporaryLiterature).filter(TemporaryLiterature.old_id == -1).all()
    add_list_4 = db.session.query(TemporaryArtifact).filter(TemporaryArtifact.old_id == -1).all()
    return render_template('manage_additions.html', title = "Manage additions", add_list = add_list, add_list_1 = add_list_1, add_list_2 = add_list_2, add_list_3 = add_list_3, add_list_4 = add_list_4)


@app.route("/admin/manage_additions/add_info_emperor/<int:id>", methods = ['GET', 'POST'])
@admin_only
@login_required
def add_info_emperor(id):
    emperor_add = db.session.get(TemporaryEmperor, id)
    return render_template("add_info_emperor.html", emperor_add = emperor_add, title = "Preview")



@app.route("/admin/manage_additions/add_info_war/<int:id>", methods = ['GET', 'POST'])
@admin_only
@login_required
def add_info_war(id):
    war_add = db.session.get(TemporaryWar, id)
    return render_template("edit_add_info_war.html", war = war_add, title = "Preview")




@app.route("/approve_emperor_add/<int:id>", methods = ['GET', 'POST'])
@admin_only
def approve_emperor_add(id):
    add_emperor = db.session.get(TemporaryEmperor, id)
    new_emperor = Emperor(title=add_emperor.title, in_greek=add_emperor.in_greek, birth=add_emperor.birth,
                          death=add_emperor.death, reign=add_emperor.reign, life=add_emperor.life,
                          dynasty=add_emperor.dynasty, reign_start = add_emperor.reign_start, references = add_emperor.references, ascent_to_power = add_emperor.ascent_to_power)
    user = db.session.query(User).filter_by(username = add_emperor.username).first()
    db.session.add(new_emperor)
    db.session.commit()
    new_log_12 = LogBook(original_id=new_emperor.id, title=new_emperor.title,
                         username=current_user.username)
    db.session.add(new_log_12)
    if add_emperor.temporary_images:
        file_name = secure_filename(add_emperor.temporary_images[0].filename)
        photo = Image(filename = file_name, url = f"/static/images/uploaded_photos/{file_name}", emperor_id = new_emperor.id)
        db.session.add(photo)
        db.session.commit()
        new_log_13 = LogBook(original_id=photo.id, title=file_name,
                             username=current_user.username)
        db.session.add(new_log_13)
        db.session.delete(add_emperor.temporary_images[0])
    approval_email(user_email=user.email, emperor_title=new_emperor.title)
    db.session.delete(add_emperor)
    db.session.commit()
    return redirect(url_for('manage_additions'))

@app.route("/reject_emperor_add/<int:id>", methods = ['GET', 'POST'])
def reject_emperor_add(id):
    add_emperor = db.session.get(TemporaryEmperor, id)
    add_emperor.status = "Reject"
    user = db.session.query(User).filter_by(username = add_emperor.username).first()
    rejection_email(user_email=user.email, emperor_title=add_emperor.title)
    db.session.commit()
    return redirect(url_for('manage_additions'))





@app.route("/admin/manage_edits_additions_users", methods = ['GET', 'POST'])
@login_required
def manage_edits_additions_users():
    total_list = db.session.query(TemporaryEmperor).all()
    total_list_1 = db.session.query(TemporaryWar).all()
    total_list_2 = db.session.query(TemporaryArchitecture).all()
    total_list_3 = db.session.query(TemporaryLiterature).all()
    total_list_4 = db.session.query(TemporaryArtifact).all()
    return render_template('manage_edits_additions_users.html', title = "Manage edits and additions", total_list = total_list, total_list_1 = total_list_1, total_list_2 = total_list_2, total_list_3 = total_list_3, total_list_4 = total_list_4)



@app.route("/admin/manage_edits_additions_users/war_info_edit_user/<int:id>", methods = ['GET', 'POST'])
@login_required
def war_info_edit_user(id):
    war_first = db.session.get(TemporaryWar, id)
    form = WarForm()
    form.edit.data = war_first.id
    form.title.data = war_first.title
    form.start_year.data = war_first.start_year
    form.dates.data = war_first.dates
    form.location.data = war_first.location
    form.longitude.data = war_first.longitude
    form.latitude.data = war_first.latitude
    form.roman_commanders.data = war_first.roman_commanders
    form.enemy_commanders.data = war_first.enemy_commanders
    form.roman_strength.data = war_first.roman_strength
    form.enemy_strength.data = war_first.enemy_strength
    form.roman_loss.data = war_first.roman_loss
    form.enemy_loss.data = war_first.enemy_loss
    form.dynasty.data = war_first.dynasty
    form.war_name.data = war_first.war_name
    form.war_type.data = war_first.war_type
    form.description.data = war_first.description
    form.references.data = war_first.references
    form.result.data = war_first.result

    return render_template("war_info_edit_user.html",war = war_first, form_open = False, title="War edit/addition information", new_form=form)




@app.route("/admin/manage_edits_additions_users/<int:id>", methods = ['GET', 'POST'])
@login_required
def user_editing(id):
    emperors_edit_additions = db.session.get(TemporaryEmperor, id)
    form = AllEmperorForm()
    form.edit.data = emperors_edit_additions.id
    form.title.data = emperors_edit_additions.title
    form.in_greek.data = emperors_edit_additions.in_greek
    form.birth.data = emperors_edit_additions.birth
    form.reign_start.data = emperors_edit_additions.reign_start
    form.ascent_to_power.data = emperors_edit_additions.ascent_to_power
    form.references.data = emperors_edit_additions.references
    form.death.data = emperors_edit_additions.death
    form.reign.data = emperors_edit_additions.reign
    form.life.data = emperors_edit_additions.life
    form.dynasty.data = emperors_edit_additions.dynasty
    return render_template("user_info.html", emperors_edit_additions=emperors_edit_additions, form_open = False, title="Macedonian dynasty", new_form=form)


@app.route('/edit_emperor_users/<int:id>', methods = ['POST', 'GET'])
@login_required
def edit_emperor_users(id):
    emperor_first_users = db.session.get(TemporaryEmperor, id)
    form = AllEmperorForm()
    if request.method == "GET":
        form.edit.data = emperor_first_users.id
        form.title.data = emperor_first_users.title
        form.reign_start.data = emperor_first_users.reign_start
        form.ascent_to_power.data = emperor_first_users.ascent_to_power
        form.references.data = emperor_first_users.references
        form.in_greek.data = emperor_first_users.in_greek
        form.birth.data = emperor_first_users.birth
        form.death.data = emperor_first_users.death
        form.reign.data = emperor_first_users.reign
        form.life.data = emperor_first_users.life
        form.dynasty.data = emperor_first_users.dynasty

    if form.validate_on_submit():
            emperor_new_edit_users = db.session.get(TemporaryEmperor, int(form.edit.data))
            emperor_new_edit_users.title = form.title.data
            emperor_new_edit_users.in_greek = form.in_greek.data
            emperor_new_edit_users.birth = form.birth.data
            emperor_new_edit_users.ascent_to_power = form.ascent_to_power.data
            emperor_new_edit_users.reign_start = form.reign_start.data
            emperor_new_edit_users.references = form.references.data
            emperor_new_edit_users.death = form.death.data
            emperor_new_edit_users.reign = form.reign.data
            emperor_new_edit_users.life = form.life.data
            emperor_new_edit_users.dynasty = form.dynasty.data
            if form.portrait.data:
                file_name = secure_filename(form.portrait.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.portrait.data.save(new_path_for_uploading)
                photo = db.session.query(TemporaryImage).filter_by(temporary_emperor_id=emperor_new_edit_users.id).order_by(
                    TemporaryImage.id.asc()).first()
                if not photo:
                    photo = TemporaryImage(temporary_emperor_id =emperor_new_edit_users.id)
                    db.session.add(photo)
                photo.filename = file_name
                photo.url = url_for('static', filename=f"images/uploaded_photos/{file_name}")
            if emperor_first_users.status != "Pending":
                emperor_new_edit_users.status = "Pending"
                confirmation_email(id=emperor_first_users.id)
            db.session.commit()
            return redirect(url_for('user_editing', id=emperor_first_users.id))
    return render_template("user_info.html", emperors_edit_additions = emperor_first_users, new_form = form, form_open = True, title = "Editing requests")












@app.route("/admin/manage_edits", methods = ['GET', 'POST'])
@admin_only
@login_required
def manage_edits():
    edit_list = db.session.query(TemporaryEmperor).filter(TemporaryEmperor.old_id != -1).all()
    edit_list_1 = db.session.query(TemporaryWar).filter(TemporaryWar.old_id !=-1).all()
    edit_list_2 = db.session.query(TemporaryArchitecture).filter(TemporaryArchitecture.old_id != -1).all()
    edit_list_3 = db.session.query(TemporaryLiterature).filter(TemporaryLiterature.old_id != -1).all()
    edit_list_4 = db.session.query(TemporaryArtifact).filter(TemporaryArtifact.old_id != -1).all()
    return render_template('manage_edits.html', title = "Manage edits", edit_list = edit_list, edit_list_1 = edit_list_1, edit_list_2 = edit_list_2, edit_list_3 = edit_list_3, edit_list_4 = edit_list_4)

@app.route("/admin/manage_edits/edit_info_emperor/<int:id>", methods = ['GET', 'POST'])
@admin_only
@login_required
def edit_info_emperor(id):
    emperor_edit = db.session.get(TemporaryEmperor, id)
    return render_template("edit_info_emperor.html", emperor_edit = emperor_edit, title = "Preview")


@app.route("/admin/manage_edits/edit_info_war/<int:id>", methods = ['GET', 'POST'])
@admin_only
@login_required
def edit_info_war(id):
    war_edit = db.session.get(TemporaryWar, id)
    return render_template("edit_add_info_war.html", war = war_edit, title = "Preview")


@app.route("/admin/manage_edits/edit_info_architecture/<int:id>", methods = ['GET', 'POST'])
@admin_only
@login_required
def edit_info_architecture(id):
    architecture_edit = db.session.get(TemporaryArchitecture, id)
    return render_template("edit_add_info_architecture.html", building = architecture_edit, title = "Preview")



@app.route("/admin/manage_additions/add_info_architecture/<int:id>", methods = ['GET', 'POST'])
@admin_only
@login_required
def add_info_architecture(id):
    architecture_add = db.session.get(TemporaryArchitecture, id)
    return render_template("edit_add_info_architecture.html", building = architecture_add, title = "Preview")





@app.route("/admin/manage_additions/edit_info_literature/<int:id>", methods = ['GET', 'POST'])
@admin_only
@login_required
def edit_info_literature(id):
    literature_edit = db.session.get(TemporaryLiterature, id)
    return render_template("edit_add_info_literature.html", book = literature_edit , title = "Preview")



@app.route("/admin/manage_additions/add_info_literature/<int:id>", methods = ['GET', 'POST'])
@admin_only
@login_required
def add_info_literature(id):
    literature_add = db.session.get(TemporaryLiterature, id)
    return render_template("edit_add_info_literature.html", book = literature_add, title = "Preview")






@app.route("/admin/manage_additions/edit_info_artifact/<int:id>", methods = ['GET', 'POST'])
@admin_only
@login_required
def edit_info_artifact(id):
    artifact_edit = db.session.get(TemporaryArtifact, id)
    return render_template("edit_add_info_artifact.html", artifact = artifact_edit , title = "Preview")



@app.route("/admin/manage_additions/add_info_artifact/<int:id>", methods = ['GET', 'POST'])
@admin_only
@login_required
def add_info_artifact(id):
    artifact_add = db.session.get(TemporaryArtifact, id)
    return render_template("edit_add_info_artifact.html", artifact = artifact_add, title = "Preview")








@app.route("/approve_emperor_edit/<int:id>", methods = ['GET', 'POST'])
@admin_only
def approve_emperor_edit(id):
    edit_emperor = db.session.get(TemporaryEmperor, id)
    emperor_new_edit = db.session.get(Emperor, int(edit_emperor.old_id))
    emperor_new_edit.title = edit_emperor.title
    emperor_new_edit.ascent_to_power = edit_emperor.ascent_to_power
    emperor_new_edit.reign_start = edit_emperor.reign_start
    emperor_new_edit.references = edit_emperor.references
    emperor_new_edit.in_greek = edit_emperor.in_greek
    emperor_new_edit.birth = edit_emperor.birth
    emperor_new_edit.death = edit_emperor.death
    emperor_new_edit.reign = edit_emperor.reign
    emperor_new_edit.life = edit_emperor.life
    emperor_new_edit.dynasty = edit_emperor.dynasty
    user = db.session.query(User).filter_by(username = edit_emperor.username).first()
    new_log_14 = LogBook(original_id=emperor_new_edit.id, title=emperor_new_edit.title,
                         username=current_user.username)
    db.session.add(new_log_14)
    if edit_emperor.temporary_images:
        photo = db.session.query(Image).filter_by(emperor_id=emperor_new_edit.id).order_by(Image.id.asc()).first()
        if photo:
            file_name = secure_filename(edit_emperor.temporary_images[0].filename)
            photo.filename = file_name
            photo.url = f"/static/images/uploaded_photos/{file_name}"
            photo.emperor_id = emperor_new_edit.id
            new_log_15 = LogBook(original_id=photo.id, title=file_name,
                                 username=current_user.username)
            db.session.add(new_log_15)
            db.session.delete(edit_emperor.temporary_images[0])
        else:
            file_name = secure_filename(edit_emperor.temporary_images[0].filename)
            photo = Image(filename = file_name, url = f"/static/images/uploaded_photos/{file_name}", emperor_id = emperor_new_edit.id)
            db.session.add(photo)
            new_log_15 = LogBook(original_id=photo.id, title=file_name,
                                 username=current_user.username)
            db.session.add(new_log_15)
            db.session.delete(edit_emperor.temporary_images[0])
    approval_email(user_email=user.email, emperor_title=edit_emperor.title)
    db.session.delete(edit_emperor)
    db.session.commit()
    return redirect(url_for('manage_edits'))

@app.route("/reject_emperor_edit/<int:id>", methods = ['GET', 'POST'])
def reject_emperor_edit(id):
    edit_emperor = db.session.get(TemporaryEmperor, id)
    edit_emperor.status = "Reject"
    user = db.session.query(User).filter_by(username = edit_emperor.username).first()
    rejection_email(user_email=user.email, emperor_title=edit_emperor.title)
    db.session.commit()
    return redirect(url_for('manage_edits'))


@app.route("/admin_delete_emperor/<int:id>", methods = ['GET', 'POST'])
def admin_delete_emperor(id):
    delete_emperor_temporary = db.session.get(TemporaryEmperor, id)
    if delete_emperor_temporary.temporary_images:
        delete_image_temporary = delete_emperor_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_emperor_temporary)
    db.session.commit()
    return redirect(url_for('manage_edits'))

@app.route("/delete_emperors_/<int:id>", methods = ['GET', 'POST'])
def delete_emperors_(id):
    delete_emperors_ = db.session.get(Emperor, id)
    if delete_emperors_.images:
        delete_images_ = delete_emperors_.images[0]
        db.session.delete(delete_images_)
    db.session.delete(delete_emperors_)
    db.session.commit()
    return redirect(url_for("macedonians"))





@app.route("/wars_selection/foreign_wars/war_info_foreign_1/<int:id>", methods=['GET','POST'])
def war_info_foreign_1(id):
    #m_e = db.session.query(Emperor).filter_by(dynasty = 'Macedonian').all()
    form = WarForm()
    war_first = db.session.get(War, id)
    form.edit.data = war_first.id
    form.title.data = war_first.title
    form.start_year.data = war_first.start_year
    form.dates.data = war_first.dates
    form.location.data = war_first.location
    form.longitude.data = war_first.longitude
    form.latitude.data = war_first.latitude
    form.roman_commanders.data = war_first.roman_commanders
    form.enemy_commanders.data = war_first.enemy_commanders
    form.roman_strength.data = war_first.roman_strength
    form.enemy_strength.data = war_first.enemy_strength
    form.roman_loss.data = war_first.roman_loss
    form.enemy_loss.data = war_first.enemy_loss
    form.dynasty.data = war_first.dynasty
    form.war_name.data = war_first.war_name
    form.war_type.data = war_first.war_type
    form.description.data = war_first.description
    form.references.data = war_first.references
    form.result.data = war_first.result
    return render_template("war_info.html", war = war_first, title = "Battle information", new_form = form, form_open = False)




@app.route("/dynasties/macedonians/<int:id>", methods=['GET','POST'])
def macedonian_emperors(id):
    #m_e = db.session.query(Emperor).filter_by(dynasty = 'Macedonian').all()
    m_e = db.session.get(Emperor, id)
    form = AllEmperorForm()
    form.edit.data = m_e.id
    form.references.data = m_e.references
    form.title.data = m_e.title
    form.in_greek.data = m_e.in_greek
    form.birth.data = m_e.birth
    form.death.data = m_e.death
    form.reign_start.data = m_e.reign_start
    form.ascent_to_power.data = m_e.ascent_to_power
    form.reign.data = m_e.reign
    form.life.data = m_e.life
    form.dynasty.data = m_e.dynasty
    if m_e.dynasty == "Macedonian":
        return render_template("macedonian_emperors.html", m_e=m_e, form_open=False, title="Macedonian dynasty",new_form=form)
    elif m_e.dynasty == "Doukas":
        return render_template("macedonian_emperors.html", m_e=m_e, form_open=False, title="Doukas dynasty",new_form=form)
    elif m_e.dynasty == "Angelos":
        return render_template("macedonian_emperors.html", m_e=m_e, form_open=False, title="Angelos dynasty",
                               new_form=form)
    elif m_e.dynasty == "Komnenos":
        return render_template("macedonian_emperors.html", m_e=m_e, form_open=False, title="Komnenos dynasty",
                               new_form=form)
    elif m_e.dynasty == "Palaiologos":
        return render_template("macedonian_emperors.html", m_e=m_e, form_open=False, title="Palaiologos dynasty",
                               new_form=form)
    else:
        return render_template(request.referrer)


@app.route("/account")
@login_required
def account():
    form = ChooseForm()
    delete_form = DeleteForm()
    invitation = db.session.query(Invitation).filter_by(user_id = current_user.id).order_by(Invitation.id.desc()).first()
    choose_form = ChooseForm()
    new_form = AdminCodeForm()
    return render_template('account.html', title="Account", choose_form = choose_form, form = form, new_form = new_form, invitation = invitation, delete_form = delete_form)


@app.route("/register_emails_", methods = ['GET', 'POST'])
def register_emails_():
    form = RegisterEmail()
    if form.validate_on_submit():
        email_data = form.email.data.strip().lower()
        success = verification_email(email_data)
        if success:
            flash("Check your inbox for the verification code, the code is valid for ten minutes.", "success")
            return redirect(url_for('register_verify'))
        else:
            flash("This email is already registered", "warning")
            return redirect(url_for('register_emails_'))
    return render_template('register_form.html', title = "Register", form = form)


@app.route("/account/change_to_admin", methods = ['POST'])
def change_to_admin():
    form = AdminCodeForm()
    u = db.session.get(User, current_user.id)
    t = db.session.query(Invitation).filter_by(user_id = current_user.id).order_by(Invitation.id.desc()).first()
    if form.validate_on_submit() :
        if form.code.data == t.code and u.role != "Admin":
            u = db.session.get(User, current_user.id)
            u.role = "Admin"
            flash("Role changed to admin", "success")
            db.session.delete(t)
            db.session.commit()
            return redirect(url_for('account'))
        elif u.role == "Admin":
            flash("You are already an admin", "warning")
            return redirect(url_for('account'))
        elif form.code.data != t.code:
            flash("Code is not correct", "danger")
            return redirect(url_for('account'))

    return render_template("account.html", new_form = form, title = "Account")

@app.route("/add_new_emperor", methods = ['POST'])
@login_required
def add_new_emperor():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Macedonian').all()
    if form.validate_on_submit() and int(form.edit.data) == -1:
        if current_user.role == "Admin" :
            new_emperor = Emperor(title=form.title.data, in_greek=form.in_greek.data, birth=form.birth.data,
                                  death=form.death.data, reign=form.reign.data, life=form.life.data,
                                  dynasty=form.dynasty.data, reign_start = form.reign_start.data, references = form.references.data, ascent_to_power = form.ascent_to_power.data)
            db.session.add(new_emperor)
            if "test" not in form.title.data:
                db.session.commit()
                id_data = db.session.query(Image).first()
                new_log_300000 = LogBook(original_id=new_emperor.id, title=new_emperor.title,
                                         username=current_user.username)
                db.session.add(new_log_300000)
                db.session.commit()
            # print(form.portrait.data.filename)
            if form.portrait.data and "test" not in form.title.data:
                file_name = secure_filename(form.portrait.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                print(path_for_uploading)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.portrait.data.save(new_path_for_uploading)
                new_emperor_portrait = Image(filename=file_name,
                                             url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                             emperor_id=new_emperor.id)
                db.session.add(new_emperor_portrait)
                db.session.commit()
                id_data = db.session.query(Image).filter(Image.emperor_id.isnot(None)).order_by(Image.id.desc()).first()
                new_log_1000000 = LogBook(original_id = new_emperor_portrait.id, title = file_name, username = current_user.username)
                db.session.add(new_log_1000000)
                db.session.commit()
            return redirect(url_for("macedonians"))

        elif current_user.role != "Admin" and "test" not in form.title.data:
            temporary_edit = TemporaryEmperor(username=current_user.username, old_id=int(form.edit.data),
                                              title=form.title.data, in_greek=form.in_greek.data, birth=form.birth.data,
                                              death=form.death.data, reign=form.reign.data, life=form.life.data,
                                              dynasty=form.dynasty.data, reign_start = form.reign_start.data, references = form.references.data, ascent_to_power = form.ascent_to_power.data)

            db.session.add(temporary_edit)
            db.session.commit()
            if form.portrait.data:
                file_name = secure_filename(form.portrait.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.portrait.data.save(new_path_for_uploading)
                id_data = db.session.query(TemporaryEmperor).filter_by(username = current_user.username).order_by(TemporaryEmperor.id.desc()).first()
                photo = TemporaryImage(username=current_user.username, old_id=int(form.edit.data), filename=file_name,
                                       url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                       temporary_emperor_id=id_data.id)
                db.session.add(photo)
                db.session.commit()
                confirmation_email(id=temporary_edit.id)
                return redirect(url_for("macedonians"))

        else:
            return redirect(url_for("macedonians"))
    return render_template('macedonians.html', title = "Macedonian dynasty", macedonian_lst = macedonian_lst, new_form = form, form_open = True, article_title = "Macedonian Dynasty (867-1056)")


#add_emperor


@app.route("/add_new_emperor_1", methods = ['POST'])
@login_required
def add_new_emperor_1():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Doukas').all()
    if form.validate_on_submit() and int(form.edit.data) == -1:
        if current_user.role == "Admin":
            new_emperor = Emperor(title=form.title.data, in_greek=form.in_greek.data, birth=form.birth.data,
                                  death=form.death.data, reign=form.reign.data, life=form.life.data,
                                  dynasty=form.dynasty.data, reign_start = form.reign_start.data, references = form.references.data, ascent_to_power = form.ascent_to_power.data)
            db.session.add(new_emperor)
            db.session.commit()
            new_log_104 = LogBook(original_id=new_emperor.id, title=new_emperor.title, username=current_user.username)
            db.session.add(new_log_104)
            db.session.commit()
            # print(form.portrait.data.filename)
            if form.portrait.data:
                file_name = secure_filename(form.portrait.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                print(path_for_uploading)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.portrait.data.save(new_path_for_uploading)
                new_emperor_portrait = Image(filename=file_name,
                                             url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                             emperor_id=new_emperor.id)
                db.session.add(new_emperor_portrait)
                db.session.commit()
                new_log_103 = LogBook(original_id = new_emperor_portrait.id, title = file_name, username = current_user.username)
                db.session.add(new_log_103)
                db.session.commit()
            return redirect(url_for("doukas"))
        else:
            temporary_edit = TemporaryEmperor(username=current_user.username, old_id=int(form.edit.data),
                                              title=form.title.data, in_greek=form.in_greek.data, birth=form.birth.data,
                                              death=form.death.data, reign=form.reign.data, life=form.life.data,
                                              dynasty=form.dynasty.data, reign_start = form.reign_start.data, references = form.references.data, ascent_to_power = form.ascent_to_power.data)

            db.session.add(temporary_edit)
            db.session.commit()
            if form.portrait.data:
                file_name = secure_filename(form.portrait.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.portrait.data.save(new_path_for_uploading)
                id_data = db.session.query(TemporaryEmperor).filter_by(username = current_user.username).order_by(TemporaryEmperor.id.desc()).first()
                photo = TemporaryImage(username=current_user.username, old_id=int(form.edit.data), filename=file_name,
                                       url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                       temporary_emperor_id=id_data.id)
                db.session.add(photo)
                db.session.commit()
                confirmation_email(id=temporary_edit.id)
            return redirect(url_for("doukas"))
    return render_template('doukas.html', title = "Doukas dynasty", macedonian_lst = macedonian_lst, new_form = form, form_open = True, article_title = "Doukas dynasty (1059-1081)")




@app.route("/add_new_emperor_2", methods = ['POST'])
@login_required
def add_new_emperor_2():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Komnenos').all()
    if form.validate_on_submit() and int(form.edit.data) == -1:
        if current_user.role == "Admin":
            new_emperor = Emperor(title=form.title.data, in_greek=form.in_greek.data, birth=form.birth.data,
                                  death=form.death.data, reign=form.reign.data, life=form.life.data,
                                  dynasty=form.dynasty.data, reign_start = form.reign_start.data, references = form.references.data, ascent_to_power = form.ascent_to_power.data)
            db.session.add(new_emperor)
            db.session.commit()
            new_log_102 = LogBook(original_id=new_emperor.id, title=new_emperor.title, username=current_user.username)
            db.session.add(new_log_102)
            db.session.commit()

            # print(form.portrait.data.filename)
            if form.portrait.data:
                file_name = secure_filename(form.portrait.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                print(path_for_uploading)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.portrait.data.save(new_path_for_uploading)
                new_emperor_portrait = Image(filename=file_name,
                                             url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                             emperor_id=new_emperor.id)
                db.session.add(new_emperor_portrait)
                db.session.commit()
                new_log_101 = LogBook(original_id = new_emperor_portrait.id, title = file_name, username = current_user.username)
                db.session.add(new_log_101)
                db.session.commit()
            return redirect(url_for("komnenos"))
        else:
            temporary_edit = TemporaryEmperor(username=current_user.username, old_id=int(form.edit.data),
                                              title=form.title.data, in_greek=form.in_greek.data, birth=form.birth.data,
                                              death=form.death.data, reign=form.reign.data, life=form.life.data,
                                              dynasty=form.dynasty.data, reign_start = form.reign_start.data, references = form.references.data, ascent_to_power = form.ascent_to_power.data)

            db.session.add(temporary_edit)
            db.session.commit()
            if form.portrait.data:
                file_name = secure_filename(form.portrait.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.portrait.data.save(new_path_for_uploading)
                id_data = db.session.query(TemporaryEmperor).filter_by(username = current_user.username).order_by(TemporaryEmperor.id.desc()).first()
                photo = TemporaryImage(username=current_user.username, old_id=int(form.edit.data), filename=file_name,
                                       url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                       temporary_emperor_id=id_data.id)
                db.session.add(photo)
                db.session.commit()
                confirmation_email(id=temporary_edit.id)
            return redirect(url_for("komnenos"))
    return render_template('komnenos.html', title = "Komnenos dynasty", macedonian_lst = macedonian_lst, new_form = form, form_open = True, article_title = "Homnenos dynasty (1081-1185)")

@app.route("/account_deletion_code", methods = ['GET','POST'])
def account_deletion_code():
    code = randint(10**8, 10**9-1)
    flash(f"Code for account deletion is {code}", "warning")
    code_1 = Deletion(code = code, user_id = current_user.id)
    db.session.add(code_1)
    db.session.commit()
    return redirect(url_for('account'))

@app.route("/account_deletion", methods = ['GET','POST'])
def account_deletion():
    delete_form = DeleteForm()
    user_id = current_user.id
    code_required = db.session.query(Deletion).filter(Deletion.user_id == user_id).order_by(Deletion.id.desc()).first()
    if code_required:
        if delete_form.validate_on_submit() and int(delete_form.number.data) == int(code_required.code):
            user_for_deletion = db.session.get(User, int(current_user.id))
            codes = db.session.query(Deletion).filter(Deletion.user_id == user_id).all()
            db.session.delete(user_for_deletion)
            for code in codes:
                db.session.delete(code)
            db.session.commit()
            return redirect(url_for('home'))
    form = ChooseForm()
    invitation = db.session.query(Invitation).filter_by(user_id=current_user.id).order_by(Invitation.id.desc()).first()
    choose_form = ChooseForm()
    new_form = AdminCodeForm()
    return render_template('account.html', title="Account", choose_form=choose_form, form=form, new_form=new_form, delete_form = delete_form,
                           invitation=invitation)




@app.route("/add_new_emperor_3", methods = ['POST'])
@login_required
def add_new_emperor_3():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Angelos').all()
    if form.validate_on_submit() and int(form.edit.data) == -1:
        if current_user.role == "Admin":
            new_emperor = Emperor(title=form.title.data, in_greek=form.in_greek.data, birth=form.birth.data,
                                  death=form.death.data, reign=form.reign.data, life=form.life.data,
                                  dynasty=form.dynasty.data, reign_start = form.reign_start.data, references = form.references.data, ascent_to_power = form.ascent_to_power.data)
            db.session.add(new_emperor)
            #db.session.commit()
            new_log = LogBook(original_id=new_emperor.id, title=new_emperor.title, username=current_user.username)
            db.session.add(new_log)
            db.session.commit()
            # print(form.portrait.data.filename)
            if form.portrait.data:
                file_name = secure_filename(form.portrait.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                print(path_for_uploading)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.portrait.data.save(new_path_for_uploading)
                new_emperor_portrait = Image(filename=file_name,
                                             url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                             emperor_id=new_emperor.id)
                db.session.add(new_emperor_portrait)
                new_log_200 = LogBook(original_id = new_emperor_portrait.id, title = file_name, username = current_user.username)
                #db.session.commit()
                db.session.add(new_log_200)
                db.session.commit()
            return redirect(url_for("angelos"))
        else:
            temporary_edit = TemporaryEmperor(username=current_user.username, old_id=int(form.edit.data),
                                              title=form.title.data, in_greek=form.in_greek.data, birth=form.birth.data,
                                              death=form.death.data, reign=form.reign.data, life=form.life.data,
                                              dynasty=form.dynasty.data, reign_start = form.reign_start.data, references = form.references.data, ascent_to_power = form.ascent_to_power.data)

            db.session.add(temporary_edit)
            db.session.commit()
            if form.portrait.data:
                file_name = secure_filename(form.portrait.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.portrait.data.save(new_path_for_uploading)
                id_data = db.session.query(TemporaryEmperor).filter_by(username = current_user.username).order_by(TemporaryEmperor.id.desc()).first()
                photo = TemporaryImage(username=current_user.username, old_id=int(form.edit.data), filename=file_name,
                                       url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                       temporary_emperor_id=id_data.id)
                db.session.add(photo)
                db.session.commit()
                confirmation_email(id=temporary_edit.id)
            return redirect(url_for("angelos"))
    return render_template('angelos.html', title = "Angelos dynasty", macedonian_lst = macedonian_lst, new_form = form, form_open = True, article_title = "Angelos dynasty (1085-1204)")





@app.route("/add_new_emperor_4", methods = ['POST'])
@login_required
def add_new_emperor_4():
    form = AllEmperorForm()
    macedonian_lst = db.session.query(Emperor).filter_by(dynasty = 'Palaiologos').all()
    if form.validate_on_submit() and int(form.edit.data) == -1:
        if current_user.role == "Admin":
            new_emperor = Emperor(title=form.title.data, in_greek=form.in_greek.data, birth=form.birth.data,
                                  death=form.death.data, reign=form.reign.data, life=form.life.data,
                                  dynasty=form.dynasty.data, reign_start = form.reign_start.data, references = form.references.data, ascent_to_power = form.ascent_to_power.data)
            db.session.add(new_emperor)
            db.session.commit()
            new_log_114 = LogBook(original_id=int(new_emperor.id), title=new_emperor.title, username=current_user.username)
            db.session.add(new_log_114)
            db.session.commit()
            # print(form.portrait.data.filename)
            if form.portrait.data:
                file_name = secure_filename(form.portrait.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                print(path_for_uploading)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.portrait.data.save(new_path_for_uploading)
                new_emperor_portrait = Image(filename=file_name,
                                             url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                             emperor_id=new_emperor.id)
                db.session.add(new_emperor_portrait)
                db.session.commit()
                new_log_1 = LogBook(original_id = new_emperor_portrait.id, title = file_name, username = current_user.username)
                db.session.add(new_log_1)
                db.session.commit()
            return redirect(url_for("palaiologos"))
        else:
            temporary_edit_1 = TemporaryEmperor(username=current_user.username, old_id=int(form.edit.data),
                                              title=form.title.data, in_greek=form.in_greek.data, birth=form.birth.data,
                                              death=form.death.data, reign=form.reign.data, life=form.life.data,
                                              dynasty=form.dynasty.data, reign_start = form.reign_start.data, references = form.references.data, ascent_to_power = form.ascent_to_power.data)

            db.session.add(temporary_edit_1)
            db.session.commit()

            if form.portrait.data:
                file_name = secure_filename(form.portrait.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.portrait.data.save(new_path_for_uploading)
                id_data = db.session.query(TemporaryEmperor).filter_by(username = current_user.username).order_by(TemporaryEmperor.id.desc()).first()
                photo_1 = TemporaryImage(username=current_user.username, old_id=form.edit.data, filename=file_name,
                                       url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                       temporary_emperor_id=id_data.id)
                db.session.add(photo_1)
                db.session.commit()
                confirmation_email(id=temporary_edit_1.id)
            return redirect(url_for("palaiologos"))
    return render_template('palaiologos.html', title = "Palaiologos dynasty", macedonian_lst = macedonian_lst, new_form = form, form_open = True, article_title = "Palaiologos dynasty (1259-1453)")










@app.route("/admin")
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

@app.route('/delete_user', methods=['POST'])
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
            return redirect(url_for('home'))
        else:
            db.session.delete(u)
            db.session.commit()
    return redirect(url_for('admin'))

@app.route('/invitation_code/<int:id>', methods=['POST', 'GET'])
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


@app.route('/edit_emperor/<int:id>', methods = ['POST', 'GET'])
@login_required
def edit_emperor(id):
    emperor_first = db.session.get(Emperor, id)
    form = AllEmperorForm()
    if request.method == "GET":
        form.edit.data = emperor_first.id
        form.title.data = emperor_first.title
        form.reign_start.data = emperor_first.reign_start
        form.ascent_to_power.data = emperor_first.ascent_to_power
        form.references.data = emperor_first.references
        form.in_greek.data = emperor_first.in_greek
        form.birth.data = emperor_first.birth
        form.death.data = emperor_first.death
        form.reign.data = emperor_first.reign
        form.life.data = emperor_first.life
        form.dynasty.data = emperor_first.dynasty

    if form.validate_on_submit():
        if current_user.role == "Admin":
            emperor_new_edit = db.session.get(Emperor, int(form.edit.data))
            emperor_new_edit.title = form.title.data
            emperor_new_edit.ascent_to_power = form.ascent_to_power.data
            emperor_new_edit.reign_start = form.reign_start.data
            emperor_new_edit.references = form.references.data
            emperor_new_edit.in_greek = form.in_greek.data
            emperor_new_edit.birth = form.birth.data
            emperor_new_edit.death = form.death.data
            emperor_new_edit.reign = form.reign.data
            emperor_new_edit.life = form.life.data
            emperor_new_edit.dynasty = form.dynasty.data
            new_log_2 = LogBook(original_id=emperor_new_edit.id, title=emperor_new_edit.title, username=current_user.username)
            db.session.add(new_log_2)
            if form.portrait.data:
                file_name = secure_filename(form.portrait.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.portrait.data.save(new_path_for_uploading)
                photo = db.session.query(Image).filter_by(emperor_id=emperor_new_edit.id).order_by(
                    Image.id.asc()).first()
                if not photo:
                    photo = Image(emperor_id=emperor_new_edit.id)
                    db.session.add(photo)
                photo.filename = file_name
                photo.url = url_for('static', filename=f"images/uploaded_photos/{file_name}")
                new_log_3 = LogBook(original_id = photo.id, title = file_name, username = current_user.username)
                db.session.add(new_log_3)
            db.session.commit()
            return redirect(url_for('macedonian_emperors', id=emperor_first.id))
        else:
            temporary_edit = TemporaryEmperor(username = current_user.username, old_id = int(form.edit.data), title = form.title.data, in_greek = form.in_greek.data, birth = form.birth.data, death = form.death.data, reign = form.reign.data, life = form.life.data, dynasty = form.dynasty.data, reign_start = form.reign_start.data, references = form.references.data, ascent_to_power = form.ascent_to_power.data)
            db.session.add(temporary_edit)
            db.session.commit()
            if form.portrait.data:
                id_data = db.session.query(TemporaryEmperor).filter_by(username = current_user.username).order_by(TemporaryEmperor.id.desc()).first()
                file_name = secure_filename(form.portrait.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.portrait.data.save(new_path_for_uploading)
                photo = TemporaryImage( username = current_user.username, old_id = int(form.edit.data),filename=file_name,
                                         url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                         temporary_emperor_id=id_data.id)
                db.session.add(photo)
            db.session.commit()
            confirmation_email(id)
            return redirect(url_for('macedonian_emperors', id=emperor_first.id))
    return render_template("macedonian_emperors.html", id=emperor_first.id, form_open = True, m_e = emperor_first, new_form = form, title = "Dynasties")

#Wars


@app.route("/add_new_war_1", methods = ['POST', 'GET'])
@login_required
def add_new_war_1():
    form = WarForm()
    foreign_wars_lst = db.session.query(War).filter(and_(War.war_type == "Foreign War")).all()
    war_map = folium.Map(location=[41.008333, 28.98], zoom_start=3)

    colors = cycle(['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
                    'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
                    'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray'])
    names = sorted({war.war_name for war in foreign_wars_lst if war.war_name})
    war_colors = {name: next(colors) for name in names}
    cluster = MarkerCluster().add_to(war_map)
    for war in foreign_wars_lst:
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
            new_war = War(title=form.title.data, start_year=form.start_year.data, dates=form.dates.data,
                                  location=form.location.data, longitude =form.longitude.data, latitude =form.latitude.data,
                                  roman_commanders=form.roman_commanders.data, enemy_commanders = form.enemy_commanders.data, roman_strength = form.roman_strength.data,
                          enemy_strength = form.enemy_strength.data, roman_loss = form.roman_loss.data , enemy_loss = form.enemy_loss.data, references = form.references.data,
                          dynasty = form.dynasty.data, war_name = form.war_name.data, war_type = form.war_type.data, description = form.description.data, result = form.result.data)
            db.session.add(new_war)
            db.session.commit()
            new_log_4 = LogBook(original_id=new_war.id, title=new_war.title, username=current_user.username)
            db.session.add(new_log_4)
            # print(form.portrait.data.filename)
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                print(path_for_uploading)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)

                new_war_image = Image(filename=file_name,
                                             url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                             war_id=new_war.id)
                new_log_5 = LogBook(original_id=new_war_image.id, title=file_name, username=current_user.username)
                db.session.add(new_log_5)
                db.session.add(new_war_image)
                db.session.commit()
            return redirect(url_for("foreign_wars_1"))
        else:
            temporary_war_edit = TemporaryWar(username=current_user.username, old_id=int(form.edit.data),
                                                  title=form.title.data, start_year=form.start_year.data,
                                                  dates=form.dates.data,
                                                  location=form.location.data, longitude=form.longitude.data,
                                                  latitude=form.latitude.data,
                                                  roman_commanders=form.roman_commanders.data,
                                                  enemy_commanders=form.enemy_commanders.data,
                                                  roman_strength=form.roman_strength.data,
                                                  enemy_strength=form.enemy_strength.data,
                                                  roman_loss=form.roman_loss.data, enemy_loss=form.enemy_loss.data,
                                                  references=form.references.data,
                                                  dynasty=form.dynasty.data, war_name=form.war_name.data,
                                                  war_type=form.war_type.data, description=form.description.data,
                                                  result=form.result.data
                                                  )

            db.session.add(temporary_war_edit)
            db.session.commit()
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                id_data = db.session.query(TemporaryWar).filter_by(username = current_user.username).order_by(TemporaryWar.id.desc()).first()
                photo = TemporaryImage(username=current_user.username, old_id=int(form.edit.data), filename=file_name,
                                       url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                       temporary_war_id= id_data.id)
                db.session.add(photo)
                db.session.commit()
                confirmation_email(id = temporary_war_edit.id)
            return redirect(url_for("foreign_wars_1"))
    return render_template('foreign_war_1.html', title = "Foreign Wars", foreign_wars_lst = foreign_wars_lst, war_html =Markup(war_html), form_open = True, new_form = form )






@app.route("/add_new_war_2", methods = ['POST', 'GET'])
@login_required
def add_new_war_2():
    form = WarForm()
    foreign_wars_lst = db.session.query(War).filter(and_(War.war_type == "Civil War")).all()
    war_map = folium.Map(location=[41.008333, 28.98], zoom_start=3)

    colors = cycle(['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
                    'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
                    'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray'])
    names = sorted({war.war_name for war in foreign_wars_lst if war.war_name})
    war_colors = {name: next(colors) for name in names}
    cluster = MarkerCluster().add_to(war_map)
    for war in foreign_wars_lst:
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
            new_war = War(title=form.title.data, start_year=form.start_year.data, dates=form.dates.data,
                                  location=form.location.data, longitude =form.longitude.data, latitude =form.latitude.data,
                                  roman_commanders=form.roman_commanders.data, enemy_commanders = form.enemy_commanders.data, roman_strength = form.roman_strength.data,
                          enemy_strength = form.enemy_strength.data, roman_loss = form.roman_loss.data , enemy_loss = form.enemy_loss.data, references = form.references.data,
                          dynasty = form.dynasty.data, war_name = form.war_name.data, war_type = form.war_type.data, description = form.description.data, result = form.result.data)
            db.session.add(new_war)
            db.session.commit()
            new_log_4 = LogBook(original_id=new_war.id, title=new_war.title, username=current_user.username)
            db.session.add(new_log_4)
            # print(form.portrait.data.filename)
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                print(path_for_uploading)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                new_war_image = Image(filename=file_name,
                                             url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                             war_id=new_war.id)
                new_log_5 = LogBook(original_id=new_war_image.id, title=file_name, username=current_user.username)
                db.session.add(new_log_5)
                db.session.add(new_war_image)
                db.session.commit()
            return redirect(url_for("civil_wars"))
        else:
            temporary_war_edit = TemporaryWar(username=current_user.username, old_id=int(form.edit.data),
                                                  title=form.title.data, start_year=form.start_year.data,
                                                  dates=form.dates.data,
                                                  location=form.location.data, longitude=form.longitude.data,
                                                  latitude=form.latitude.data,
                                                  roman_commanders=form.roman_commanders.data,
                                                  enemy_commanders=form.enemy_commanders.data,
                                                  roman_strength=form.roman_strength.data,
                                                  enemy_strength=form.enemy_strength.data,
                                                  roman_loss=form.roman_loss.data, enemy_loss=form.enemy_loss.data,
                                                  references=form.references.data,
                                                  dynasty=form.dynasty.data, war_name=form.war_name.data,
                                                  war_type=form.war_type.data, description=form.description.data,
                                                  result=form.result.data
                                                  )

            db.session.add(temporary_war_edit)
            db.session.commit()
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                id_data = db.session.query(TemporaryWar).filter_by(username = current_user.username).order_by(TemporaryWar.id.desc()).first()
                photo = TemporaryImage(username=current_user.username, old_id=int(form.edit.data), filename=file_name,
                                       url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                       temporary_war_id= id_data.id)
                db.session.add(photo)
                db.session.commit()
                confirmation_email(id = temporary_war_edit.id)
            return redirect(url_for("civil_wars"))
    return render_template('civil_wars.html', title = "Civil Wars", foreign_wars_lst = foreign_wars_lst, war_html =Markup(war_html), form_open = True, new_form = form )










@app.route('/edit_war/<int:id>', methods = ['POST', 'GET'])
@login_required
def edit_war(id):
    war_first = db.session.get(War, id)
    form = WarForm()
    if request.method == "GET":
        form.edit.data = war_first.id
        form.title.data = war_first.title
        form.start_year.data = war_first.start_year
        form.dates.data = war_first.dates
        form.location.data = war_first.location
        form.longitude.data = war_first.longitude
        form.latitude.data = war_first.latitude
        form.roman_commanders.data = war_first.roman_commanders
        form.enemy_commanders.data = war_first.enemy_commanders
        form.roman_strength.data = war_first.roman_strength
        form.enemy_strength.data = war_first.enemy_strength
        form.roman_loss.data = war_first.roman_loss
        form.enemy_loss.data = war_first.enemy_loss
        form.dynasty.data = war_first.dynasty
        form.war_name.data = war_first.war_name
        form.war_type.data = war_first.war_type
        form.description.data = war_first.description
        form.references.data = war_first.references
        form.result.data = war_first.result

    if form.validate_on_submit():
        if current_user.role == "Admin":
            war_new_edit = db.session.get(War, int(form.edit.data))
            war_new_edit.title = form.title.data
            war_new_edit.start_year =  form.start_year.data
            war_new_edit.dates = form.dates.data
            war_new_edit.location = form.location.data
            war_new_edit.longitude = form.longitude.data
            war_new_edit.latitude = form.latitude.data
            war_new_edit.roman_commanders = form.roman_commanders.data
            war_new_edit.enemy_commanders = form.enemy_commanders.data
            war_new_edit.roman_strength = form.roman_strength.data
            war_new_edit.enemy_strength = form.enemy_strength.data
            war_new_edit.roman_loss = form.roman_loss.data
            war_new_edit.enemy_loss = form.enemy_loss.data
            war_new_edit.dynasty = form.dynasty.data
            war_new_edit.war_name = form.war_name.data
            war_new_edit.war_type = form.war_type.data
            war_new_edit.description = form.description.data
            war_new_edit.references = form.references.data
            war_new_edit.result = form.result.data
            new_log_6 = LogBook(original_id=war_new_edit.id, title=war_new_edit.title, username=current_user.username)
            db.session.add(new_log_6)
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                photo = db.session.query(Image).filter_by(war_id=war_new_edit.id).order_by(
                    Image.id.asc()).first()
                if not photo:
                    photo = Image(war_id=war_new_edit.id)
                    db.session.add(photo)
                photo.filename = file_name
                new_log_7 = LogBook(original_id=photo.id, title=file_name,
                                    username=current_user.username)
                db.session.add(new_log_7)
                photo.url = url_for('static', filename=f"images/uploaded_photos/{file_name}")
            db.session.commit()
            return redirect(url_for('war_info_foreign_1', id=war_first.id))
        else:
            temporary_edit = TemporaryWar(username=current_user.username, old_id=int(form.edit.data),
                                                  title=form.title.data, start_year=form.start_year.data,
                                                  dates=form.dates.data,
                                                  location=form.location.data, longitude=form.longitude.data,
                                                  latitude=form.latitude.data,
                                                  roman_commanders=form.roman_commanders.data,
                                                  enemy_commanders=form.enemy_commanders.data,
                                                  roman_strength=form.roman_strength.data,
                                                  enemy_strength=form.enemy_strength.data,
                                                  roman_loss=form.roman_loss.data, enemy_loss=form.enemy_loss.data,
                                                  references=form.references.data,
                                                  dynasty=form.dynasty.data, war_name=form.war_name.data,
                                                  war_type=form.war_type.data, description=form.description.data,
                                                  result=form.result.data)
            db.session.add(temporary_edit)
            db.session.commit()
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                id_data = db.session.query(TemporaryWar).filter_by(username = current_user.username).order_by(TemporaryWar.id.desc()).first()
                photo = TemporaryImage( username = current_user.username, old_id = int(form.edit.data),filename=file_name,
                                         url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                         temporary_war_id=id_data.id)
                db.session.add(photo)
            db.session.commit()
            confirmation_email(id=id)
            return redirect(url_for('war_info_foreign_1', id=war_first.id))
    war_first = db.session.get(War, id)
    return render_template("war_info.html", id=war_first.id, form_open = True, war = war_first, new_form = form, title = "Battle information")
    #return render_template("war_info.html", war = war, title = "Battle information")





@app.route('/edit_wars_users/<int:id>', methods = ['POST', 'GET'])
@login_required
def edit_wars_users(id):
    war_first = db.session.get(TemporaryWar, id)
    form = WarForm()
    if request.method == "GET":
        form.edit.data = war_first.id
        form.title.data = war_first.title
        form.start_year.data = war_first.start_year
        form.dates.data = war_first.dates
        form.location.data = war_first.location
        form.longitude.data = war_first.longitude
        form.latitude.data = war_first.latitude
        form.roman_commanders.data = war_first.roman_commanders
        form.enemy_commanders.data = war_first.enemy_commanders
        form.roman_strength.data = war_first.roman_strength
        form.enemy_strength.data = war_first.enemy_strength
        form.roman_loss.data = war_first.roman_loss
        form.enemy_loss.data = war_first.enemy_loss
        form.dynasty.data = war_first.dynasty
        form.war_name.data = war_first.war_name
        form.war_type.data = war_first.war_type
        form.description.data = war_first.description
        form.references.data = war_first.references
        form.result.data = war_first.result
    if form.validate_on_submit():
        war_new_edit = db.session.get(TemporaryWar, int(form.edit.data))
        war_new_edit.title = form.title.data
        war_new_edit.start_year = form.start_year.data
        war_new_edit.dates = form.dates.data
        war_new_edit.location = form.location.data
        war_new_edit.longitude = form.longitude.data
        war_new_edit.latitude = form.latitude.data
        war_new_edit.roman_commanders = form.roman_commanders.data
        war_new_edit.enemy_commanders = form.enemy_commanders.data
        war_new_edit.roman_strength = form.roman_strength.data
        war_new_edit.enemy_strength = form.enemy_strength.data
        war_new_edit.roman_loss = form.roman_loss.data
        war_new_edit.enemy_loss = form.enemy_loss.data
        war_new_edit.dynasty = form.dynasty.data
        war_new_edit.war_name = form.war_name.data
        war_new_edit.war_type = form.war_type.data
        war_new_edit.description = form.description.data
        war_new_edit.references = form.references.data
        war_new_edit.result = form.result.data
        if form.image.data:
            file_name = secure_filename(form.image.data.filename)
            uuid_ = uuid.uuid4().hex[:8]
            file_name = f"{uuid_}_{file_name}"
            path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            new_path_for_uploading = path_for_uploading.replace('\\', '/')
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            form.image.data.save(new_path_for_uploading)
            photo = db.session.query(TemporaryImage).filter_by(temporary_war_id=war_new_edit.id).order_by(
                TemporaryImage.id.asc()).first()
            if not photo:
                photo = TemporaryImage(temporary_war_id =war_new_edit.id)
                db.session.add(photo)
            photo.filename = file_name
            photo.url = url_for('static', filename=f"images/uploaded_photos/{file_name}")
        if war_first.status != "Pending":
            war_first.status = "Pending"
            confirmation_email(id=war_first.id)
        db.session.commit()
        return redirect(url_for('war_info_edit_user', id=war_first.id))
    return render_template("war_info_edit_user.html", war = war_first, new_form = form, form_open = True, title = "Editing requests")






@app.route("/approve_war_edit/<int:id>", methods = ['GET', 'POST'])
@admin_only
def approve_war_edit(id):
    war_first = db.session.get(TemporaryWar, id)
    new_war = db.session.get(War, int(war_first.old_id))
    new_war.title = war_first.title
    new_war.start_year = war_first.start_year
    new_war.dates = war_first.dates
    new_war.location = war_first.location
    new_war.longitude = war_first.longitude
    new_war.latitude = war_first.latitude
    new_war.roman_commanders = war_first.roman_commanders
    new_war.enemy_commanders = war_first.enemy_commanders
    new_war.roman_strength = war_first.roman_strength
    new_war.enemy_strength = war_first.enemy_strength
    new_war.roman_loss = war_first.roman_loss
    new_war.enemy_loss = war_first.enemy_loss
    new_war.dynasty = war_first.dynasty
    new_war.war_name = war_first.war_name
    new_war.war_type = war_first.war_type
    new_war.description = war_first.description
    new_war.references = war_first.references
    new_war.result = war_first.result
    user = db.session.query(User).filter_by(username = war_first.username).first()
    new_log_8 = LogBook(original_id=id, title=new_war.title,
                        username=current_user.username)
    db.session.add(new_log_8)
    if war_first.temporary_images:
        photo = db.session.query(Image).filter_by(war_id=new_war.id).order_by(Image.id.asc()).first()
        if photo:
            file_name = secure_filename(war_first.temporary_images[0].filename)
            photo.filename = file_name
            photo.url = f"/static/images/uploaded_photos/{file_name}"
            photo.war_id = new_war.id
            db.session.delete(war_first.temporary_images[0])
            new_log_900 = LogBook(original_id=photo.id, title=file_name,
                                username=current_user.username)
            db.session.add(new_log_900)
        else:
            file_name = secure_filename(war_first.temporary_images[0].filename)
            photo = Image(filename = file_name, url = f"/static/images/uploaded_photos/{file_name}", war_id = new_war.id)
            db.session.add(photo)
            db.session.delete(war_first.temporary_images[0])
            new_log_9 = LogBook(original_id=photo.id, title=file_name,
                                username=current_user.username)
            db.session.add(new_log_9)
    approval_email(user_email=user.email, emperor_title=new_war.title)
    db.session.delete(war_first)
    db.session.commit()
    return redirect(url_for('manage_edits'))

@app.route("/approve_war_add/<int:id>", methods=['GET', 'POST'])
@admin_only
def approve_war_add(id):
    add_war = db.session.get(TemporaryWar, id)
    new_war = War(title=add_war.title, start_year=add_war.start_year, dates=add_war.dates,
                      location=add_war.location, longitude=add_war.longitude, latitude=add_war.latitude,
     roman_commanders=add_war.roman_commanders, enemy_commanders = add_war.enemy_commanders, roman_strength = add_war.roman_strength,
                          enemy_strength = add_war.enemy_strength, roman_loss = add_war.roman_loss , enemy_loss = add_war.enemy_loss, references = add_war.references,
                          dynasty = add_war.dynasty, war_name = add_war.war_name, war_type = add_war.war_type, description = add_war.description, result = add_war.result)
    user = db.session.query(User).filter_by(username = add_war.username).first()
    db.session.add(new_war)
    new_log_1000 = LogBook(original_id=new_war.id, title=new_war.title,
                        username=current_user.username)
    db.session.add(new_log_1000)
    if add_war.temporary_images:
        file_name = secure_filename(add_war.temporary_images[0].filename)
        photo = Image(filename = file_name, url = f"/static/images/uploaded_photos/{file_name}", war_id = new_war.id)
        db.session.add(photo)
        db.session.delete(add_war.temporary_images[0])
        new_log_1100 = LogBook(original_id=photo.id, title=file_name,
                            username=current_user.username)
        db.session.add(new_log_1100)
    approval_email(user_email=user.email, emperor_title=new_war.title)
    db.session.delete(add_war)
    db.session.commit()
    return redirect(url_for('manage_additions'))


@app.route("/reject_war_add/<int:id>", methods = ['GET', 'POST'])
def reject_war_add(id):
    add_war = db.session.get(TemporaryWar, id)
    add_war.status = "Reject"
    user = db.session.query(User).filter_by(username = add_war.username).first()
    rejection_email(user_email=user.email, emperor_title=add_war.title)
    db.session.commit()
    return redirect(url_for('manage_additions'))

@app.route("/reject_war_edit/<int:id>", methods=['GET', 'POST'])
def reject_war_edit(id):
    add_war = db.session.get(TemporaryWar, id)
    add_war.status = "Reject"
    user = db.session.query(User).filter_by(username=add_war.username).first()
    rejection_email(user_email=user.email, emperor_title=add_war.title)
    db.session.commit()
    return redirect(url_for('manage_edits'))




@app.route("/admin_delete_war_1/<int:id>", methods = ['GET', 'POST'])
def admin_delete_war_1(id):
    delete_war_temporary = db.session.get(TemporaryWar, id)
    if delete_war_temporary.temporary_images:
        delete_image_temporary = delete_war_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_war_temporary)
    db.session.commit()
    return redirect(url_for('manage_edits'))




@app.route("/admin_delete_war_2/<int:id>", methods = ['GET', 'POST'])
def admin_delete_war_2(id):
    delete_war_temporary = db.session.get(TemporaryWar, id)
    if delete_war_temporary.temporary_images:
        delete_image_temporary = delete_war_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_war_temporary)
    db.session.commit()
    return redirect(url_for('manage_additions'))



#Wars




@app.route("/admin_delete_emperor_1/<int:id>", methods = ['GET', 'POST'])
def admin_delete_emperor_1(id):
    delete_emperor_temporary = db.session.get(TemporaryEmperor, id)
    if delete_emperor_temporary.temporary_images:
        delete_image_temporary = delete_emperor_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_emperor_temporary)
    db.session.commit()
    return redirect(url_for('manage_additions'))
#Wars end



#architecture



@app.route('/art_selection/architecture_info', methods= ['GET', 'POST'])
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



@app.route('/art_selection/architecture_info/architecture_info_detail/<int:id>', methods= ['GET', 'POST'])
def architecture_info_detail(id):
    form = ArchitectureForm()
    form_1 = ImageUploadForm()
    form_2 = ImageEditForm()
    architecture_first = db.session.get(Architecture, id)
    images = db.session.query(Image).filter(Image.architecture_id == id).all()
    form.edit.data = architecture_first.id
    form.title.data = architecture_first.title
    form.construction_completed.data = architecture_first.construction_completed
    form.location.data = architecture_first.location
    form.longitude.data = architecture_first.longitude
    form.latitude.data = architecture_first.latitude
    form.in_greek.data = architecture_first.in_greek
    form.description.data = architecture_first.description
    form.references.data = architecture_first.references
    form.current_status.data = architecture_first.current_status
    form.building_type.data = architecture_first.building_type
    form.architectural_style.data = architecture_first.architectural_style

    return render_template('architecture_info_detail.html', title = "Architecture Info", new_form = form, new_form_1 = form_1, new_form_2 = form_2,form_open = False ,form_open_1 = False,form_open_2 = False ,building = architecture_first, images = images)






@app.route("/add_new_architecture", methods = ['POST', 'GET'])
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
            new_architecture = Architecture(title=form.title.data, location = form.location.data, references= form.references.data, in_greek = form.in_greek.data, construction_completed = form.construction_completed.data, architectural_style = form.architectural_style.data,
                                            current_status = form.current_status.data, longitude = form.longitude.data, latitude = form.latitude.data, description = form.description.data, building_type = form.building_type.data )
            db.session.add(new_architecture)
            new_log_16 = LogBook(original_id=new_architecture.id, title=new_architecture.title,
                                username=current_user.username)
            db.session.add(new_log_16)
            db.session.commit()
            # print(form.portrait.data.filename)
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                print(path_for_uploading)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                new_architecture_image = Image(filename=file_name,
                                             url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                             architecture_id=new_architecture.id)
                db.session.add(new_architecture_image)
                new_log_17 = LogBook(original_id=new_architecture_image.id, title=file_name,
                                     username=current_user.username)
                db.session.add(new_log_17)
                db.session.commit()
            return redirect(url_for("architecture_info"))
        else:
            temporary_architecture_edit = TemporaryArchitecture(username=current_user.username, old_id=int(form.edit.data),
                                                                title=form.title.data, location=form.location.data,
                                                                references=form.references.data,
                                                                in_greek=form.in_greek.data,
                                                                construction_completed=form.construction_completed.data,
                                                                architectural_style=form.architectural_style.data,
                                                                current_status=form.current_status.data,
                                                                longitude=form.longitude.data,
                                                                latitude=form.latitude.data,
                                                                description=form.description.data,
                                                                building_type=form.building_type.data
                                                                )

            db.session.add(temporary_architecture_edit)
            db.session.commit()
            if form.image.data:
                id_data = db.session.query(TemporaryArchitecture).filter_by(username = current_user.username).order_by(TemporaryArchitecture.id.desc()).first()
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                photo = TemporaryImage(username=current_user.username, old_id=int(form.edit.data), filename=file_name,
                                       url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                       temporary_architecture_id= id_data.id)
                db.session.add(photo)
                db.session.commit()
                confirmation_email(id = temporary_architecture_edit.id)
            return redirect(url_for("architecture_info"))
    return render_template('architecture_info.html', title = "Architecture", buildings_lst = buildings_lst , architecture_html =Markup(building_html), form_open = True, new_form = form )






@app.route('/edit_architecture/<int:id>', methods = ['POST', 'GET'])
@login_required
def edit_architecture(id):
    architecture_first = db.session.get(Architecture, id)
    form = ArchitectureForm()
    form_1 = ImageUploadForm()
    form_2 = ImageEditForm()
    images = db.session.query(Image).filter(Image.architecture_id == id).all() or []
    if request.method == "GET":
        form.edit.data = architecture_first.id
        form.title.data = architecture_first.title
        form.construction_completed.data = architecture_first.construction_completed
        form.location.data = architecture_first.location
        form.longitude.data = architecture_first.longitude
        form.latitude.data = architecture_first.latitude
        form.in_greek.data = architecture_first.in_greek
        form.description.data = architecture_first.description
        form.references.data = architecture_first.references
        form.current_status.data = architecture_first.current_status
        form.building_type.data = architecture_first.building_type
        form.architectural_style.data = architecture_first.architectural_style

    if form.validate_on_submit():
        if current_user.role == "Admin":
            architecture_new_edit = db.session.get(Architecture, int(form.edit.data))
            architecture_new_edit.title = form.title.data
            architecture_new_edit.construction_completed =  form.construction_completed.data
            architecture_new_edit.location = form.location.data
            architecture_new_edit.longitude = form.longitude.data
            architecture_new_edit.latitude = form.latitude.data
            architecture_new_edit.in_greek = form.in_greek.data
            architecture_new_edit.description = form.description.data
            architecture_new_edit.references = form.references.data
            architecture_new_edit.current_status = form.current_status.data
            architecture_new_edit.building_type = form.building_type.data
            architecture_new_edit.architectural_style = form.architectural_style.data
            new_log_18 = LogBook(original_id=id, title=architecture_new_edit.title,
                                 username=current_user.username)
            db.session.add(new_log_18)
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                photo = db.session.query(Image).filter_by(architecture_id=architecture_new_edit.id).order_by(
                    Image.id.asc()).first()
                if not photo:
                    photo = Image(architecture_id=architecture_new_edit.id)
                    db.session.add(photo)
                photo.filename = file_name
                photo.url = url_for('static', filename=f"images/uploaded_photos/{file_name}")
                new_log_10000 = LogBook(original_id=photo.id, title=file_name,
                                     username=current_user.username)
                db.session.add(new_log_10000)
            db.session.commit()
            return redirect(url_for('architecture_info_detail', id=architecture_new_edit.id))
        else:
            temporary_edit = TemporaryArchitecture(username=current_user.username, old_id=int(form.edit.data),
                                                                title=form.title.data, location=form.location.data,
                                                                references=form.references.data,
                                                                in_greek=form.in_greek.data,
                                                                construction_completed=form.construction_completed.data,
                                                                architectural_style=form.architectural_style.data,
                                                                current_status=form.current_status.data,
                                                                longitude=form.longitude.data,
                                                                latitude=form.latitude.data,
                                                                description=form.description.data,
                                                                building_type=form.building_type.data)
            db.session.add(temporary_edit)
            db.session.commit()
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                id_data = db.session.query(TemporaryArchitecture).filter_by(username = current_user.username).order_by(TemporaryArchitecture.id.desc()).first()
                photo = TemporaryImage( username = current_user.username, old_id = int(form.edit.data),filename=file_name,
                                         url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                         temporary_architecture_id=id_data.id)
                db.session.add(photo)
            db.session.commit()
            confirmation_email(id = id)
            return redirect(url_for('architecture_info_detail', id=temporary_edit.id))
    return render_template("architecture_info_detail.html", id=architecture_first.id, form_open = True, building = architecture_first, new_form = form, new_form_1 = form_1, new_form_2 = form_2,title = "Architecture information", form_open_1 = False, form_open_2 = False, images = images)
    #return render_template("war_info.html", war = war, title = "Battle information")






@app.route('/edit_architecture_users/<int:id>', methods = ['POST', 'GET'])
@login_required
def edit_architecture_users(id):
    architecture_first = db.session.get(TemporaryArchitecture, id)
    form = ArchitectureForm()

    if request.method == "GET":
        form.edit.data = architecture_first.id
        form.title.data = architecture_first.title
        form.construction_completed.data = architecture_first.construction_completed
        form.location.data = architecture_first.location
        form.longitude.data = architecture_first.longitude
        form.latitude.data = architecture_first.latitude
        form.in_greek.data = architecture_first.in_greek
        form.description.data = architecture_first.description
        form.references.data = architecture_first.references
        form.current_status.data = architecture_first.current_status
        form.building_type.data = architecture_first.building_type
        form.architectural_style.data = architecture_first.architectural_style

    if form.validate_on_submit():
        architecture_new_edit = db.session.get(TemporaryArchitecture, int(form.edit.data))
        architecture_new_edit.title = form.title.data
        architecture_new_edit.construction_completed = form.construction_completed.data
        architecture_new_edit.location = form.location.data
        architecture_new_edit.longitude = form.longitude.data
        architecture_new_edit.latitude = form.latitude.data
        architecture_new_edit.in_greek = form.in_greek.data
        architecture_new_edit.description = form.description.data
        architecture_new_edit.references = form.references.data
        architecture_new_edit.current_status = form.current_status.data
        architecture_new_edit.building_type = form.building_type.data
        architecture_new_edit.architectural_style = form.architectural_style.data
        if form.image.data:
            file_name = secure_filename(form.image.data.filename)
            uuid_ = uuid.uuid4().hex[:8]
            file_name = f"{uuid_}_{file_name}"
            path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            new_path_for_uploading = path_for_uploading.replace('\\', '/')
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            form.image.data.save(new_path_for_uploading)
            photo = db.session.query(TemporaryImage).filter_by(
                temporary_architecture_id=architecture_new_edit.id).order_by(
                TemporaryImage.id.asc()).first()
            if not photo:
                photo = TemporaryImage(temporary_architecture_id=architecture_new_edit.id)
                db.session.add(photo)
            photo.filename = file_name
            photo.url = url_for('static', filename=f"images/uploaded_photos/{file_name}")

        if architecture_first.status != "Pending":
            architecture_new_edit.status = "Pending"
            confirmation_email(id=architecture_first.id)
        db.session.commit()
        return redirect(url_for('architecture_info_edit_user', id=architecture_first.id))
    return render_template("architecture_info_edit_user.html", building = architecture_first, new_form = form, form_open = True, title = "Editing requests")






@app.route("/approve_architecture_edit/<int:id>", methods = ['GET', 'POST'])
@admin_only
def approve_architecture_edit(id):
    architecture_first = db.session.get(TemporaryArchitecture, id)
    new_architecture = db.session.get(Architecture, int(architecture_first.old_id))
    new_architecture.title = architecture_first.title
    new_architecture.in_greek = architecture_first.in_greek
    new_architecture.architectural_style = architecture_first.architectural_style
    new_architecture.location = architecture_first.location
    new_architecture.longitude = architecture_first.longitude
    new_architecture.latitude = architecture_first.latitude
    new_architecture.current_status = architecture_first.current_status
    new_architecture.construction_completed = architecture_first.construction_completed
    new_architecture.building_type = architecture_first.building_type
    new_architecture.description = architecture_first.description
    new_architecture.references = architecture_first.references
    user = db.session.query(User).filter_by(username = architecture_first.username).first()
    new_log_20 = LogBook(original_id=id, title=new_architecture.title,
                         username=current_user.username)
    db.session.add(new_log_20)
    if architecture_first.temporary_images:
        photo = db.session.query(Image).filter_by(architecture_id=new_architecture.id).order_by(Image.id.asc()).first()
        if photo:
            file_name = secure_filename(architecture_first.temporary_images[0].filename)
            uuid_ = uuid.uuid4().hex[:8]
            photo.url = f"/static/images/uploaded_photos/{file_name}"
            photo.architecture_id = new_architecture.id
            new_log_2100 = LogBook(original_id=photo.id, title=file_name,
                                 username=current_user.username)
            db.session.add(new_log_2100)
            db.session.delete(architecture_first.temporary_images[0])
        else:
            file_name = secure_filename(architecture_first.temporary_images[0].filename)
            photo = Image(filename = file_name, url = f"/static/images/uploaded_photos/{file_name}", architecture_id = new_architecture.id)
            db.session.add(photo)
            new_log_21 = LogBook(original_id=photo.id, title=file_name,
                                 username=current_user.username)
            db.session.add(new_log_21)
            db.session.delete(architecture_first.temporary_images[0])
    approval_email(user_email=user.email, emperor_title=new_architecture.title)
    db.session.delete(architecture_first)
    db.session.commit()
    return redirect(url_for('manage_edits'))


@app.route("/approve_architecture_add/<int:id>", methods=['GET', 'POST'])
@admin_only
def approve_architecture_add(id):
    add_architecture = db.session.get(TemporaryArchitecture, id)
    new_architecture = Architecture(title=add_architecture.title, location = add_architecture.location, references= add_architecture.references, in_greek = add_architecture.in_greek, construction_completed = add_architecture.construction_completed, architectural_style = add_architecture.architectural_style,
                                            current_status = add_architecture.current_status, longitude = add_architecture.longitude, latitude = add_architecture.latitude, description = add_architecture.description, building_type = add_architecture.building_type)
    user = db.session.query(User).filter_by(username = add_architecture.username).first()
    db.session.add(new_architecture)
    new_log_2200 = LogBook(original_id=new_architecture.id, title=new_architecture.title,
                         username=current_user.username)
    db.session.add(new_log_2200)
    if add_architecture.temporary_images:
        file_name = secure_filename(add_architecture.temporary_images[0].filename)
        photo = Image(filename = file_name, url = f"/static/images/uploaded_photos/{file_name}", architecture_id = new_architecture.id)
        db.session.add(photo)
        new_log_2300 = LogBook(original_id=photo.id, title=file_name,
                             username=current_user.username)
        db.session.add(new_log_2300)
        db.session.delete(add_architecture.temporary_images[0])
    approval_email(user_email=user.email, emperor_title=add_architecture.title)
    db.session.delete(add_architecture)
    db.session.commit()
    return redirect(url_for('manage_additions'))



@app.route("/reject_architecture_add/<int:id>", methods = ['GET', 'POST'])
def reject_architecture_add(id):
    add_architecture = db.session.get(TemporaryArchitecture, id)
    add_architecture.status = "Reject"
    user = db.session.query(User).filter_by(username = add_architecture.username).first()
    rejection_email(user_email=user.email, emperor_title=add_architecture.title)
    db.session.commit()
    return redirect(url_for('manage_additions'))

@app.route("/reject_architecture_edit/<int:id>", methods=['GET', 'POST'])
def reject_architecture_edit(id):
    add_architecture = db.session.get(TemporaryArchitecture, id)
    add_architecture.status = "Reject"
    user = db.session.query(User).filter_by(username=add_architecture.username).first()
    rejection_email(user_email=user.email, emperor_title=add_architecture.title)
    db.session.commit()
    return redirect(url_for('manage_edits'))




@app.route("/admin_delete_architecture_1/<int:id>", methods = ['GET', 'POST'])
def admin_delete_architecture_1(id):
    delete_architecture_temporary = db.session.get(TemporaryArchitecture, id)
    if delete_architecture_temporary.temporary_images:
        delete_image_temporary = delete_architecture_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_architecture_temporary)
    db.session.commit()
    return redirect(url_for('manage_edits'))



@app.route("/admin_delete_architecture_2/<int:id>", methods = ['GET', 'POST'])
def admin_delete_architecture_2(id):
    delete_architecture_temporary = db.session.get(TemporaryArchitecture, id)
    if delete_architecture_temporary.temporary_images:
        delete_image_temporary = delete_architecture_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_architecture_temporary)
    db.session.commit()
    return redirect(url_for('manage_additions'))

@app.route("/edit_an_image/<int:id>", methods = ['GET', 'POST'])
@login_required
def edit_an_image(id):
    form = ImageEditForm()
    form_1 = ArchitectureForm()
    form_2 = ImageUploadForm()
    if current_user.user_type == "Authorised" or current_user.role == "Admin":
        if form.validate_on_submit():
            file_name = secure_filename(form.image.data.filename)
            uuid_ = uuid.uuid4().hex[:8]
            file_name = f"{uuid_}_{file_name}"
            path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            new_path_for_uploading = path_for_uploading.replace('\\', '/')
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            form.image.data.save(new_path_for_uploading)
            photo = db.session.query(Image).filter_by(id=form.id_number.data).first()
            if photo:
                if photo.architecture_id:
                    new_confirmation_email(id =photo.id, category="architecture")
                    photo.filename = file_name
                    photo.url = url_for('static', filename=f"images/uploaded_photos/{file_name}")
                    photo.caption = form.caption.data
                    db.session.add(photo)
                    db.session.commit()
                    new_log_24000 = LogBook(original_id=form.id_number.data, title=file_name,
                                         username=current_user.username)
                    db.session.add(new_log_24000)
                    db.session.commit()
                    flash("Successfully edited", "success")
                    return redirect(url_for('architecture_info_detail', id=id))
                elif photo.literature_id:
                    new_confirmation_email(id=photo.id, category="literature")
                    photo.filename = file_name
                    photo.url = url_for('static', filename=f"images/uploaded_photos/{file_name}")
                    photo.caption = form.caption.data
                    db.session.add(photo)
                    db.session.commit()
                    new_log_24000 = LogBook(original_id=form.id_number.data, title=file_name,
                                         username=current_user.username)
                    db.session.add(new_log_24000)
                    db.session.commit()
                    flash("Successfully edited", "success")
                    return redirect(url_for('literature_info_detail', id=id))
                elif photo.artifact_id:
                    new_confirmation_email(id=photo.id, category="artifact")
                    photo.filename = file_name
                    photo.url = url_for('static', filename=f"images/uploaded_photos/{file_name}")
                    photo.caption = form.caption.data
                    db.session.add(photo)
                    db.session.commit()
                    new_log_24000 = LogBook(original_id=form.id_number.data, title=file_name,
                                         username=current_user.username)
                    db.session.add(new_log_24000)
                    db.session.commit()
                    flash("Successfully edited", "success")
                    return redirect(url_for('artifact_info_detail', id=id))
            else:
                flash("Invalid ID number", "danger")
                return redirect(request.referrer)
    flash("Invalid details, please resubmit the form", "warning")
    return redirect(request.referrer)



@app.route('/add_an_image/<int:id>', methods = ['GET', 'POST'])
@login_required
def add_an_image(id):
    form = ImageUploadForm()
    form_1 = ArchitectureForm()
    form_2 = ImageEditForm()
    if current_user.user_type == "Authorised" or current_user.role == "Admin":
        if form.validate_on_submit():
            file_name = secure_filename(form.image.data.filename)
            uuid_ = uuid.uuid4().hex[:8]
            file_name = f"{uuid_}_{file_name}"
            path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            new_path_for_uploading = path_for_uploading.replace('\\', '/')
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            form.image.data.save(new_path_for_uploading)
            photo = Image(filename = file_name, url = url_for('static', filename=f"images/uploaded_photos/{file_name}"), caption = form.caption.data, architecture_id = id)
            db.session.add(photo)
            db.session.commit()
            id_data = db.session.query(Image).filter_by(architecture_id = id).order_by(Image.id.desc()).first()
            new_log_25000 = LogBook(original_id=id_data.id, title=file_name,
                                 username=current_user.username)
            db.session.add(new_log_25000)
            db.session.commit()
            new_confirmation_email(id=photo.id, category="architecture")
            flash("Successfully uploaded", "success")
            return redirect(url_for('architecture_info_detail', id=id))
    flash("Invalid details, please resubmit the form", "warning")
    return redirect(url_for('architecture_info_detail', id=id))



@app.route("/admin/manage_edits_additions_users/architecture_info_edit_user/<int:id>", methods = ['GET', 'POST'])
@login_required
def architecture_info_edit_user(id):
    #war_first = db.session.get(TemporaryWar, id)
    form = ArchitectureForm()
    architecture_first = db.session.get(TemporaryArchitecture, id)
    form.edit.data = architecture_first.id
    form.title.data = architecture_first.title
    form.construction_completed.data = architecture_first.construction_completed
    form.location.data = architecture_first.location
    form.longitude.data = architecture_first.longitude
    form.latitude.data = architecture_first.latitude
    form.in_greek.data = architecture_first.in_greek
    form.description.data = architecture_first.description
    form.references.data = architecture_first.references
    form.current_status.data = architecture_first.current_status
    form.building_type.data = architecture_first.building_type
    form.architectural_style.data = architecture_first.architectural_style

    return render_template("architecture_info_edit_user.html",building = architecture_first, form_open = False, title="Architecture edit/addition information", new_form=form)




#literature



@app.route('/art_selection/literature_info', methods= ['GET', 'POST'])
def literature_info():
    form = LiteratureForm()
    literature_lst = db.session.query(Literature).all()
    return render_template('literature_info.html', title = "Literature",literature_lst = literature_lst, new_form = form, form_open = False)


@app.route('/art_selection/literature_info/literature_info_detail/<int:id>', methods= ['GET', 'POST'])
def literature_info_detail(id):
    form = LiteratureForm()
    literature_first = db.session.get(Literature, id)
    form_1 = ImageUploadForm()
    form_2 = ImageEditForm()
    images = db.session.query(Image).filter(Image.literature_id == id).all()
    form.edit.data = literature_first.id
    form.title.data = literature_first.title
    form.year_completed.data = literature_first.year_completed
    form.genre.data = literature_first.genre
    form.in_greek.data = literature_first.in_greek
    form.description.data = literature_first.description
    form.references.data = literature_first.references
    form.current_location.data = literature_first.current_location
    form.author.data = literature_first.author
    return render_template('literature_info_detail.html', title = "Literature information",book = literature_first, new_form = form, new_form_1 = form_1, new_form_2 = form_2, images =images, form_open = False, form_open_1 = False, form_open_2 = False)






@app.route("/add_new_literature", methods = ['POST', 'GET'])
@login_required
def add_new_literature():
    form = LiteratureForm()
    literature_lst = db.session.query(Literature).all()
    if form.validate_on_submit() and int(form.edit.data) == -1:
        if current_user.role == "Admin":
            new_literature = Literature(title=form.title.data, current_location = form.current_location.data, references= form.references.data, in_greek = form.in_greek.data, year_completed = form.year_completed.data, genre = form.genre.data,
                                description = form.description.data, author = form.author.data )
            db.session.add(new_literature)
            new_log_26 = LogBook(original_id=new_literature.id, title=new_literature.title,
                                 username=current_user.username)
            db.session.add(new_log_26)
            db.session.commit()
            # print(form.portrait.data.filename)
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                print(path_for_uploading)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                new_literature_image = Image(filename=file_name,
                                             url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                             literature_id=new_literature.id)
                db.session.add(new_literature_image)
                new_log_27 = LogBook(original_id=new_literature_image.id, title=file_name,
                                     username=current_user.username)
                db.session.add(new_log_27)
                db.session.commit()
            return redirect(url_for("literature_info"))
        else:
            temporary_literature_edit = TemporaryLiterature(username=current_user.username, old_id=int(form.edit.data),
                                                                title=form.title.data, author = form.author.data,
                                                                current_location=form.current_location.data,
                                                                references=form.references.data,
                                                                in_greek=form.in_greek.data,
                                                                year_completed=form.year_completed.data,
                                                                genre=form.genre.data,
                                                                description=form.description.data
                                                                )

            db.session.add(temporary_literature_edit)
            db.session.commit()
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                id_data = db.session.query(TemporaryLiterature).filter_by(username = current_user.username).order_by(TemporaryLiterature.id.desc()).first()
                photo = TemporaryImage(username=current_user.username, old_id=int(form.edit.data), filename=file_name,
                                       url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                       temporary_literature_id= id_data.id)
                db.session.add(photo)
                db.session.commit()
                confirmation_email(temporary_literature_edit.id)
            return redirect(url_for("literature_info"))
    return render_template('literature_info.html', title = "Literature", literature_lst = literature_lst , form_open = True, new_form = form )





@app.route('/edit_literature/<int:id>', methods = ['POST', 'GET'])
@login_required
def edit_literature(id):
    literature_first = db.session.get(Literature, id)
    form = LiteratureForm()
    form_1 = ImageUploadForm()
    form_2 = ImageEditForm()
    images = db.session.query(Image).filter(Image.literature_id == id).all() or []
    if request.method == "GET":
        form.edit.data = literature_first.id
        form.title.data = literature_first.title
        form.year_completed.data = literature_first.year_completed
        form.genre.data = literature_first.genre
        form.in_greek.data = literature_first.in_greek
        form.description.data = literature_first.description
        form.references.data = literature_first.references
        form.current_location.data = literature_first.current_location
        form.author.data = literature_first.author
    if form.validate_on_submit():
        if current_user.role == "Admin":
            literature_new_edit = db.session.get(Literature, int(form.edit.data))
            literature_new_edit.title = form.title.data
            literature_new_edit.year_completed =  form.year_completed.data
            literature_new_edit.current_location= form.current_location.data
            literature_new_edit.genre = form.genre.data
            literature_new_edit.in_greek = form.in_greek.data
            literature_new_edit.description = form.description.data
            literature_new_edit.references = form.references.data
            literature_new_edit.author = form.author.data
            new_log_28 = LogBook(original_id=literature_new_edit.id, title=literature_new_edit.title,
                                 username=current_user.username)
            db.session.add(new_log_28)
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                photo = db.session.query(Image).filter_by(literature_id=literature_new_edit.id).order_by(Image.id.asc()).first()
                if not photo:
                    photo = Image(literature_id=literature_new_edit.id)
                    db.session.add(photo)
                photo.filename = file_name
                new_log_29 = LogBook(original_id=photo.id, title=file_name,
                                     username=current_user.username)
                db.session.add(new_log_29)
                photo.url = url_for('static', filename=f"images/uploaded_photos/{file_name}")
            db.session.commit()
            return redirect(url_for('literature_info_detail', id=literature_new_edit.id))
        else:
            temporary_edit = TemporaryLiterature(username=current_user.username, old_id=int(form.edit.data),
                                                 title=form.title.data, author=form.author.data,
                                                 current_location=form.current_location.data,
                                                 references=form.references.data,
                                                 in_greek=form.in_greek.data,
                                                 year_completed=form.year_completed.data,
                                                 genre=form.genre.data,
                                                 description=form.description.data
                                                 )
            db.session.add(temporary_edit)
            db.session.commit()
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                id_data = db.session.query(TemporaryLiterature).filter_by(username = current_user.username).order_by(TemporaryLiterature.id.desc()).first()
                photo = TemporaryImage( username = current_user.username, old_id = int(form.edit.data),filename=file_name,
                                         url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                         temporary_literature_id=id_data.id)
                db.session.add(photo)
            db.session.commit()
            confirmation_email(id)
            return redirect(url_for('literature_info_detail', id=literature_first.id))
    return render_template("literature_info_detail.html", id=literature_first.id, form_open = True, form_1 = False, form_2 = False,book = literature_first, new_form = form, new_form_1 = form_1, new_form_2 = form_2,title = "Literature information", images = images)
    #return render_template("war_info.html", war = war, title = "Battle information")




@app.route('/edit_literature_users/<int:id>', methods = ['POST', 'GET'])
@login_required
def edit_literature_users(id):
    literature_first = db.session.get(TemporaryLiterature, id)
    form = LiteratureForm()
    if request.method == "GET":
        form.edit.data = literature_first.id
        form.title.data = literature_first.title
        form.year_completed.data = literature_first.year_completed
        form.genre.data = literature_first.genre
        form.in_greek.data = literature_first.in_greek
        form.description.data = literature_first.description
        form.references.data = literature_first.references
        form.current_location.data = literature_first.current_location
        form.author.data = literature_first.author
    if form.validate_on_submit():
        literature_new_edit = db.session.get(TemporaryLiterature, int(form.edit.data))
        literature_new_edit.title = form.title.data
        literature_new_edit.year_completed = form.year_completed.data
        literature_new_edit.current_location = form.current_location.data
        literature_new_edit.genre = form.genre.data
        literature_new_edit.in_greek = form.in_greek.data
        literature_new_edit.description = form.description.data
        literature_new_edit.references = form.references.data
        literature_new_edit.author = form.author.data
        if form.image.data:
            file_name = secure_filename(form.image.data.filename)
            uuid_ = uuid.uuid4().hex[:8]
            file_name = f"{uuid_}_{file_name}"
            path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            new_path_for_uploading = path_for_uploading.replace('\\', '/')
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            form.image.data.save(new_path_for_uploading)
            photo = db.session.query(TemporaryImage).filter_by(
                temporary_literature_id=literature_new_edit.id).order_by(
                TemporaryImage.id.asc()).first()
            if not photo:
                photo = TemporaryImage(temporary_literature_id=literature_new_edit.id)
                db.session.add(photo)
            photo.filename = file_name
            photo.url = url_for('static', filename=f"images/uploaded_photos/{file_name}")
        if literature_first.status != "Pending":
            literature_new_edit.status = "Pending"
            confirmation_email(id=literature_first.id)
        db.session.commit()
        return redirect(url_for('literature_info_edit_user', id=literature_first.id))
    return render_template("literature_info_edit_user.html", book = literature_first, new_form = form, form_open = True, title = "Editing requests")







@app.route("/approve_literature_edit/<int:id>", methods = ['GET', 'POST'])
@admin_only
def approve_literature_edit(id):
    literature_first = db.session.get(TemporaryLiterature, id)
    new_literature = db.session.get(Literature, int(literature_first.old_id))
    new_literature.title = literature_first.title
    new_literature.in_greek = literature_first.in_greek
    new_literature.current_location = literature_first.current_location
    new_literature.genre = literature_first.genre
    new_literature.author = literature_first.author
    new_literature.year_completed = literature_first.year_completed
    new_literature.description = literature_first.description
    new_literature.references = literature_first.references
    user = db.session.query(User).filter_by(username = literature_first.username).first()
    new_log_30 = LogBook(original_id=id, title=new_literature.title,
                         username=current_user.username)
    db.session.add(new_log_30)
    if literature_first.temporary_images:
        photo = db.session.query(Image).filter_by(literature_id=new_literature.id).order_by(Image.id.asc()).first()
        if photo:
            file_name = secure_filename(literature_first.temporary_images[0].filename)
            photo.filename = file_name
            photo.url = f"/static/images/uploaded_photos/{file_name}"
            photo.literature_id = new_literature.id
            new_log_3100 = LogBook(original_id=photo.id, title=file_name,
                                 username=current_user.username)
            db.session.add(new_log_3100)
            db.session.delete(literature_first.temporary_images[0])
        else:
            file_name = secure_filename(literature_first.temporary_images[0].filename)
            photo = Image(filename = file_name, url = f"/static/images/uploaded_photos/{file_name}", literature_id = new_literature.id)
            db.session.add(photo)
            new_log_31 = LogBook(original_id=photo.id, title=file_name,
                                 username=current_user.username)
            db.session.add(new_log_31)
            db.session.delete(literature_first.temporary_images[0])
    approval_email(user_email=user.email, emperor_title=new_literature.title)
    db.session.delete(literature_first)
    db.session.commit()
    return redirect(url_for('manage_edits'))




@app.route("/approve_literature_add/<int:id>", methods=['GET', 'POST'])
@admin_only
def approve_literature_add(id):
    add_literature = db.session.get(TemporaryLiterature, id)
    new_literature = Literature(title=add_literature.title, current_location = add_literature.current_location, references= add_literature.references, in_greek = add_literature.in_greek, year_completed = add_literature.year_completed, genre = add_literature.genre,
                                description = add_literature.description, author = add_literature.author)
    user = db.session.query(User).filter_by(username = add_literature.username).first()
    db.session.add(new_literature)
    new_log_3200 = LogBook(original_id=new_literature.id, title=new_literature.title,
                         username=current_user.username)
    db.session.add(new_log_3200)
    if add_literature.temporary_images:
        file_name = secure_filename(add_literature.temporary_images[0].filename)
        photo = Image(filename = file_name, url = f"/static/images/uploaded_photos/{file_name}", literature_id = new_literature.id)
        db.session.add(photo)
        new_log_3300 = LogBook(original_id=photo.id, title=file_name,
                             username=current_user.username)
        db.session.add(new_log_3300)
        db.session.delete(add_literature.temporary_images[0])
    approval_email(user_email=user.email, emperor_title=add_literature.title)
    db.session.delete(add_literature)
    db.session.commit()
    return redirect(url_for('manage_additions'))




@app.route("/reject_literature_add/<int:id>", methods = ['GET', 'POST'])
def reject_literature_add(id):
    add_literature = db.session.get(TemporaryLiterature, id)
    add_literature.status = "Reject"
    user = db.session.query(User).filter_by(username = add_literature.username).first()
    rejection_email(user_email=user.email, emperor_title=add_literature.title)
    db.session.commit()
    return redirect(url_for('manage_additions'))

@app.route("/reject_literature_edit/<int:id>", methods=['GET', 'POST'])
def reject_literature_edit(id):
    add_literature = db.session.get(TemporaryLiterature, id)
    add_literature.status = "Reject"
    user = db.session.query(User).filter_by(username=add_literature.username).first()
    rejection_email(user_email=user.email, emperor_title=add_literature.title)
    db.session.commit()
    return redirect(url_for('manage_edits'))



@app.route("/admin_delete_literature_1/<int:id>", methods = ['GET', 'POST'])
def admin_delete_literature_1(id):
    delete_literature_temporary = db.session.get(TemporaryLiterature, id)
    if delete_literature_temporary.temporary_images:
        delete_image_temporary = delete_literature_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_literature_temporary)
    db.session.commit()
    return redirect(url_for('manage_edits'))



@app.route("/admin_delete_literature_2/<int:id>", methods = ['GET', 'POST'])
def admin_delete_literature_2(id):
    delete_literature_temporary = db.session.get(TemporaryLiterature, id)
    if delete_literature_temporary.temporary_images:
        delete_image_temporary = delete_literature_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_literature_temporary)
    db.session.commit()
    return redirect(url_for('manage_additions'))



@app.route("/admin/manage_edits_additions_users/literature_info_edit_user/<int:id>", methods = ['GET', 'POST'])
@login_required
def literature_info_edit_user(id):
    #war_first = db.session.get(TemporaryWar, id)
    form = LiteratureForm()
    literature_first = db.session.get(TemporaryLiterature, id)
    form.edit.data = literature_first.id
    form.title.data = literature_first.title
    form.year_completed.data = literature_first.year_completed
    form.genre.data = literature_first.genre
    form.in_greek.data = literature_first.in_greek
    form.description.data = literature_first.description
    form.references.data = literature_first.references
    form.current_location.data = literature_first.current_location
    form.author.data = literature_first.author

    return render_template("literature_info_edit_user.html",book = literature_first, form_open = False, title="Literature edit/addition information", new_form=form)




@app.route('/add_an_image_1/<int:id>', methods = ['GET', 'POST'])
@login_required
def add_an_image_1(id):
    form = ImageUploadForm()
    form_1 = LiteratureForm()
    form_2 = ImageEditForm()
    if current_user.user_type == "Authorised" or current_user.role == "Admin":
        if form.validate_on_submit():
            file_name = secure_filename(form.image.data.filename)
            uuid_ = uuid.uuid4().hex[:8]
            file_name = f"{uuid_}_{file_name}"
            path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            new_path_for_uploading = path_for_uploading.replace('\\', '/')
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            form.image.data.save(new_path_for_uploading)
            photo = Image(filename = file_name, url = url_for('static', filename=f"images/uploaded_photos/{file_name}"), caption = form.caption.data, literature_id = id)
            db.session.add(photo)
            db.session.commit()
            id_data = db.session.query(Image).filter_by(literature_id = id).order_by(Image.id.desc()).first()
            new_log_34 = LogBook(original_id=id_data.id, title=file_name,
                                 username=current_user.username)
            db.session.add(new_log_34)
            db.session.commit()
            new_confirmation_email(id=photo.id, category="literature")
            flash("Successfully uploaded", "success")
            return redirect(url_for('literature_info_detail', id=id))
    flash("Invalid details, please resubmit the form", "warning")
    return redirect(url_for('literature_info_detail', id=id))




#artifact



@app.route('/art_selection/artifact_info', methods= ['GET', 'POST'])
def artifact_info():
    form = ArtifactForm()
    artifact_lst = db.session.query(Artifact).all()
    return render_template('artifact_info.html', title = "Artifact",artifact_lst = artifact_lst, new_form = form, form_open = False)


@app.route('/art_selection/artifact_info/artifact_info_detail/<int:id>', methods= ['GET', 'POST'])
def artifact_info_detail(id):
    form = ArtifactForm()
    artifact_first = db.session.get(Artifact, id)
    form_1 = ImageUploadForm()
    form_2 = ImageEditForm()
    images = db.session.query(Image).filter(Image.artifact_id == id).all()
    form.edit.data = artifact_first.id
    form.title.data = artifact_first.title
    form.year_completed.data = artifact_first.year_completed
    form.in_greek.data = artifact_first.in_greek
    form.description.data = artifact_first.description
    form.references.data = artifact_first.references
    form.current_location.data = artifact_first.current_location
    return render_template('artifact_info_detail.html', title = "Artifact information",artifact = artifact_first, new_form = form, new_form_1 = form_1, new_form_2 = form_2, images =images, form_open = False, form_open_1 = False, form_open_2 = False)




@app.route('/toggle_user_type', methods=['POST'])
def toggle_user_type():
    form = ChooseForm()
    if form.validate_on_submit():
        u = db.session.get(User, int(form.choice.data))
        if u.user_type == "user":
            u.user_type = "Authorised"
        elif u.user_type == "Authorised":
            u.user_type = "user"
        db.session.commit()
    return redirect(url_for('admin'))



@app.route("/add_new_artifact", methods = ['POST', 'GET'])
@login_required
def add_new_artifact():
    form = ArtifactForm()
    artifact_lst = db.session.query(Artifact).all()
    if form.validate_on_submit() and int(form.edit.data) == -1:
        if current_user.role == "Admin":
            new_artifact = Artifact(title=form.title.data, current_location = form.current_location.data, references= form.references.data, in_greek = form.in_greek.data, year_completed = form.year_completed.data,
                                description = form.description.data )
            db.session.add(new_artifact)
            new_log_35 = LogBook(original_id=new_artifact.id, title=new_artifact.title,
                                 username=current_user.username)
            db.session.add(new_log_35)
            db.session.commit()
            # print(form.portrait.data.filename)
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                print(path_for_uploading)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                new_artifact_image = Image(filename=file_name,
                                             url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                             artifact_id=new_artifact.id)
                db.session.add(new_artifact_image)
                new_log_36 = LogBook(original_id=new_artifact_image.id, title=file_name, username=current_user.username)
                db.session.add(new_log_36)
                db.session.commit()
            return redirect(url_for("artifact_info"))
        else:
            temporary_artifact_edit = TemporaryArtifact(username=current_user.username, old_id=int(form.edit.data),
                                                                title=form.title.data,
                                                                current_location=form.current_location.data,
                                                                references=form.references.data,
                                                                in_greek=form.in_greek.data,
                                                                year_completed=form.year_completed.data,
                                                                description=form.description.data
                                                                )

            db.session.add(temporary_artifact_edit)
            db.session.commit()
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                id_data = db.session.query(TemporaryArtifact).filter_by(username = current_user.username).order_by(TemporaryArtifact.id.desc()).first()
                photo = TemporaryImage(username=current_user.username, old_id=int(form.edit.data), filename=file_name,
                                       url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                       temporary_artifact_id= id_data.id)
                db.session.add(photo)
                db.session.commit()
                confirmation_email(temporary_artifact_edit.id)
            return redirect(url_for("artifact_info"))
    return render_template('artifact_info.html', title = "Artifact", artifact_lst = artifact_lst , form_open = True, new_form = form )








@app.route('/edit_artifact/<int:id>', methods = ['POST', 'GET'])
@login_required
def edit_artifact(id):
    artifact_first = db.session.get(Artifact, id)
    form = ArtifactForm()
    form_1 = ImageUploadForm()
    form_2 = ImageEditForm()
    images = db.session.query(Image).filter(Image.artifact_id == id).all() or []
    if request.method == "GET":
        form.edit.data = artifact_first.id
        form.title.data = artifact_first.title
        form.year_completed.data = artifact_first.year_completed
        form.in_greek.data = artifact_first.in_greek
        form.description.data = artifact_first.description
        form.references.data = artifact_first.references
        form.current_location.data = artifact_first.current_location
    if form.validate_on_submit():
        if current_user.role == "Admin":
            artifact_new_edit = db.session.get(Artifact, int(form.edit.data))
            artifact_new_edit.title = form.title.data
            artifact_new_edit.year_completed =  form.year_completed.data
            artifact_new_edit.current_location= form.current_location.data
            artifact_new_edit.in_greek = form.in_greek.data
            artifact_new_edit.description = form.description.data
            artifact_new_edit.references = form.references.data
            new_log_37 = LogBook(original_id=artifact_new_edit.id, title=artifact_new_edit.title, username=current_user.username)
            db.session.add(new_log_37)
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                photo = db.session.query(Image).filter_by(artifact_id=artifact_new_edit.id).order_by(Image.id.asc()).first()
                if not photo:
                    photo = Image(artifact_id=artifact_new_edit.id)
                    db.session.add(photo)
                photo.filename = file_name
                photo.url = url_for('static', filename=f"images/uploaded_photos/{file_name}")
                new_log_38 = LogBook(original_id=photo.id, title=file_name,
                                     username=current_user.username)
                db.session.add(new_log_38)
            db.session.commit()
            return redirect(url_for('artifact_info_detail', id=artifact_new_edit.id))
        else:
            temporary_edit = TemporaryArtifact(username=current_user.username, old_id=int(form.edit.data),
                                                 title=form.title.data,
                                                 current_location=form.current_location.data,
                                                 references=form.references.data,
                                                 in_greek=form.in_greek.data,
                                                 year_completed=form.year_completed.data,
                                                 description=form.description.data
                                                 )
            db.session.add(temporary_edit)
            db.session.commit()
            if form.image.data:
                file_name = secure_filename(form.image.data.filename)
                uuid_ = uuid.uuid4().hex[:8]
                file_name = f"{uuid_}_{file_name}"
                path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                new_path_for_uploading = path_for_uploading.replace('\\', '/')
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                form.image.data.save(new_path_for_uploading)
                id_data = db.session.query(TemporaryArtifact).filter_by(username = current_user.username).order_by(TemporaryArtifact.id.desc()).first()
                photo = TemporaryImage( username = current_user.username, old_id = int(form.edit.data),filename=file_name,
                                         url=url_for('static', filename=f"images/uploaded_photos/{file_name}"),
                                         temporary_artifact_id=id_data.id)
                db.session.add(photo)
            db.session.commit()
            confirmation_email(id)
            return redirect(url_for('artifact_info_detail', id=artifact_first.id))
    return render_template("artifact_info_detail.html", id=artifact_first.id, form_open = True, form_1 = False, form_2 = False,artifact = artifact_first, new_form = form, new_form_1 = form_1, new_form_2 = form_2,title = "Artifact information", images = images)
    #return render_template("war_info.html", war = war, title = "Battle information")






@app.route('/edit_artifact_users/<int:id>', methods = ['POST', 'GET'])
@login_required
def edit_artifact_users(id):
    artifact_first = db.session.get(TemporaryArtifact, id)
    form = ArtifactForm()
    if request.method == "GET":
        form.edit.data = artifact_first.id
        form.title.data = artifact_first.title
        form.year_completed.data = artifact_first.year_completed
        form.in_greek.data = artifact_first.in_greek
        form.description.data = artifact_first.description
        form.references.data = artifact_first.references
        form.current_location.data = artifact_first.current_location
    if form.validate_on_submit():
        artifact_new_edit = db.session.get(TemporaryArtifact, int(form.edit.data))
        artifact_new_edit.title = form.title.data
        artifact_new_edit.year_completed = form.year_completed.data
        artifact_new_edit.current_location = form.current_location.data
        artifact_new_edit.in_greek = form.in_greek.data
        artifact_new_edit.description = form.description.data
        artifact_new_edit.references = form.references.data
        if form.image.data:
            file_name = secure_filename(form.image.data.filename)
            uuid_ = uuid.uuid4().hex[:8]
            file_name = f"{uuid_}_{file_name}"
            path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            new_path_for_uploading = path_for_uploading.replace('\\', '/')
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            form.image.data.save(new_path_for_uploading)
            photo = db.session.query(TemporaryImage).filter_by(
                temporary_artifact_id=artifact_new_edit.id).order_by(
                TemporaryImage.id.asc()).first()
            if not photo:
                photo = TemporaryImage(temporary_artifact_id=artifact_new_edit.id)
                db.session.add(photo)
            photo.filename = file_name
            photo.url = url_for('static', filename=f"images/uploaded_photos/{file_name}")
        if artifact_first.status != "Pending":
            artifact_new_edit.status = "Pending"
            confirmation_email(id=artifact_first.id)
        db.session.commit()
        return redirect(url_for('artifact_info_edit_user', id=artifact_first.id))
    return render_template("artifact_info_edit_user.html", artifact = artifact_first, new_form = form, form_open = True, title = "Editing requests")








@app.route("/approve_artifact_edit/<int:id>", methods = ['GET', 'POST'])
@admin_only
def approve_artifact_edit(id):
    artifact_first = db.session.get(TemporaryArtifact, id)
    new_artifact = db.session.get(Artifact, int(artifact_first.old_id))
    new_artifact.title = artifact_first.title
    new_artifact.in_greek = artifact_first.in_greek
    new_artifact.current_location = artifact_first.current_location
    new_artifact.year_completed = artifact_first.year_completed
    new_artifact.description = artifact_first.description
    new_artifact.references = artifact_first.references
    user = db.session.query(User).filter_by(username = artifact_first.username).first()
    new_log_39 = LogBook(original_id=id, title=new_artifact.title,
                         username=current_user.username)
    db.session.add(new_log_39)
    if artifact_first.temporary_images:
        photo = db.session.query(Image).filter_by(artifact_id=new_artifact.id).order_by(Image.id.asc()).first()
        if photo:
            file_name = secure_filename(artifact_first.temporary_images[0].filename)
            uuid_ = uuid.uuid4().hex[:8]
            file_name = f"{uuid_}_{file_name}"
            photo.filename = file_name
            photo.url = f"/static/images/uploaded_photos/{file_name}"
            photo.artifact_id = new_artifact.id
            db.session.delete(artifact_first.temporary_images[0])
            new_log_4000 = LogBook(original_id=photo.id, title=file_name,
                                 username=current_user.username)
            db.session.add(new_log_4000)
        else:
            file_name = secure_filename(artifact_first.temporary_images[0].filename)
            uuid_ = uuid.uuid4().hex[:8]
            file_name = f"{uuid_}_{file_name}"
            photo = Image(filename = file_name, url = f"/static/images/uploaded_photos/{file_name}", artifact_id = new_artifact.id)
            new_log_40 = LogBook(original_id=photo.id, title=file_name,
                                 username=current_user.username)
            db.session.add(new_log_40)
            db.session.add(photo)
            db.session.delete(artifact_first.temporary_images[0])
    approval_email(user_email=user.email, emperor_title=new_artifact.title)
    db.session.delete(artifact_first)
    db.session.commit()
    return redirect(url_for('manage_edits'))


@app.route("/approve_artifact_add/<int:id>", methods=['GET', 'POST'])
@admin_only
def approve_artifact_add(id):
    add_artifact = db.session.get(TemporaryArtifact, id)
    new_artifact = Artifact(title=add_artifact.title, current_location = add_artifact.current_location, references= add_artifact.references, in_greek = add_artifact.in_greek, year_completed = add_artifact.year_completed,
                                description = add_artifact.description)
    user = db.session.query(User).filter_by(username = add_artifact.username).first()
    db.session.add(new_artifact)
    new_log_4100 = LogBook(original_id=new_artifact.id, title=new_artifact.title,
                         username=current_user.username)
    db.session.add(new_log_4100)
    if add_artifact.temporary_images:
        file_name = secure_filename(add_artifact.temporary_images[0].filename)
        uuid_ = uuid.uuid4().hex[:8]
        file_name = f"{uuid_}_{file_name}"
        photo = Image(filename = file_name, url = f"/static/images/uploaded_photos/{file_name}", artifact_id = new_artifact.id)
        new_log_4200 = LogBook(original_id=photo.id, title=file_name,
                             username=current_user.username)
        db.session.add(new_log_4200)
        db.session.add(photo)
        db.session.delete(add_artifact.temporary_images[0])
    approval_email(user_email=user.email, emperor_title=add_artifact.title)
    db.session.delete(add_artifact)
    db.session.commit()
    return redirect(url_for('manage_additions'))



@app.route("/reject_artifact_add/<int:id>", methods = ['GET', 'POST'])
def reject_artifact_add(id):
    add_artifact = db.session.get(TemporaryArtifact, id)
    add_artifact.status = "Reject"
    user = db.session.query(User).filter_by(username = add_artifact.username).first()
    rejection_email(user_email=user.email, emperor_title=add_artifact.title)
    db.session.commit()
    return redirect(url_for('manage_additions'))

@app.route("/reject_artifact_edit/<int:id>", methods=['GET', 'POST'])
def reject_artifact_edit(id):
    add_artifact = db.session.get(TemporaryArtifact, id)
    add_artifact.status = "Reject"
    user = db.session.query(User).filter_by(username = add_artifact.username).first()
    rejection_email(user_email=user.email, emperor_title=add_artifact.title)
    db.session.commit()
    return redirect(url_for('manage_edits'))





@app.route("/admin_delete_artifact_1/<int:id>", methods = ['GET', 'POST'])
def admin_delete_artifact_1(id):
    delete_artifact_temporary = db.session.get(TemporaryArtifact, id)
    if delete_artifact_temporary.temporary_images:
        delete_image_temporary = delete_artifact_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_artifact_temporary)
    db.session.commit()
    return redirect(url_for('manage_edits'))



@app.route("/admin_delete_artifact_2/<int:id>", methods = ['GET', 'POST'])
def admin_delete_artifact_2(id):
    delete_artifact_temporary = db.session.get(TemporaryArtifact, id)
    if delete_artifact_temporary.temporary_images:
        delete_image_temporary = delete_artifact_temporary.temporary_images[0]
        db.session.delete(delete_image_temporary)
    db.session.delete(delete_artifact_temporary)
    db.session.commit()
    return redirect(url_for('manage_additions'))



@app.route("/admin/manage_edits_additions_users/artifact_info_edit_user/<int:id>", methods = ['GET', 'POST'])
@login_required
def artifact_info_edit_user(id):
    #war_first = db.session.get(TemporaryWar, id)
    form = ArtifactForm()
    artifact_first = db.session.get(TemporaryArtifact, id)
    form.edit.data = artifact_first.id
    form.title.data = artifact_first.title
    form.year_completed.data = artifact_first.year_completed
    form.in_greek.data = artifact_first.in_greek
    form.description.data = artifact_first.description
    form.references.data = artifact_first.references
    form.current_location.data = artifact_first.current_location

    return render_template("artifact_info_edit_user.html",artifact = artifact_first, form_open = False, title="Artifacts edit/addition information", new_form=form)







@app.route('/add_an_image_2/<int:id>', methods = ['GET', 'POST'])
@login_required
def add_an_image_2(id):
    form = ImageUploadForm()
    form_1 = ArtifactForm()
    form_2 = ImageEditForm()
    if current_user.user_type == "Authorised" or current_user.role == "Admin":
        if form.validate_on_submit():
            file_name = secure_filename(form.image.data.filename)
            uuid_ = uuid.uuid4().hex[:8]
            file_name = f"{uuid_}_{file_name}"
            path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            new_path_for_uploading = path_for_uploading.replace('\\', '/')
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            form.image.data.save(new_path_for_uploading)
            photo = Image(filename = file_name, url = url_for('static', filename=f"images/uploaded_photos/{file_name}"), caption = form.caption.data, artifact_id = id)
            db.session.add(photo)
            db.session.commit()
            id_data = db.session.query(Image).filter_by(architecture_id = id).order_by(Image.id.desc()).first()
            new_log_43 = LogBook(original_id=id_data.id, title=file_name,
                                 username=current_user.username)
            db.session.add(new_log_43)
            db.session.commit()
            new_confirmation_email(id=photo.id, category="artifact")
            flash("Successfully uploaded", "success")
            return redirect(url_for('artifact_info_detail', id=id))
    flash("Invalid details, please resubmit the form", "warning")
    return redirect(url_for('artifact_info_detail', id=id))













@app.route('/admin/de_admin/<int:id>', methods=['POST', 'GET'])
@admin_only
@login_required
def de_admin(id):
    if current_user.usertype == "Autocrat":
        form = ChooseForm()
        q = db.select(User)
        user_lst = db.session.scalars(q)
        user = db.session.get(User, id)
        user.role = "Normal"
        flash("User role has now been changed to normal", "success")
        db.session.commit()
    else:
        abort(403)
    return render_template("admin.html", title = "Admin", user_lst = user_lst, form = form)








@app.route("/change_pw",methods=['POST','GET'])
def change_pw():
    form = ChangePasswordForm()
    if form.validate_on_submit() and current_user.check_password(form.password.data):
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash("Password has been changed!",'success')
        return redirect(url_for('account'))
    return render_template('generic_form.html',title='Change Password', form=form)

@app.route("/change_email",methods=['POST','GET'])
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit() and current_user.check_password(form.password.data):
        current_user.email = form.new_email.data
        db.session.commit()
        flash("Email has been updated!",'success')
        return redirect(url_for('account'))
    return render_template('generic_form.html',title='Change Email', form=form)


@app.route("/register_verify",methods=['POST','GET'])
def register_verify():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegisterForm()
    if form.validate_on_submit():
        email_data = form.email.data
        query_email = db.session.query(Verification).filter_by(email = email_data).order_by(Verification.id.desc()).first()
        if not query_email:
            flash("Email is not correct!", 'danger')
        else:
            if query_email.verification_code == form.verification_code.data:
                new_user = User(username=form.username.data, email=form.email.data)
                new_user.set_password(form.password.data)
                db.session.add(new_user)
                db.session.commit()
                login_user(user=new_user)
                return redirect(url_for('register_emails_'))
            else:
                flash("Verification code is not correct!", 'danger')
                return redirect(url_for('register_verify'))
    return render_template('generic_form.html', title='Verify',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(or_(User.username == form.username.data, User.email == form.username.data)))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('generic_form.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Error handlers
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

# Error handler for 403 Forbidden
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403

# Handler for 404 Not Found
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413

# 500 Internal Server Error
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500