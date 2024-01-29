# adminbp = Blueprint('adminbp', name)
# admin.add_view(ModelView(User, db.session, category="Team"))
# admin.add_view(ModelView(Role, db.session, category="Team"))
#
# path = op.join(op.dirname(file), 'tuozhan')
# admin.add_view(FileAdmin(path, '/static/tuozhan/', name='File Explore'))
from flask import redirect, url_for, request
from flask_admin import expose, helpers
from flask_admin.contrib import sqla
import flask_admin as admin
import flask_login as login
from werkzeug.security import generate_password_hash

from src import db
from src.auth.forms import LoginForm, SignUpForm
from src.models import Usuario


class MyAdminModelView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated


class MyAdminIndexView(admin.AdminIndexView):
    @expose("/")
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for(".login_view"))
        return super(MyAdminIndexView, self).index()

    @expose("/login/", methods=("GET", "POST"))
    def login_view(self):
        # Handling user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            usuario = form.get_user()
            login.login_user(usuario)

        if login.current_user.is_authenticated:
            return redirect(url_for(".index"))

        link = (
            '<p>¿No tienes una cuenta? <a href="' + url_for(".register_view") + '">Pulse aquí para registrarse.</a></p>'
        )
        self._template_args["form"] = form
        self._template_args["link"] = link
        return super(MyAdminIndexView, self).index()

    @expose("/register/", methods=("GET", "POST"))
    def register_view(self):
        form = SignUpForm(request.form)
        if helpers.validate_form_on_submit(form):
            usuario = Usuario()

            form.populate_obj(usuario)
            # We hash the users password to avoid saving it as plaintext in the db
            usuario.password = generate_password_hash(form.password.data)

            db.session.add(usuario)
            db.session.commit()

            login.login_user(usuario)
            return redirect(url_for(".index"))
        #
        link = (
            '<p>¿Ya tienes una cuenta? <a href="' + url_for(".login_view") + '">Haga clic aquí para ingresar.</a></p>'
        )
        self._template_args["form"] = form
        self._template_args["link"] = link
        return super(MyAdminIndexView, self).index()

    @expose("/logout/")
    def logout_view(self):
        login.logout_user()
        return redirect(url_for(".index"))
