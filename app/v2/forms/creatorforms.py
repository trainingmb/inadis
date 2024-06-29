#!/usr/bin/python3
"""
Base for Creator Forms
"""
from app.v2.forms import DataRequired, FlaskForm, IntegerField, Length, StringField, SubmitField

class BaseCreatorForm(FlaskForm):
    """
    Base Creator Form
    """
    creator_name = StringField("Name of Creator", validators=[DataRequired("A creator cannot be nameless"), Length(max=128)])
    creator_reference = IntegerField("Reference Number of the Creator", validators=[DataRequired("A creator cannot be without a reference")])
    creator_link = StringField("Link to Creator", validators=[DataRequired("A creator cannot be without a link"), Length(max=255)])
    submit = SubmitField(label="Create New Creator")

    def validate(self, extra_validators=None):
        # check if all required fields are filled
        rv = super(BaseCreatorForm, self).validate(extra_validators)
        if not rv:
            return False
        return True