# # Built-in imports
# # Third-Party imports
# from flask_wtf import FlaskForm
# from werkzeug.security import check_password_hash
# from wtforms import form, fields, validators
#
# # Local imports
# from ..models import Usuario
#
#
# class BaseForm(FlaskForm):
#     """
#     Using Spanish for the built-in messages: https://wtforms.readthedocs.io/en/stable/i18n/#internationalization-i18n.
#     Apply it for all forms
#     """
#
#     class Meta:
#         locales = ["es_ES"]
#
#
# class LoginAdminForm(form.Form):
#     """
#     Form for admins to login
#     """
#
#     email = fields.StringField(validators=[validators.InputRequired()])
#     password = fields.PasswordField(validators=[validators.InputRequired()])
#
#     def validate_login(self, field):
#         usuario = self.get_user()
#
#         return_value = FlaskForm.validate(self)
#         if not return_value:
#             return False
#
#         if usuario is None:
#             self.email.errors.append("Usuario(a) inválido")
#             return False
#
#         if not check_password_hash(usuario.password, self.password.data):
#             self.password.errors.append("Contrasenã inválida")
#             return False
#
#         return True
#
#     def get_user(self):
#         return Usuario.query.filter_by(email=self.email.data).first()
