from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_login import current_user



class PostForm(FlaskForm):
    title = StringField('Title', validators =[DataRequired()])
    text = TextAreaField('Content')
    image = MultipleFileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('submit')

class ImageTestForm(FlaskForm):
    image = MultipleFileField('image_text')
    submit = SubmitField('submit')

class CkeditorTestForm(FlaskForm):
    pass
