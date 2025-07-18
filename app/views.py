from os import write
from functools import wraps
import os
from random import randint
from pandas import date_range
from werkzeug.utils import secure_filename
from app import signer, TOKEN_MAX_AGE, verification_email
from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory,session, jsonify
from unicodedata import category
from urllib3.connection import port_by_scheme

from app import app
from app.models import User, Emperor, \
    Verification, Invitation, Image
from app.forms import ChooseForm, LoginForm, ChangePasswordForm, ChangeEmailForm, RegisterForm, RegisterEmail, \
    AdminCodeForm, InvitationCodeForm, AllEmperorForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app.new_file import db
from urllib.parse import urlsplit
from sqlalchemy import or_
import csv
import io
import datetime
import random
import json
from sqlalchemy.exc import IntegrityError
import google.generativeai as genai
def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != "Admin":
            return redirect(url_for('home'))
        return func(*args, **kwargs)
    return wrapper

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
    return render_template('macedonians.html', title = "Macedonian dynasty", macedonian_lst = macedonian_lst, new_form = form)

@app.route("/dynasties/macedonians/<int:id>", methods=['GET','POST'])
def macedonian_emperors(id):
    #m_e = db.session.query(Emperor).filter_by(dynasty = 'Macedonian').all()
    m_e = db.session.get(Emperor, id)
    return render_template("macedonian_emperors.html", m_e = m_e, title = "Macedonian dynasty")


@app.route("/account")
@login_required
def account():
    form = ChooseForm()
    invitation = db.session.query(Invitation).filter_by(user_id = current_user.id).first()
    choose_form = ChooseForm()
    new_form = AdminCodeForm()
    return render_template('account.html', title="Account", choose_form = choose_form, form = form, new_form = new_form, invitation = invitation)


@app.route("/register_emails_", methods = ['GET', 'POST'])
def register_emails_():
    form = RegisterEmail()
    if form.validate_on_submit():
        email_data = form.email.data.strip().lower()
        success = verification_email(email_data)
        if success:
            flash("Check your inbox for the verification code.", "success")
            return redirect(url_for('register_verify'))
        else:
            flash("This email is already registered", "warning")
            return redirect(url_for('register_emails_'))
    return render_template('generic_form.html', title = "Register", form = form)


@app.route("/change_to_admin", methods = ['POST'])
def change_to_admin():
    form = AdminCodeForm()
    u = db.session.get(User, current_user.id)
    t = db.session.query(Invitation).filter_by(user_id = current_user.id).first()
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
def add_new_emperor():
    form = AllEmperorForm()
    if form.validate_on_submit() and int(form.edit.data) == -1:
        new_emperor = Emperor(title = form.title.data, in_greek = form.in_greek.data, birth = form.birth.data, death = form.death.data, reign = form.reign.data, life = form.life.data, dynasty = form.dynasty.data)
        db.session.add(new_emperor)
        db.session.commit()
        if form.portrait.data:
            file_name = secure_filename(form.portrait.data.filename)
            path_for_uploading = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            form.portrait.data.save(path_for_uploading)
            new_emperor_portrait = Image(filename = file_name, url = url_for('static', filename =f"images/uploaded_photos/{file_name}"), emperor_title = form.title.data)
            db.session.add(new_emperor_portrait)
            db.session.commit()

    return redirect(url_for('macedonians'))



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



@app.route('/de_admin/<int:id>', methods=['POST', 'GET'])
def de_admin(id):
    form = ChooseForm()
    q = db.select(User)
    user_lst = db.session.scalars(q)
    user = db.session.get(User, id)
    user.role = "Normal"
    flash("User role has now been changed to normal", "success")
    db.session.commit()
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