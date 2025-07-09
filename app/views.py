from os import write
from functools import wraps
from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory,session, jsonify
from unicodedata import category
from urllib3.connection import port_by_scheme

from app import app
from app.models import User, UniversityEmail, Appointment, Event, Enrollment, Psychologist, BookingLog
from app.forms import ChooseForm, LoginForm, ChangePasswordForm, ChangeEmailForm, RegisterForm, RegisterEmail, \
    RegisterEmailVerify, EventsForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
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
    return render_template('home.html', title="Home")

@app.route("/account")
@login_required
def account():
    form = ChooseForm()
    choose_form = ChooseForm()
    q = db.select(Enrollment).where(Enrollment.username == current_user.username)
    list_of_enrollments = db.session.scalars(q)
    psychologist = db.session.get(Psychologist, current_user.id)
    p = db.select(Appointment).where(Appointment.user_name == current_user.username)
    list_of_appointments = db.session.scalars(p)
    return render_template('account.html', title="Account", list_of_enrollments = list_of_enrollments, choose_form = choose_form, psychologist =psychologist, form = form, list_of_appointments = list_of_appointments)

@app.route("/admin")
@login_required
@admin_only
def admin():
    # if current_user.role != "Admin":
    #     return redirect(url_for('home'))
    form = ChooseForm()
    q = db.select(User)
    user_lst = db.session.scalars(q)
    q = db.select(Enrollment)
    list_of_enrollments = db.session.scalars(q)
    p = db.select(Psychologist)
    list_of_psychologists = db.session.scalars(p)
    p = db.select(Appointment)
    list_of_appointments = db.session.scalars(p)
    return render_template('admin.html', title="Admin", user_lst=user_lst, form=form, list_of_enrollments = list_of_enrollments, list_of_psychologists = list_of_psychologists, list_of_appointments = list_of_appointments, choose_form = form)

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

@app.route('/toggle_user_role', methods=['POST'])
def toggle_user_role():
    form = ChooseForm()
    if form.validate_on_submit():
        u = db.session.get(User, int(form.choice.data))
        q = db.select(User).where((User.role == "Admin") & (User.id != u.id))
        first = db.session.scalars(q).first()
        if not first:
            flash("You can't drop your admin role if there are no other admin users!", "danger")
        elif u.id == current_user.id:
                logout_user()
                u.role = "Normal"
                db.session.commit()
                return redirect(url_for('home'))
        else:
            # u.role = "Normal" if u.role == "Admin" else "Admin"
            if u.role == "Normal":
                u.role = "Organiser"
            elif u.role == "Organiser":
                u.role = "Admin"
            elif u.role == "Admin":
                u.role = "Normal"
            db.session.commit()
    return redirect(url_for('admin'))


@app.route('/toggle_user_type', methods=['POST'])
def toggle_user_type():
    form = ChooseForm()
    if form.validate_on_submit():
        u = db.session.get(User, int(form.choice.data))
        q = db.select(User).where((User.user_type == "Psychologist") & (User.id != u.id))
        first = db.session.scalars(q).first()
        if not first:
            flash("You can't drop your psychologist role if there are no other psychologist users!", "danger")
        elif u.id == current_user.id:
                logout_user()
                u.user_type = "user"
                db.session.commit()
                return redirect(url_for('home'))
        else:
            # u.role = "Normal" if u.role == "Admin" else "Admin"
            if u.user_type == "user":
                u.user_type = "Psychologist"
                #new = Psychologist(id = u.id, username = u.username, email = u.email, password_hash=u.password_hash, user_type= "Psychologist")
                #db.session.delete(u)
                #db.session.add(new)
                db.session.execute(sa.insert(Psychologist.__table__).values(id=u.id))
                db.session.commit()
            elif u.user_type == "Psychologist":
                u.user_type = "user"
               #new = User(id = u.id, username = u.username, email = u.email, password_hash=u.password_hash)
                #db.session.delete(u)
                #db.session.add(new)
                db.session.execute(sa.delete(Psychologist).where(Psychologist.id==u.id))
                db.session.commit()
    return redirect(url_for('admin'))






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

