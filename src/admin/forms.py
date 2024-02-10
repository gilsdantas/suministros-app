# Built-in imports
# Third-Party imports
from flask import abort
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import form, fields, validators, PasswordField, StringField
from wtforms.validators import DataRequired, Email

# Local imports
from ..models import Usuario


class BaseForm(FlaskForm):
    """
    Using Spanish for the built-in messages: https://wtforms.readthedocs.io/en/stable/i18n/#internationalization-i18n.
    Apply it for all forms
    """

    class Meta:
        locales = ["es_ES"]


class LoginAdminForm(form.Form):
    """
    Form for admins to login
    """

    email = fields.StringField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        usuario = self.get_user()

        if usuario is None or not check_password_hash(usuario.password, self.password.data):
            abort(401, "Usuario(a) o contrasenã inválidos")

    def get_user(self):
        user = Usuario.query.filter_by(email=self.email.data).first()
        if not user:
            abort(
                403,
                "Usuario(a) no encontrado. Si se trata de un error, envíe un "
                "correo electrónico a support@mariaonline.com e infórmenos su "
                "situación.",
            )
        return user

    #
    # email = StringField("Email", validators=[DataRequired(), Email()])
    # password = PasswordField("Contraseña", validators=[DataRequired()])
    #
    # def validar_login(self, field):
    #     usuario = self.get_user()
    #
    #     if usuario is None or not check_password_hash(usuario.password, self.password.data):
    #         abort(
    #             403,
    #             "Usuario(a) o contrasenã inválidos"
    #         )
    #
    # def get_user(self):
    #     user = Usuario.query.filter_by(email=self.email.data).first()
    #     if not user:
    #         abort(
    #             403,
    #             "Usuario(a) no encontrado. Si se trata de un error, envíe un "
    #             "correo electrónico a support@mariaonline.com e infórmenos su "
    #             "situación."
    #         )
    #     return user
