from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email
from app.models import User, Patient, Treatment

class PatientSignUpForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    dateofbirth = StringField('Date of Birth', validators=[DataRequired()])
    submit = SubmitField('Continue')

class TreatmentSignUpForm(FlaskForm):
    treatmentname = StringField('Treatment Name', validators=[DataRequired()])
    treatmentnotes = StringField('Treatment Notes', validators=[DataRequired()])
    treatmentdate = StringField('Date of Treatment', validators=[DataRequired()])
    treatmentprice = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Sign Up Patient')

class TherapistLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class TherapistRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
