from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Contraseña')
    nombre = StringField('Nombre Completo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Guardar')