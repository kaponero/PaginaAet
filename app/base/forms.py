from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField, TextField, PasswordField
from wtforms.validators import Email, DataRequired


class Formulario(Form):
    name = StringField ('Nombre del programa')
    category = StringField ('Categoria')
    genre = StringField ('genero')


class LoginForm(FlaskForm):
    email = TextField('email', id='email_login'   , validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='pwd_login', validators=[DataRequired()])
