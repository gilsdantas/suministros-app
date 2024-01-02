# Built-in imports
# Thirty part imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Email

# Local imports


class BaseForm(FlaskForm):
    """
    Using Spanish for the built-in messages: https://wtforms.readthedocs.io/en/stable/i18n/#internationalization-i18n.
    Apply it for all forms
    """

    class Meta:
        locales = ["es_ES"]


class UsuarioForm(BaseForm):
    """
    Form for a usuario to edit its information
    """

    nombre = StringField("Nombre", validators=[DataRequired()])
    apellido = StringField("Apellido", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-Mail", validators=[Email()])
    submit = SubmitField("Editar")
