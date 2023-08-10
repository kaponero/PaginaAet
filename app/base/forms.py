from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField, TextField, PasswordField
from wtforms.validators import Email, DataRequired


class Formulario(Form):
    name = StringField ('Nombre del programa')
    category = StringField ('Categoria')
    genre = StringField ('genero')
