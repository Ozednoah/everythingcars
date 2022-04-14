from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,BooleanField,IntegerField,SelectField

from wtforms.validators import DataRequired, Email,Length

class Loginform(FlaskForm):
    email=StringField('Enter your password',validators=[DataRequired(),Email()])
    password=PasswordField('Enter password:',validators=[DataRequired()])
    submitbtn=SubmitField('Submit')

class Specform(FlaskForm):
    fullname = StringField('Enter your fullname',validators=[DataRequired()])
    email=StringField('Enter your password',validators=[DataRequired(),Email()])
    password=PasswordField('Enter password:',validators=[DataRequired()])
    password1=PasswordField('Enter password:',validators=[DataRequired()])
    submitbtn=SubmitField('Submit')