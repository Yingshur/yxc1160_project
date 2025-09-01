import glob
from sqlalchemy import text
from app.decorators.management_functions import admin_only
from flask import render_template, redirect, url_for
from app.models import User, Emperor, \
    Verification, Invitation, Image, TemporaryEmperor, TemporaryImage, War, TemporaryWar, Architecture, TemporaryArchitecture, Literature, TemporaryLiterature, Artifact, TemporaryArtifact, LogBook, Deletion, Version, CurrentVersion, NewVersion
from app.forms import ChooseForm, LoginForm, ChangePasswordForm, ChangeEmailForm, RegisterForm, RegisterEmail, \
    AdminCodeForm, InvitationCodeForm, AllEmperorForm, WarForm, ArchitectureForm, ImageEditForm, ImageUploadForm, LiteratureForm, ArtifactForm, DeleteForm, ChatForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
from app.new_file import db
import csv
from flask import Blueprint
import os

version_control_bp = Blueprint("version_control_bp", __name__)


@version_control_bp.route('/versions_', methods = ["GET", "POST"], endpoint="versions_")
@login_required
@admin_only
def versions_():
    versions = db.session.query(Version).order_by(Version.id.desc()).all()
    current_versions = db.session.query(CurrentVersion).all()
    new_version = db.session.query(NewVersion).all()
    return render_template("version_control.html", title = "Version control", versions = versions, current_versions = current_versions, new_version = new_version)


@version_control_bp.route('/versions_control_/<int:id>', methods = ["GET", "POST"], endpoint = "version_control_")
@login_required
@admin_only
def version_control_(id):
    version = db.session.get(Version, id)
    versions = db.session.query(Version).order_by(Version.id.desc()).all()
    first_version = versions[-1]
    unique_number_ = version.unique
    models = [Image, Architecture, Emperor, War, Literature, Artifact]
    with db.engine.begin() as context:
        context.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        for each in models:
            each.__table__.drop(context, checkfirst= True)
        for each in models:
            each.__table__.create(context, checkfirst= True)
        context.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    model_table_names = {model.__tablename__: model for model in models}
    dir_versions = os.environ.get("BACKUP_DIR", os.path.join(os.getcwd(), "old_versions"))
    os.makedirs(dir_versions, exist_ok=True)
    for path_of_file in glob.glob(os.path.join(dir_versions, "*.csv")):
        name_of_table_full = os.path.splitext(os.path.basename(path_of_file))[0]
        actual_table_name = name_of_table_full[:-33]

        if name_of_table_full[-32:] == unique_number_ and actual_table_name in model_table_names:
            with open(path_of_file, "r", encoding="utf-8-sig") as csv_file:
                dictionary_reader = csv.DictReader(csv_file)
                table_dictionary = [dict(row) for row in dictionary_reader]
                for item in table_dictionary:
                    for a, b in item.items():
                        if b in ("", ',', None, ''):
                            item[a] = None
                    #item.pop("id", None)
                add_data = [model_table_names[actual_table_name](**row) for row in table_dictionary]
                db.session.add_all(add_data)
    #db.session.delete(version)
    current_version = db.session.query(CurrentVersion).first()
    if current_version:
        if id == first_version.id:
            current_version.username = current_user.username
            current_version.time_version = "-"
        else:
            current_version.username = version.username
            latest_edit = db.session.query(Version).filter(Version.id < id).order_by(Version.id.desc()).first()
            current_version.time_version = latest_edit.created_at
    db.session.commit()
    return redirect(url_for("version_control_bp.versions_"))


@version_control_bp.route('/versions_control_overwrite/<int:id>', methods = ["GET", "POST"], endpoint = "version_control_overwrite")
@login_required
@admin_only
def version_control_overwrite(id):
    version = db.session.get(NewVersion, id)
    unique_number_ = version.unique
    latest_edit = db.session.query(Version).order_by(Version.id.desc()).first()
    with db.engine.begin() as context:
        context.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        models = [Image, Architecture, Emperor, War, Literature, Artifact]
        for each in models:
            each.__table__.drop(context, checkfirst=True)
        for each in models:
            each.__table__.create(context, checkfirst=True)
        context.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    dir_versions = os.environ.get("BACKUP_DIR", os.path.join(os.getcwd(), "new_versions"))
    os.makedirs(dir_versions, exist_ok=True)
    model_table_names = {model.__tablename__: model for model in models}
    for path_of_file in glob.glob(
            os.path.join(dir_versions, "*.csv")):
        name_of_table_full = os.path.splitext(os.path.basename(path_of_file))[0]
        actual_table_name = name_of_table_full[:-33]
        if name_of_table_full[-32:] == unique_number_ and actual_table_name in model_table_names:
            with open(path_of_file, "r", encoding="utf-8-sig") as csv_file:
                dictionary_reader = csv.DictReader(csv_file)
                table_dictionary = [dict(row) for row in dictionary_reader]
                for item in table_dictionary:
                    for a, b in item.items():
                        if b in ("", ',', None, ''):
                            item[a] = None
                    # item.pop("id", None)
                add_data = [model_table_names[actual_table_name](**row) for row in table_dictionary]
                db.session.add_all(add_data)
    #db.session.delete(version)
    current_version = db.session.query(CurrentVersion).first()
    if current_version:
        current_version.username = version.username
        current_version.time_version = latest_edit.created_at
    db.session.commit()
    return redirect(url_for("version_control_bp.versions_"))


@version_control_bp.route("/logbook", methods=["GET", "POST"], endpoint = "logbook")
@login_required
def logbook():
    logbook = db.session.query(LogBook).all()
    return render_template('logbook.html', title = "Logbook", logbook =logbook)
