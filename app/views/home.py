from functools import wraps
from random import randint
from sqlalchemy import text
import threading
from flask import render_template, redirect, url_for, flash
from app.models import User, Invitation, TemporaryEmperor, TemporaryWar, TemporaryArchitecture, TemporaryLiterature, TemporaryArtifact,  Deletion
from app.forms import ChooseForm, ChangePasswordForm, ChangeEmailForm, \
    AdminCodeForm, DeleteForm
from flask_login import current_user, login_required
from app.new_file import db
from flask import Blueprint
import os
from app.mixed.delete_unused_images import delete_unused_images
from app.views.chatbot import client, model_ready, readiness_test, client_setting, background_chatbot

home_bp = Blueprint("home_bp", __name__)


@home_bp.route("/", endpoint = "home")
def home():
    if not readiness_test():
        threading.Thread(target=background_chatbot, daemon=True).start()
    return render_template('home.html', title="Roman Empire")


@home_bp.route("/account", endpoint = "account")
@login_required
def account():
    form = ChooseForm()
    delete_form = DeleteForm()
    invitation = db.session.query(Invitation).filter_by(user_id = current_user.id).order_by(Invitation.id.desc()).first()
    choose_form = ChooseForm()
    new_form = AdminCodeForm()
    return render_template('account.html', title="Account", choose_form = choose_form, form = form, new_form = new_form, invitation = invitation, delete_form = delete_form)


@home_bp.route("/account/change_to_admin", methods = ['POST'], endpoint = "change_to_admin")
@login_required
def change_to_admin():
    form = AdminCodeForm()
    u = db.session.get(User, current_user.id)
    t = db.session.query(Invitation).filter_by(user_id = current_user.id).order_by(Invitation.id.desc()).first()
    if form.validate_on_submit() :
        if form.code.data == t.code and u.role != "Admin":
            u = db.session.get(User, current_user.id)
            u.role = "Admin"
            if u.user_type == "Authorised":
                u.user_type = "user"
            flash("Role changed to admin", "success")
            db.session.delete(t)
            db.session.commit()
            return redirect(url_for('home_bp.account'))
        elif u.role == "Admin":
            flash("You are already an admin", "warning")
            return redirect(url_for('home_bp.account'))
        elif form.code.data != t.code:
            flash("Code is not correct", "danger")
            return redirect(url_for('home_bp.account'))

    return render_template("account.html", new_form = form, title = "Account")


@home_bp.route("/account_deletion_code", methods = ['GET','POST'], endpoint = "account_deletion_code")
@login_required
def account_deletion_code():
    code = randint(10**8, 10**9-1)
    flash(f"Code for account deletion is {code}", "warning")
    code_1 = Deletion(code = code, user_id = current_user.id)
    db.session.add(code_1)
    db.session.commit()
    return redirect(url_for('home_bp.account'))


@home_bp.route("/account_deletion", methods = ['GET','POST'], endpoint = "account_deletion")
@login_required
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
            return redirect(url_for('home_bp.home'))
    form = ChooseForm()
    invitation = db.session.query(Invitation).filter_by(user_id=current_user.id).order_by(Invitation.id.desc()).first()
    choose_form = ChooseForm()
    new_form = AdminCodeForm()
    return render_template('account.html', title="Account", choose_form=choose_form, form=form, new_form=new_form, delete_form = delete_form,
                           invitation=invitation)

@home_bp.route("/change_pw",methods=['POST','GET'], endpoint = "change_pw")
@login_required
def change_pw():
    form = ChangePasswordForm()
    if form.validate_on_submit() and current_user.check_password(form.password.data):
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash("Password has been changed!",'success')
        return redirect(url_for('home_bp.account'))
    return render_template('generic_form.html',title='Change Password', form=form)



@home_bp.route("/change_email",methods=['POST','GET'], endpoint = "change_email")
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit() and current_user.check_password(form.password.data):
        current_user.email = form.new_email.data
        db.session.commit()
        flash("Email has been updated!",'success')
        return redirect(url_for('home_bp.account'))
    return render_template('generic_form.html',title='Change Email', form=form)


@home_bp.route("/manage_edits_additions_users", methods = ['GET', 'POST'], endpoint = "manage_edits_additions_users")
@login_required
def manage_edits_additions_users():
    total_list = db.session.query(TemporaryEmperor).all()
    total_list_1 = db.session.query(TemporaryWar).all()
    total_list_2 = db.session.query(TemporaryArchitecture).all()
    total_list_3 = db.session.query(TemporaryLiterature).all()
    total_list_4 = db.session.query(TemporaryArtifact).all()
    return render_template('manage_edits_additions_users.html', title = "Manage edits and additions", total_list = total_list, total_list_1 = total_list_1, total_list_2 = total_list_2, total_list_3 = total_list_3, total_list_4 = total_list_4)
