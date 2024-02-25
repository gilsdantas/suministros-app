# Built-in imports
# Third-part imports
import flask_admin as admin
import flask_login as login
from flask import redirect, url_for, request, flash, session
from flask_admin import expose, helpers
from flask_admin.contrib import sqla

# Local imports
from src.admin.forms import LoginAdminForm


class MyAdminModelView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated


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
