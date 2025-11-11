from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    full_name = StringField("Full Name", validators=[Optional(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
