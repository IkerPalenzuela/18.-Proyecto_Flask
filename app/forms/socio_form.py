from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SocioForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[
        DataRequired(message="El nombre es obligatorio"),
        Length(min=3, max=100)
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message="El email es obligatorio"),
        Email(message="Introduce un email válido")
    ])
    
    submit = SubmitField('Guardar Socio')