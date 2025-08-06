from random import choices
from itertools import cycle
from datetime import datetime
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, PasswordField, BooleanField, SelectField, IntegerField, FloatField
from flask_wtf.file import FileAllowed, FileRequired, FileField
#from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Email, Optional, Length, Regexp, \
    AnyOf, InputRequired
from app.new_file import db
from app.models import User
import datetime


def int_validator(form, field):
    try:
        int(field.data)
    except(ValueError, TypeError):
        raise ValidationError('You must enter a integer')


def float_validator(form, field):
    try:
        float(field.data)
    except(ValueError, TypeError):
        raise ValidationError('You must enter a float number')


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
    reign_start = IntegerField(' Start of the Reign (Year)', validators=[DataRequired('Data is required')])
    reign = StringField('Reign of the Emperor', validators=[DataRequired('Data is required')])
    dynasty = SelectField('Choose a dynasty', choices=[('Macedonian', 'Macedonian'), ('Doukas', 'Doukas'), ('Komnenos', 'Komnenos'), ('Angelos', 'Angelos'), ('Palaiologos', 'Palaiologos')],validators=[DataRequired('Data is required')] )
    ascent_to_power = SelectField('Choose how the emperor ascended to throne', choices=[('Hereditary Succession', 'Hereditary Succession'), ('Coup d\'état', 'Coup d\'état'), ('Marriage', 'Marriage'), ('Civil War', 'Civil War'), ('Appointment', 'Appointment'),],validators=[DataRequired('Data is required')] )
    portrait = FileField('Upload Portrait', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images Only')])
    life = TextAreaField('Life', validators=[DataRequired('Data is required')], render_kw={"rows":30, "style":"min-height: 400px;"})
    references = TextAreaField('References', validators=[DataRequired('Data is required')], render_kw={"rows":10, "style":"min-height: 400px;"})
    submit = SubmitField('Submit')



class DeleteForm(FlaskForm):
    number = IntegerField('Code for deletion', validators=[DataRequired('Data is required')])
    submit = SubmitField('Submit')



class ArchitectureForm(FlaskForm):
    edit = HiddenField(default='-1')
    in_greek = StringField('Name of the Building in Native Language', validators=[DataRequired('Data is required')])
    title = StringField('Name of the building', validators=[DataRequired('Data is required')])
    construction_completed = IntegerField('Year Completed', validators=[DataRequired('Data is required'), int_validator])
    architectural_style = StringField('Architectural Style', validators=[DataRequired('Data is required')])
    current_status = SelectField('Current use', choices=[('Retains original role', 'Retains original role'), ('Converted into a secular building', 'Converted into a secular building'), ('Converted into a Mosque', 'Converted into a Mosque'), ('Ruined', 'Ruined')], validators=[DataRequired('Data is required')])
    location = StringField('Location of the building', validators=[DataRequired('Data is required)')])
    longitude = FloatField('Longitude of the building location',validators=[InputRequired('Data is required'), float_validator])
    latitude = FloatField('Latitude of the building location', validators=[InputRequired('Data is required'), float_validator])
    description=  TextAreaField('Description', validators=[DataRequired('Data is required')], render_kw={"rows":30, "style":"min-height: 400px;"})
    references= TextAreaField('References', validators=[DataRequired('Data is required')], render_kw={"rows":10, "style":"min-height: 400px;"})
    image = FileField('Upload Portrait', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images Only')])
    building_type = SelectField('Original building type', choices=[('Ecclesiastical Building', 'Ecclesiastical Building'), ('Civil Building', 'Civil Building'), ('Fortification', 'Fortification')],validators=[DataRequired('Data is required')] )
    submit = SubmitField('Submit')



class ImageEditForm(FlaskForm):
    edit = HiddenField(default='-1')
    id_number = IntegerField('Input the ID number of the image', validators=[DataRequired('Data is required')])
    image = FileField('Upload Portrait', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images Only'), DataRequired('Data is required')])
    caption = StringField('Caption', validators=[DataRequired('Data is required)')])
    submit = SubmitField('Submit')



class ImageUploadForm(FlaskForm):
    edit = HiddenField(default='-1')
    #id_number = IntegerField('Input the ID number of the image', validators=[DataRequired('Data is required')])
    image = FileField('Upload Portrait', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images Only'), DataRequired('Data is required')])
    caption = StringField('Caption', validators=[DataRequired('Data is required)')])
    submit = SubmitField('Submit')





class WarForm(FlaskForm):
    edit = HiddenField(default='-1')
    title = StringField('Name of the Battle', validators=[DataRequired('Data is required')])
    start_year= IntegerField('Year when the battle started', validators=[InputRequired('Data is required, must be a whole number'), int_validator])
    dates = StringField('Dates of the battle', validators=[DataRequired('Data is required')])
    location = StringField('Location of the battle', validators=[DataRequired('Data is required, enter the approximate name (e.g. a nearby village if exact name is unknown)')])
    longitude = FloatField('Longitude of the battle location', validators=[InputRequired('Data is required'), float_validator])
    latitude = FloatField('Latitude of the battle location', validators=[InputRequired('Data is required'), float_validator])
    roman_commanders = StringField('Roman Commanders', validators=[DataRequired('Data is required')])
    enemy_commanders= StringField('Enemy Commanders', validators=[DataRequired('Data is required')])
    roman_strength= StringField('Roman Strength', validators=[DataRequired('Data is required')])
    enemy_strength=  StringField('Enemy Strength', validators=[DataRequired('Data is required')])
    roman_loss =  StringField('Roman Losses', validators=[DataRequired('Data is required')])
    enemy_loss= StringField('Enemy Losses', validators=[DataRequired('Data is required')])
    dynasty = SelectField('Choose a dynasty', choices=[('Macedonian', 'Macedonian'), ('Doukas', 'Doukas'), ('Komnenos', 'Komnenos'), ('Angelos', 'Angelos'), ('Palaiologos', 'Palaiologos')],validators=[DataRequired('Data is required')] )
    war_name = StringField('War name', validators=[DataRequired('Data is required')])
    war_type = SelectField('Foreign or Civil War?', choices=[('Foreign War', 'Foreign War'), ('Civil War', 'Civil War')],validators=[DataRequired('Data is required')] )
    description=  TextAreaField('Description', validators=[DataRequired('Data is required')], render_kw={"rows":30, "style":"min-height: 400px;"})
    references= TextAreaField('References', validators=[DataRequired('Data is required')], render_kw={"rows":10, "style":"min-height: 400px;"})
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images Only')])
    result = SelectField('Result', choices=[('Roman Victory', 'Roman Victory'), ('Enemy Victory', 'Enemy Victory'), ('Inconclusive', 'Inconclusive'),  ],validators=[DataRequired('Data is required')] )
    submit = SubmitField('Submit')





class LiteratureForm(FlaskForm):
    edit = HiddenField(default='-1')
    #id: so.Mapped[int] = so.mapped_column(primary_key=True, unique=True)
    title = StringField('Title of the Work',  validators=[DataRequired('Data is required')])
    in_greek = StringField('Title of the Work in Greek',  validators=[DataRequired('Data is required')])
    author = StringField('Name of the Author',  validators=[DataRequired('Data is required')])
    year_completed = StringField('Year Completed (Approximate)', validators=[DataRequired('Data is required')])
    current_location= StringField('Current location',  validators=[DataRequired('Data is required')])
    genre = SelectField('Genre', choices=[('Religious Literature', 'Religious Literature'), ('Chronicle', 'Chronicle'), ('Secular Poetry', 'Secular Poetry'), ('Secular Academic Literature', 'Secular Academic Literature'), ('Others', 'Others')],validators=[DataRequired('Data is required')] )
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images Only')])
    description = TextAreaField('Description', validators=[DataRequired('Data is required')],
                                render_kw={"rows": 30, "style": "min-height: 400px;"})
    references = TextAreaField('References', validators=[DataRequired('Data is required')],
                               render_kw={"rows": 10, "style": "min-height: 400px;"})
    submit = SubmitField('Submit')




class ArtifactForm(FlaskForm):
    edit = HiddenField(default='-1')
    #id: so.Mapped[int] = so.mapped_column(primary_key=True, unique=True)
    title = StringField('Title of the Work',  validators=[DataRequired('Data is required')])
    in_greek = StringField('Title of the Work in Greek',  validators=[DataRequired('Data is required')])
    #author = StringField('Name of the Author',  validators=[DataRequired('Data is required')])
    year_completed = StringField('Year Completed (Approximate)', validators=[DataRequired('Data is required')])
    current_location= StringField('Current location',  validators=[DataRequired('Data is required')])
    #genre = SelectField('Genre', choices=[('Religious Literature', 'Religious Literature'), ('Chronicle', 'Chronicle'), ('Secular Poetry', 'Secular Poetry'), ('Secular Academic Literature', 'Secular Academic Literature'), ('Others', 'Others')],validators=[DataRequired('Data is required')] )
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images Only')])
    description = TextAreaField('Description', validators=[DataRequired('Data is required')],
                                render_kw={"rows": 30, "style": "min-height: 400px;"})
    references = TextAreaField('References', validators=[DataRequired('Data is required')],
                               render_kw={"rows": 10, "style": "min-height: 400px;"})
    submit = SubmitField('Submit')







def password_policy(form, field):
    message = """A password must be between 8 and 16 characters long, and have an
                uppercase and lowercase letter, a digit, and a special character, white space is not allowed."""
    if len(field.data) < 8:
        raise ValidationError(message)
    if len(field.data) > 16:
        raise ValidationError(message)
    flg_upper = flg_lower = flg_digit = flg_non_let_dig = False
    for ch in field.data:
        if ch == " ":
            raise ValidationError(message)
        flg_upper = flg_upper or ch.isupper()
        flg_lower = flg_lower or ch.islower()
        flg_digit = flg_digit or ch.isdigit()
        flg_non_let_dig = flg_non_let_dig or not ch.isalnum()
    if not (flg_upper and flg_lower and flg_digit and flg_non_let_dig):
        raise ValidationError(message)

class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')
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



