from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Formulario de búsqueda de libros por título
class BuscarForm(FlaskForm):
    busqueda = StringField('Buscar por titulo', validators=[DataRequired()])
    enviar = SubmitField('Buscar')