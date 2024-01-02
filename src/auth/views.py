# Built-in imports
import json

# Third-Party imports
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError

# Local imports
from . import auth
from .. import db
from .forms import LoginForm, SignUpForm
from ..models import Usuario


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handle requests to the /signup route
    Add a usuario to the database through the sign-up form
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

        # add usuario to the database
        try:
            db.session.add(usuario)
            db.session.commit()
        except SQLAlchemyError as error:
            print(f"Error: {error}")
            db.session.rollback()
            abort(403, f'Username "{usuario.username}" o email "{usuario.email}" ya existen en la base de datos.')
        except Exception as error:
            abort(500, error)

        flash("¡Se ha registrado exitosamente! Ahora puede iniciar sesión.")

        # redirect to the login page
        return redirect(url_for("auth.login"), 201)
    elif request.method == "GET":
        # load registration template
        print("Estou em GET request for Auth")
        return render_template("auth/registro.html", form=form, title="Sign Up")
    else:
        abort(405)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle requests to the /login route
    Log a usuario in through the sign-in form
    """

    req = request.data if request.data else request.form

    form = LoginForm()

    if request.method == "POST":
        # Check if the user exists in the DB and if the password entered matches the password in the DB
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.check_password(form.password.data):
            # Log user in
            login_user(usuario)

            # Redirect to the correct dashboard (admin or no-admin user) page after login
            if usuario.is_admin:
                return redirect(url_for("home.admin_dashboard"))
            else:
                return redirect(url_for("home.dashboard"))
        # When login details are incorrect
        else:
            flash("Correo electrónico o contraseña no válidos.")
            return render_template("auth/login.html", form=form, title="Login"), 401

    # load login template
    return render_template("auth/login.html", form=form, title="Login")


@auth.route("/logout")
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log a usuario out through the logout link
    """

    logout_user()
    flash("Has cerrado tu sesión correctamente.")

    # Redirect to the login page
    return redirect(url_for("auth.login"))
