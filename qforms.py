from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length


class queryForm(FlaskForm):
    query = StringField(validators=[Length(min=3, max=400)])
    submit = SubmitField('Search')
