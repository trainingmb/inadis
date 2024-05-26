#!/usr/bin/python3
"""
Base for Post Forms
"""
from app.v1.forms import DateTimeField, DataRequired, FlaskForm, IntegerField, Length, StringField, SubmitField

class BasePostForm(FlaskForm):
    """
    Base Creator Form
    """
    post_creations = SelectField('Creation')
    post_title = StringField("Title", validators=[DataRequired("A Post must have a Title"), Length(max=255)])
    post_content = StringField('Content', validators=[DataRequired("A Post must Content"), Length(max=65535)])
    post_comment = StringField("Comment", validators=[Length(max=255)])
    post_reference = IntegerField("Reference Number of the Creator", validators=[DataRequired("A Post cannot be without a reference")])
    post_posted_at =  DateTimeField("Posted At")
    post_fetched_at = DateTimeField("Fetched At")
    submit = SubmitField(label="Create New Post")

    def validate(self, extra_validators=None):
        # check if all required fields are filled
        rv = super(BasePostForm, self).validate(extra_validators)
        if not rv:
            return False
        return True