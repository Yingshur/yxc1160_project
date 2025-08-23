import random
import uuid
#from ensurepip import bootstrap
from wtforms import form, ValidationError
#from time import timezone
import os
import pymysql
from app.new_file import db
from flask import Flask, url_for, render_template
import flask_mail, itsdangerous
from flask_mail import Mail, Message
from itsdangerous import  URLSafeSerializer, SignatureExpired, BadSignature, URLSafeTimedSerializer
from app.models import User, Verification, Version
import pymysql
# from pymupdf import message


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



from app import views, models
from app.debug_utils import reset_db


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, sa=sa, so=so, reset_db=reset_db)

