# Built-in imports
# Thirty part imports
from flask import render_template, abort, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

# Local imports
from . import home


@home.route("/")
@home.route("/index")
def homepage():
    """
    Render the homepage templates on the '/' or '/index' route
    """

    # Send products to template index.html
    return render_template("home/index.html", title="Home")


@home.route("/admin/dashboard")
@login_required
def admin_dashboard():
    """
    Render the admin dashboard template on the /admin/dashboard route
    """

    if not current_user.is_admin:
        abort(403)

    return render_template("home/admin_dashboard.html", title="Dashboard")


@home.route("/usuario/dashboard")
@login_required
def dashboard():
    """
    Render the dashboard template on the /usuario/dashboard route
    """
    print(f"Current user Id: {current_user.id}")
    return redirect(url_for("usuario.dashboard", usuario_id=current_user.id))
