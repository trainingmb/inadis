#!/usr/bin/python3
"""
Base for User Forms
"""
from app.v2.forms import BooleanField, DataRequired, FlaskForm, IntegerField, Length, StringField, SubmitField, PasswordInput

class BaseUserForm(FlaskForm):
    """
    Base user Form
    """
    user_name = StringField("User Name", validators=[DataRequired("A user cannot be nameless"), Length(max=128)])
    user_email = StringField("User Email", validators=[DataRequired("A user cannot be without an email"), Length(max=128)])
    user_password = StringField("User Password", widget=PasswordInput(hide_value=True), validators=[DataRequired("A user cannot be without a password"), Length(max=128)])
    user_password2 = StringField("ReEnter User Password", widget=PasswordInput(hide_value=True), validators=[DataRequired("A user cannot be without a password"), Length(max=128)])
    user_remember = BooleanField("Remember You?")
    submit = SubmitField(label="Create New User")

    def validate(self, extra_validators=None):
        # check if all required fields are filled
        rv = super(BaseUserForm, self).validate(extra_validators)
        if not rv:
            return False
        return True