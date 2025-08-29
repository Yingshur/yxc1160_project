
import uuid
from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory,session, jsonify
from app.mixed.emails import verification_email, confirmation_email, approval_email, new_confirmation_email, rejection_email
import folium
from app.models import User, Emperor, \
    Verification, Invitation, Image, TemporaryEmperor, TemporaryImage, War, TemporaryWar, Architecture, TemporaryArchitecture, Literature, TemporaryLiterature, Artifact, TemporaryArtifact, LogBook, Deletion, Version, CurrentVersion, NewVersion
from app.forms import ChooseForm, LoginForm, ChangePasswordForm, ChangeEmailForm, RegisterForm, RegisterEmail
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app.new_file import db
from urllib.parse import urlsplit
from sqlalchemy import or_, and_
from flask import Blueprint

login_logout_bp = Blueprint("login_logout_bp", __name__)


@login_logout_bp.route("/register_emails_", methods = ['GET', 'POST'], endpoint = "register_emails_")
def register_emails_():
    form = RegisterEmail()
    if form.validate_on_submit():
        email_data = form.email.data.strip().lower()
        success = verification_email(email_data)
        if success:
            flash("Check your inbox for the verification code, the code is valid for ten minutes.", "success")
            return redirect(url_for('login_logout_bp.register_verify'))
        else:
            flash("This email is already registered", "warning")
            return redirect(url_for('login_logout_bp.register_emails_'))
    return render_template('register_form.html', title = "Register", form = form)


@login_logout_bp.route("/register_verify",methods=['POST','GET'], endpoint = "register_verify")
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
                return redirect(url_for('home_bp.home'))
            else:
                flash("Verification code is not correct!", 'danger')
                return redirect(url_for('login_logout_bp.register_verify'))
    return render_template('generic_form.html', title='Verify',form=form)


@login_logout_bp.route('/login', methods=['GET', 'POST'], endpoint = "login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(or_(User.username == form.username.data, User.email == form.username.data)))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login_logout_bp.login'))
        session_token = str(uuid.uuid4())
        user_now = db.session.query(User).filter(or_(User.username == form.username.data, User.email == form.username.data)).first()
        user_now.active_session = session_token
        current_version = db.session.query(CurrentVersion).first()
        db.session.commit()
        login_user(user)
        session['active_session'] = session_token
        if user_now.role != "Admin":
            pass
        else:
            if current_version is not None:
                pass
            else:
                current_version = CurrentVersion(username=current_user.username, time_version="-")
                db.session.add(current_version)
                db.session.commit()
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home_bp.home')
        return redirect(next_page)
    return render_template('generic_form.html', title='Sign In', form=form)


@login_logout_bp.route('/logout', endpoint = "logout")
def logout():
    user = db.session.get(User, current_user.id)
    if user:
        current_user.active_session = None
        db.session.commit()
    logout_user()
    session.clear()
    response = redirect(url_for('home_bp.home'))
    response.set_cookie('remember_token', '', expires=0)
    return response

