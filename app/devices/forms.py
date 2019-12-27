from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DeviceForm(FlaskForm):
    """
    Form for admin to add or edit device
    """
    hostname = StringField('Hostname', validators=[DataRequired()])
    ip = StringField('IP')
    description = StringField('Description')
    make = StringField('Make')
    hardware = StringField('Hardware')
    location = StringField('Location')
    submit = SubmitField('Submit')