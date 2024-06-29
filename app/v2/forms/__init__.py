#!/usr/bin/python3

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField, DateField, DateTimeField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from wtforms.widgets import PasswordInput


from app.v2.forms.creatorforms import *
from app.v2.forms.creationforms import *
from app.v2.forms.postforms import *
from app.v2.forms.userforms import *