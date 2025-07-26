import random
#from ensurepip import bootstrap
from wtforms import form, ValidationError
#from time import timezone
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone, timedelta
from flask import Flask, url_for, render_template
import flask_mail, itsdangerous
from flask_mail import Mail, Message
from itsdangerous import  URLSafeSerializer, SignatureExpired, BadSignature, URLSafeTimedSerializer
from pycparser.ply.lex import TOKEN
from app.models import User, Verification
from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory,session, jsonify
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required


# from pymupdf import message



from config import Config
from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.new_file import db, login

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.config.from_object(Config)
#db = SQLAlchemy(app)
#login = LoginManager(app)
login.login_view = 'login'
login.init_app(app)
db.init_app(app)
app.config.update(
    SECRET_KEY = "11451419191810YJSP893kksk__",
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 587,
    MAIL_USERNAME = "chenyingshu1234@gmail.com",
    MAIL_PASSWORD = "vumkqibpmcfyjvaw",
    MAIL_USE_TLS = True,
)

mail = Mail(app)
signer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
TOKEN_MAX_AGE = 60*60*24

import os
BASE = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE, 'static', 'images', 'uploaded_photos')
app.config['UPLOAD_FOLDER_TEMPORARY'] = os.path.join(BASE, 'static', 'images', 'temporary')
app.config['MAX_CONTENT_LENGTH'] = 2000*1024*1024



def verification_email(user_email: str) -> bool:
    user = User.query.filter_by(email = user_email).first()
    if not user:
        code = ''.join(random.choices("0123456789", k=6))
        verified = Verification(email=user_email, verification_code = code)
        #user = Verification(email=user_email)
        db.session.add(verified)
        #db.session.add(user)
        db.session.commit()
        html = render_template("email_verify.html", code=code)
        msg = Message(
            sender= "chenyingshu1234@gmail.com",
            subject="Please confirm your email",
            recipients=[user_email],
            html=html,
        )
        mail.send(msg)
        return True
    else:
        return False

def confirmation_email():
    emails = db.session.query(User).filter_by(role = "Admin").all()
    if emails:
        html = render_template("confirmation_sent.html", user = current_user.username)
        for email in emails:
            msg = Message(sender="chenyingshu1234@gmail.com",
                          subject="A new edit or addition",
                          recipients = [email.email],
                          html=html,)
            mail.send(msg)


def approval_email(user_email: str, emperor_title: str):
        html = render_template("approval_sent.html", title = emperor_title )
        msg = Message(sender="chenyingshu1234@gmail.com",
                          subject="Approval",
                          recipients = [user_email],
                          html=html,)
        mail.send(msg)



def rejection_email(user_email: str, emperor_title: str):
        html = render_template("rejection.sent.html", title = emperor_title )
        msg = Message(sender="chenyingshu1234@gmail.com",
                          subject="Rejection",
                          recipients = [user_email],
                          html=html,)
        mail.send(msg)


def deleting_expired_auto():
    with app.app_context():
        from datetime import datetime, timezone, timedelta
        from app.models import User, Verification
        from app.new_file import db
        the_threshold = datetime.now(timezone.utc) - timedelta(minutes=9)
        all_record = Verification.query.all()
        for each_record in all_record:
            try:
                raw = each_record.created_at.replace(" ", "T")
                creation_time = datetime.fromisoformat(raw)
                if creation_time < the_threshold:
                    db.session.delete(each_record)
            except Exception as e:
                #db.session.rollback()
                print(f"Invalid format: {each_record.created_at}-{e}")
        db.session.commit()


def schedule_start():
    schedule = BackgroundScheduler()
    schedule.add_job(deleting_expired_auto, 'interval', minutes = 10, misfire_grace_time=2)
    schedule.start()


from app import views, models
from app.debug_utils import reset_db


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, sa=sa, so=so, reset_db=reset_db)
