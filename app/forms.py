from random import choices

from datetime import datetime
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, PasswordField, BooleanField, SelectField, IntegerField
from flask_wtf.file import FileAllowed, FileRequired, FileField
#from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Email, Optional, Length, Regexp, AnyOf
from app.new_file import db
from app.models import User
import datetime



class AdminCodeForm(FlaskForm):
    code = StringField('Admin Invitation Code', validators=[DataRequired(message="Data is required")])
    submit = SubmitField('Submit')

class InvitationCodeForm(FlaskForm):
    code = StringField('Admin Invitation Code', validators=[DataRequired(message="Data is required")])
    user_id = IntegerField('user_id', validators=[DataRequired(message="Data is required")])

class AllEmperorForm(FlaskForm):
    edit = HiddenField(default='-1')
    title = StringField('Name of the Emperor', validators=[DataRequired('Data is required')])
    in_greek = StringField('Name of the Emperor in Greek', validators=[DataRequired('Data is required')])
    birth = StringField('Birth date of the Emperor', validators=[DataRequired('Data is required')])
    death = StringField('Death date of the Emperor', validators=[DataRequired('Data is required')])
    reign = StringField('Reign of the Emperor', validators=[DataRequired('Data is required')])
    dynasty = SelectField('Choose a dynasty', choices=[('Macedonian', 'Macedonian'), ('Doukas', 'Doukas'), ('Komnenos', 'Komnenos'), ('Angelos', 'Angelos'), ('Palaiologos', 'Palaiologos')],validators=[DataRequired('Data is required')] )
    portrait = FileField('Upload Portrait', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images Only')])
    life = TextAreaField('Life', validators=[DataRequired('Data is required')])
    submit = SubmitField('Submit')




def password_policy(form, field):
    message = """A password must be at least 8 characters long, and have an
                uppercase and lowercase letter, a digit, and a character which is
                neither a letter or a digit"""
    if len(field.data) < 8:
        raise ValidationError(message)
    flg_upper = flg_lower = flg_digit = flg_non_let_dig = False
    for ch in field.data:
        flg_upper = flg_upper or ch.isupper()
        flg_lower = flg_lower or ch.islower()
        flg_digit = flg_digit or ch.isdigit()
        flg_non_let_dig = flg_non_let_dig or not ch.isalnum()
    if not (flg_upper and flg_lower and flg_digit and flg_non_let_dig):
        raise ValidationError(message)

class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')
    appo_id = HiddenField('appo_id')
    user_id = HiddenField('user_id')
    current_choice = HiddenField()

class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Current Password',validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(),password_policy])
    confirm_password = PasswordField('Confirm New Password',validators=[DataRequired(),EqualTo('new_password')])
    submit = SubmitField('Change Password')

    @staticmethod
    def validate_password(form, field):
        if not current_user.check_password(field.data):
            raise ValidationError('Incorrect Password')

class ChangeEmailForm(FlaskForm):
    password = PasswordField('Your Password',validators=[DataRequired()])
    new_email = StringField('New Email', validators=[DataRequired()])
    confirm_email = StringField('Confirm New Email',validators=[DataRequired(),EqualTo('new_email')])
    submit = SubmitField('Update Email')

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),password_policy])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    verification_code = StringField('Verification code', validators=[DataRequired()])
    submit = SubmitField('Register')

    @staticmethod
    def validate_username(form, field):
        q = db.select(User).where(User.username==field.data)
        if db.session.scalar(q):
            raise ValidationError('Username already taken. Try again')

    def validate_email(form, field):
        q = db.select(User).where(User.email==field.data)
        if db.session.scalar(q):
            raise ValidationError('Email already taken. Try again')

class RegisterEmail(FlaskForm):
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Verify Email')
