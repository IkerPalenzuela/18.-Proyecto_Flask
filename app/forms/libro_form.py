from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class LibroForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[DataRequired(message="El título es obligatorio"), Length(max=200)]
    )

    autor = StringField(
        "Autor",
        validators=[DataRequired(), Length(max=100)]
    )

    # Cambiamos Resumen por Año (Integer)
    anio = IntegerField(
        "Año",
        validators=[NumberRange(min=1000, max=2100, message="Pon un año válido")]
    )

    # Cambiamos Resumen por Categoria
    categoria = StringField(
        "Categoría",
        validators=[Length(max=100)]
    )

    submit = SubmitField("Guardar")