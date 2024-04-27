# Built-in imports
# Third-Party imports
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
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
    submit = SubmitField("Login")

    def validate_email(self, field):
        usuario = self.get_user()
        if usuario is None:
            print(f"===> Validate user email: {usuario}")
            raise ValidationError("Usuario no encontrado", "error")

    def validate_password(self, field):
        usuario = self.get_user()

        # More about the method below: https://tedboy.github.io/flask/generated/werkzeug.check_password_hash.html
        if usuario and not check_password_hash(usuario.password, self.password.data):
            raise ValidationError("La contraseña no es válida", "error")

    def get_user(self):
        return Usuario.query.filter_by(email=self.email.data).first()
