from wtforms import Form
from wtforms import StringField

class Formulario(Form):
    name = StringField ('Nombre del programa')
    category = StringField ('Categoria')
    gender = StringField ('genero')
    