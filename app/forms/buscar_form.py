from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Validaciones para el formulario de búsqueda
class BuscarForm(FlaskForm):
    busqueda = StringField('Buscar por titulo', validators=[DataRequired()])
    enviar = SubmitField('Buscar')