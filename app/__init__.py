import random
import uuid
#from ensurepip import bootstrap
from wtforms import form, ValidationError
import time
import os
import pymysql
from app.new_file import db
from flask import Flask, url_for, render_template, request, redirect,session, flash
import flask_mail, itsdangerous
from flask_mail import Mail, Message
from itsdangerous import  URLSafeSerializer, SignatureExpired, BadSignature, URLSafeTimedSerializer
from app.models import User, Verification, Version
from app.forms import ChatForm
import pymysql
# from pymupdf import message
from flask_login import current_user, logout_user

from config import Config
from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.new_file import db, login
import csv
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
pymysql.install_as_MySQLdb()
import os
BASE = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE, 'static', 'images', 'uploaded_photos')
app.config['UPLOAD_FOLDER_TEMPORARY'] = os.path.join(BASE, 'static', 'images', 'temporary')
app.config['MAX_CONTENT_LENGTH'] = 2000*1024*1024



from app import models
from app.debug_utils import reset_db
from app.views import blueprint_registration
blueprint_registration(app)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, sa=sa, so=so, reset_db=reset_db)

@app.before_request
def only_one_device_allowed_at_one_time():
    if current_user.is_authenticated:
        if current_user.active_session != session.get("active_session"):
            logout_user()
            session.clear()
            return redirect(url_for('home_bp.home'))
    return None

@app.before_request
def prevent_frequent_requests():
    if request.method == "POST" and request.endpoint == "chatbot_bp.chatbot":
        form = ChatForm()
        latest_request_time = session.get("last_request_time", 0)
        current_time = time.time()
        if latest_request_time is not None:
            if current_user.is_authenticated:
                if current_time - latest_request_time < 3:
                    flash("Please wait for three seconds before making another request!", "warning")
                    return render_template("chatbot.html", text_=None, title="Chatbot", form=form)
            else:
                if current_time - latest_request_time < 10:
                    flash("Please wait for ten seconds before making another request!", "warning")
                    return render_template("chatbot.html", text_=None, title="Chatbot", form=form)
        session["last_request_time"] = current_time
    return None


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
