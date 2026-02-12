from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

# Validaciones para el formulario de libros
class LibroForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[DataRequired(message="El título es obligatorio"), Length(max=200)]
    )

    autor = StringField(
        "Autor",
        validators=[DataRequired(message="El autor es obligatorio"), Length(max=100)]
    )

    anio = IntegerField(
        "Año",
        validators=[
            DataRequired(message="El año es obligatorio"),
            NumberRange(min=1000, max=2100, message="Pon un año válido (ej: 2024)")
        ]
    )

    categoria = StringField(
        "Categoría",
        validators=[DataRequired(message="La categoria es obligatoria"),Length(max=100)]
    )

    submit = SubmitField("Guardar Libro")