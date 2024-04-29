# Built-in imports
# Third-part imports
import flask_admin as admin
import flask_login as login
from flask import redirect, url_for, request, flash, session
from flask_admin import expose, helpers
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField, Select2Widget
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from passlib.hash import sha256_crypt
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from wtforms import fields, validators

from src.producto.forms import ProductoForm


# from src.admin.forms import LoginAdminForm


# Local imports
# from .forms import LoginAdminForm


class BaseForm(FlaskForm):
    """
    Using Spanish for the built-in messages: https://wtforms.readthedocs.io/en/stable/i18n/#internationalization-i18n.
    Apply it for all forms
    """

    class Meta:
        locales = ["es_ES"]


class LoginAdminForm(BaseForm):
    """
    Form for admins to login
    """

    email = fields.StringField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        usuario = self.get_user()

        return_value = FlaskForm.validate(self)
        if not return_value:
            return False

        if usuario is None:
            self.email.errors.append("Usuario(a) inválido")
            return False

        if not sha256_crypt.verify(self.password.data, usuario.password):
            self.password.errors.append("Contrasenã inválida")
            return False

        return True

    def get_user(self):
        from src.models import Usuario

        return Usuario.query.filter_by(email=self.email.data).first()


class ProductoModelView(ModelView):
    column_display_pk = True
    form = ProductoForm

    # How columns are displayed in the list view
    column_list = ("id", "nombre", "descripcion", "categoria", "precio", "stock", "image")

    # Column labels
    column_labels = {
        "nombre": "Nombre",
        "descripcion": "Descripción",
        "categoria": "Categoría",
        "precio": "Precio",
        "stock": "Existencias",
        "image": "Imagen",
    }

    # Column filters
    column_filters = ("nombre", "categoria", "precio", "stock")

    form_widget_args = {"categoria": {"widget": Select2Widget()}}

    def on_model_change(self, form, model, is_created):
        if form.imagen.data:
            filename = secure_filename(form.imagen.data.filename)
            model.save_images(form.imagen.data)

    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.is_admin


class UsuarioModelView(ModelView):
    column_display_pk = True

    # How columns are displayed in the list view
    column_list = ("id", "nombre", "apellido", "username", "email", "password")

    # Column labels
    column_labels = {
        "nombre": "Nombre",
        "apellido": "Apellido",
        "username": "Nombre de usuario",
        "email": "Correo electrónico",
        "password": "contraseña",
    }

    # Column filters
    column_filters = ("nombre", "apellido", "username", "email")

    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.is_admin


class MyAdminIndexView(admin.AdminIndexView):
    @expose("/")
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for(".login_view"))
        if not login.current_user.is_admin:
            session["flash_message"] = "No tienes permiso de administrador para acceder a este panel", "error"
            session["flash_category"] = "error"
            return redirect(url_for(".login_view"))

        form = LoginAdminForm()
        self._template_args["form"] = form
        return super(MyAdminIndexView, self).index()

    @expose("/login/", methods=("GET", "POST"))
    def login_view(self):
        if login.current_user.is_authenticated and login.current_user.is_admin:
            return redirect(url_for(".index"))

        form = LoginAdminForm(request.form)
        if helpers.validate_form_on_submit(form):
            usuario = form.get_user()
            if usuario is None:
                session["flash_message"] = "Correo electrónico o contraseña no válidos", "error"
                session["flash_category"] = "error"
            else:
                login.login_user(usuario)
                if usuario.is_admin:
                    return redirect(url_for(".index"))
                else:
                    session["flash_message"] = "No tienes permiso de administrador para acceder a este panel", "error"
                    session["flash_category"] = "error"
                    return redirect(url_for("home.dashboard"))  # Adjust the route name as needed

        self._template_args["form"] = form

        return super(MyAdminIndexView, self).index()

    @expose("/logout/")
    def logout_view(self):
        login.logout_user()
        return redirect(url_for(".index"))