@app.route("/register",methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegisterForm()
    if form.validate_on_submit():
        query_email = db.select(UniversityEmail).where(UniversityEmail.email == form.email.data)
        check_email = db.session.scalars(query_email).first()
        if check_email:
            new_user=User(username=form.username.data, email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(user=new_user)
        else:
            flash("Error: not a valid university email!",'danger')
            return redirect(url_for('register_email'))
        return redirect(url_for('account'))

    return render_template('generic_form.html', title='Register',form=form)

@app.route("/register_email",methods=['POST','GET'])
def register_email():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegisterEmail()
    if form.validate_on_submit():
        query_email = db.select(UniversityEmail).where(UniversityEmail.email==form.email.data)
        check_email = db.session.scalars(query_email).first()
        if check_email:
            verify_code = str(random.randint(100000,999999))
            session['email'] = form.email.data
            session['verify_code'] = verify_code

            form = RegisterEmailVerify(email=check_email.email)
            flash(f"Verification code {verify_code} was emailed to you. Check your email!",'success')
            return render_template('register_verify.html', title='Verify', form=form)
        else:
            flash("Email not found! Try to check your university email again!",'danger')
            return redirect(url_for('register_email'))
    return render_template('generic_form.html', title='Register',form=form)

@app.route("/register_verify",methods=['POST','GET'])
def register_verify():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegisterEmailVerify()
    if form.validate_on_submit() and form.verify.data == session['verify_code']:
        query_email = db.select(UniversityEmail).where(UniversityEmail.email==form.email.data)
        check_email = db.session.scalars(query_email).first()
        if check_email:
            form = RegisterForm(username=check_email.username, email=check_email.email)
            return render_template('register_complete.html', title='Register', form=form)
    else:
        flash("Verification code not correct!",'danger')
        return render_template('register_verify.html', title='Verify', form=form)
    return render_template('register_verify.html', title='Verify',form=form)

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

@app.route('/events',  methods=['GET', 'POST'])
@login_required
def events():
    choose_form = ChooseForm()
    q = db.select(Event)
    list_of_events = db.session.scalars(q)
    return render_template('events.html', title="Events", list_of_events = list_of_events, choose_form = choose_form)

def generate_schedule():
    today = datetime.datetime.today().date()
    slots_per_day = ["09:00", "11:00", "14:00", "16:00"]
    # slots_per_day = [
    #     {"start": "09:00", "availability": True},
    #     {"start": "11:00", "availability": True},
    #     {"start": "14:00", "availability": True},
    #     {"start": "16:00", "availability": True},
    # ]
    schedule = []
    for i in range(7):
        date = today + datetime.timedelta(days=i)
        schedule.append({
            "weekday": date.strftime("%A"),
            "date": date.strftime("%m-%d"),
            "slots": slots_per_day
        })
    return schedule

def check_availability():
    q = db.select(Appointment).order_by(Appointment.date, Appointment.slot)
    unavailable_slots = db.session.scalars(q).all()
    return unavailable_slots

@app.route('/appointments')
def appointments():
    form = ChooseForm()
    schedule = generate_schedule()
    unavailable_slots = check_availability()
    return render_template('appointment.html', title='Appointment', schedule=schedule, form=form, unavailable_slots=unavailable_slots)




@app.route('/toggle_user_availability', methods=['POST'])
def toggle_user_availability():
    form = ChooseForm()
    if form.validate_on_submit():
        u = db.session.get(Psychologist, int(form.choice.data))
        #q = db.select(User).where((User.user_type == "Psychologist") & (User.id != u.id))
        #first = db.session.scalars(q).first()
        #if not first:
            #flash("You can't drop your psychologist role if there are no other psychologist users!", "danger")
        #elif u.id == current_user.id:
                #logout_user()
                #u.user_type = "user"
                #db.session.commit()
                #return redirect(url_for('home'))
        #else:
            # u.role = "Normal" if u.role == "Admin" else "Admin"
        if u.availability == "Available":
            u.availability = "Unavailable"

            Appointment.query.filter_by(id=u.id).delete()
            BookingLog.query.filter_by(id=u.id).delete()
            # new = Psychologist(id = u.id, username = u.username, email = u.email, password_hash=u.password_hash, user_type= "Psychologist")
            # db.session.delete(u)
            # db.session.add(new)
            #db.session.execute(sa.insert(Psychologist.__table__).values(id=u.id))
            db.session.commit()
        elif u.availability == "Unavailable":
            u.availability = "Available"
            # new = User(id = u.id, username = u.username, email = u.email, password_hash=u.password_hash)
            # db.session.delete(u)
            # db.session.add(new)
            #db.session.execute(sa.delete(Psychologist).where(Psychologist.id == u.id))
            db.session.commit()
    return redirect(url_for('account'))




@app.route('/toggle_user_availability_/<int:psychologist_id>', methods=['POST'])
def toggle_user_availability_(psychologist_id):
    form = ChooseForm()
    if form.validate_on_submit():
        u = db.session.get(Psychologist, int(psychologist_id))
        #q = db.select(User).where((User.user_type == "Psychologist") & (User.id != u.id))
        #first = db.session.scalars(q).first()
        #if not first:
            #flash("You can't drop your psychologist role if there are no other psychologist users!", "danger")
        #elif u.id == current_user.id:
                #logout_user()
                #u.user_type = "user"
                #db.session.commit()
                #return redirect(url_for('home'))
        #else:
            # u.role = "Normal" if u.role == "Admin" else "Admin"
        if u.availability == "Available":
            u.availability = "Unavailable"

            Appointment.query.filter_by(id=u.id).delete()
            BookingLog.query.filter_by(id=u.id).delete()
            # new = Psychologist(id = u.id, username = u.username, email = u.email, password_hash=u.password_hash, user_type= "Psychologist")
            # db.session.delete(u)
            # db.session.add(new)
            #db.session.execute(sa.insert(Psychologist.__table__).values(id=u.id))
            db.session.commit()
        elif u.availability == "Unavailable":
            u.availability = "Available"
            # new = User(id = u.id, username = u.username, email = u.email, password_hash=u.password_hash)
            # db.session.delete(u)
            # db.session.add(new)
            #db.session.execute(sa.delete(Psychologist).where(Psychologist.id == u.id))
            db.session.commit()
    return redirect(url_for('admin'))



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