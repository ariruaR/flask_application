from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

class RegisterForm(FlaskForm):
  username = StringField(validators=[
    InputRequired(), 
    Length(min=4, max=20)],
    render_kw={"placeholder": "Username"}
    )
  password = StringField(validators=[
    InputRequired(), 
    Length(min=4, max=20)],
    render_kw={"placeholder": "Password"}
    )
  submit = SubmitField("Register")

class LoginForm(FlaskForm):
  username = StringField(validators=[
    InputRequired(), 
    Length(min=4, max=20)],
    render_kw={"placeholder": "Username"}
    )
  password = StringField(validators=[
    InputRequired(), 
    Length(min=4, max=20)],
    render_kw={"placeholder": "Password"}
    )
  submit = SubmitField("Login")
