# Thirty part imports
from flask_wtf import FlaskForm  # https://flask-wtf.readthedocs.io/en/1.2.x/
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class ProductoForm(FlaskForm):
    """
    Form for an admin to add or edit a product
    """

    nombre = StringField("Nombre", validators=[DataRequired()])
    descripcion = StringField("Descripcíon", validators=[DataRequired()])
    categorias = ["Laptop", "Desktop", "Periferico", "Otros"]
    categoria = SelectField("Categoria", choices=categorias)  # ToDo: Create a table for Categorias
    stock = StringField("Cantidad", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UsuarioForm(FlaskForm):
    """
    Form for an admin to edit a usuarios
    """

    nombre = StringField("Nombre", validators=[DataRequired()])
    apellido = StringField("Apellido", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired()])
    is_admin = SelectField("Es admin?", choices=["True", "False"])
    submit = SubmitField("Edit")
