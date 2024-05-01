from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField ,EmailField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class UpadateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email',validators=[DataRequired(), Email()])

    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')