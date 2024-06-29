#!/usr/bin/python3
"""
Base for Creation Forms
"""
from app.v1.forms import DataRequired, FlaskForm, Length, StringField, SubmitField, SelectField

class BaseCreationForm(FlaskForm):
    """
    Base Creation Form
    """
    creation_name = StringField("Name of Creation", validators=[DataRequired("A creation cannot be nameless"), Length(max=255)])
    creation_regexfilter = StringField("Regex Filter for the Creation", validators=[DataRequired("A creation cannot be without a filter. Write '^' to match everthing"), Length(max=255)])
    creation_creators = SelectField('List of Creators')
    submit = SubmitField(label="Create New Creation")

    def validate(self, extra_validators=None):
        # check if all required fields are filled
        rv = super(BaseCreationForm, self).validate(extra_validators)
        if not rv:
            return False
        return True