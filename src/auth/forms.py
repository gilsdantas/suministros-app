# Built-in imports
# Third-Party imports
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from src.models import Usuario


# Local imports
# from ..models import Usuario


class BaseForm(FlaskForm):
    """
    Using Spanish for the built-in messages: https://wtforms.readthedocs.io/en/stable/i18n/#internationalization-i18n.
    Apply it for all forms
    """

    class Meta:
        locales = ["es_ES"]


class SignUpForm(BaseForm):
    """
    Form for usuarios to create new account
    """

    nombre = StringField(label="Nombre", validators=[DataRequired()])
    apellido = StringField(label="Apellido", validators=[DataRequired()])
    username = StringField(label="Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        label="Contraseña",
        validators=[
            DataRequired(),
            Length(min=6, max=12, message="La longitud de la contraseña debe estar entre %(min)d y %(max)d caracteres"),
        ],
    )
    confirm_password = PasswordField(
        label="Confirmar contraseña",
        validators=[DataRequired(), EqualTo("password", message="¡Ambos campos de contraseña deben ser iguales!")],
    )
    submit = SubmitField("Registro")

    def validate_email(self, field):
        if Usuario.query.filter_by(email=field.data).first():
            raise ValidationError("Correo electrónico ya está en uso.")

    def validate_username(self, field):
        if Usuario.query.filter_by(username=field.data).first():
            raise ValidationError("El nombre de usuarios ya está en uso.")


class LoginForm(BaseForm):
    """
    Form for users to login
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Login")  # User validation is done only in the server side for safety reasons

    def get_user(self):
        return Usuario.query.filter_by(email=self.email.data).first()
