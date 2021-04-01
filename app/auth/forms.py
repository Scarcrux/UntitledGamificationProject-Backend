from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from models.user import User

class RegistrationForm(FlaskForm):
    email =  StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
   	Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
          'Usernames must have only letters, numbers, dots or '
          'underscores')])
    password = PasswordField(label='Password',
                             validators=[DataRequired(),
                                         EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField(label='Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

def validate_email(self, field):
   	if User.query.filter_by(email=field.data.lower()).first():
          raise ValidationError('Email already registered.')

def validate_username(self, field):
    if User.query.filter_by(username=field.data).first():
          raise ValidationError('Username already in use.')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in', id="checkbox")
    submit = SubmitField('Login')