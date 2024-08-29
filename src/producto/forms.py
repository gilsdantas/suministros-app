# Built-in imports
# Third-Party imports
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.security import check_password_hash
from wtforms import (
    PasswordField,
    StringField,
    SubmitField,
    ValidationError,
    FloatField,
    IntegerField,
    SelectField,
    FileField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Local imports
from src.models import Producto


class BaseForm(FlaskForm):
    """
    Using Spanish for the built-in messages: https://wtforms.readthedocs.io/en/stable/i18n/#internationalization-i18n.
    Apply it for all forms
    """

    class Meta:
        locales = ["es_ES"]


class ProductoForm(BaseForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    descripcion = StringField("Descripción", validators=[DataRequired()])
    precio = FloatField("Precio", validators=[DataRequired()])
    stock = IntegerField("Stock", validators=[DataRequired()])
    categoria = SelectField("Categoría", validators=[DataRequired()])
    imagen = FileField(
        "Imagen",
        validators=[FileAllowed(["jpg", "jpeg", "png", "svg", "gif", "bmp"], "Solo se permiten archivos de imagen.")],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categoria.choices = self.get_categoria_choices()

    def get_categoria_choices(self):
        # Query distinct values of Categoria from the Producto table
        categorias = Producto.query.with_entities(Producto.categoria).distinct().all()
        # Flatten the results into a list of choices
        choices = [(categoria[0], categoria[0]) for categoria in categorias]
        return choices
