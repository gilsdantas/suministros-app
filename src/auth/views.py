# Built-in imports
# Third-Party imports
from flask import abort, flash, redirect, render_template, request, url_for, get_flashed_messages
from flask_login import login_required, login_user, logout_user, LoginManager
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash

# Local imports
from . import auth
from .forms import LoginForm, SignUpForm
from .. import db
from ..models import Usuario


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handle requests to the /signup route
    Add a usuarios to the database through the sign-up form
    """

    req = request.data if request.data else request.form
    form = SignUpForm(obj=req)

    if request.method == "POST":
        usuario = Usuario(
            nombre=req.get("nombre"),
            apellido=req.get("apellido"),
            username=req.get("username"),
            email=req.get("email"),
            password=req.get("password"),
            is_admin=req.get("is_admin", False),
        )

        # add usuarios to the database
        try:
            db.session.add(usuario)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            flash(f'Username "{usuario.username}" o email "{usuario.email}" ya existen en la base de datos.', "error")
        except Exception as error:
            flash(str(error), "error")

        flash("¡Se ha registrado exitosamente! Ahora puede iniciar sesión.", "info")

        # redirect to the login page
        return redirect(url_for("auth.login"), 201)
    elif request.method == "GET":
        # load registration template
        return render_template("auth/registro.html", form=form, title="Sign Up")
    else:
        flash("Método no permitido. Comprueba tus acciones y vuelve a intentarlo.", "error")


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle requests to the /login route
    Log a user in through the sign-in form
    """

    req = request.data if request.data else request.form
    next_page = request.args.get("next")
    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            # Check if the user exists in the DB and if the password entered matches the password in the DB
            usuario = Usuario.query.filter_by(email=form.email.data).first()
            print(f"---> Usuaruio: {usuario}")
            print(f"---> Password: {form.password.data}")
            print(f"---> usuario.password: {usuario.password}")
            print(
                f"---> check_password_hash(usuario.password, form.password.data): {check_password_hash(usuario.password, form.password.data)}"
            )

            if usuario and check_password_hash(usuario.password, form.password.data):
                # Log user in
                login_user(usuario)

                # Redirect to the correct dashboard (admin or no-admin user) page after login
                next_page = request.args.get("next")
                if next_page:
                    return redirect(next_page)
                elif usuario.is_admin:
                    return redirect(url_for("home.admin_dashboard"))
                else:
                    return redirect(url_for("home.dashboard"))
            # When login details are incorrect
            else:
                flash("Correo electrónico o contraseña no válidos.", "error")
                return render_template("auth/login.html", form=form, title="Login"), 401

    # load login template
    return render_template("auth/login.html", form=form, title="Login", messagess=get_flashed_messages())


@auth.route("/logout")
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log a user out through the logout link
    """

    logout_user()
    flash("Has cerrado tu sesión correctamente.", "info")

    # Redirect to the login page
    return redirect(url_for("auth.login"))


login_manager = LoginManager()


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
