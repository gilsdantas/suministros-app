# Built-in imports
# Thirty part imports
from flask import render_template, flash, abort, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

# Local imports
from . import usuario
from .forms import UsuarioForm
from .. import db
from ..models import Usuario, Producto, Venta


@usuario.route("/usuarios", methods=["GET"])
@login_required
def usuario_detalles():
    """
    Show the usuarios detail
    """

    usuario_obj: Usuario = Usuario.query.get_or_404(current_user.id)
    return render_template("usuarios/users.html", usuario=usuario_obj, title="Usuario Detalles")


@usuario.route("/usuarios/<int:usuario_id>/editar", methods=["GET", "POST"])
@login_required
def editar_usuario(usuario_id):
    """
    Edit a usuarios
    """

    usuario_obj: Usuario = Usuario.query.get_or_404(usuario_id)
    form = UsuarioForm(obj=usuario_obj)

    # ToDo: Implement change Password
    if form.validate_on_submit():
        usuario_obj.nombre = form.nombre.data
        usuario_obj.apellido = form.apellido.data
        usuario_obj.username = form.username.data
        usuario_obj.email = form.email.data

        try:
            # edit usuarios in the database
            db.session.commit()
            flash("Ha editado correctamente el usuarios.", "info")
        except SQLAlchemyError:
            db.session.rollback()
            flash(f'Username "{usuario.username}" o email "{usuario.email}" ya existen en la base de datos.', "error")
        except Exception as error:
            flash(str(error), "error")

        # redirect to the usuarios page
        return redirect(url_for("usuario_bp.usuario_detalles"))

    form.nombre.data = usuario_obj.nombre
    form.apellido.data = usuario_obj.apellido
    form.username.data = usuario_obj.username
    form.email.data = usuario_obj.email

    return render_template(
        "usuarios/user.html",
        action="Edit",
        form=form,
        user=usuario_obj,
        title="Editar Usuario",
    )


#
#
# @usuarios.route("/eliminar-producto/<id>")
# def eliminar_producto(id):
#     producto = db.session.query(Producto).filter_by(id=int(id)).delete()
#     db.session.commit()
#
#     return redirect(url_for("home"))
#
#
# @usuarios.route("/tarea-hecha/<id>")
# def hecha(id):
#     # Se obtiene la tarea que se busca
#     tarea = db.session.query(Producto).filter_by(id=int(id)).first()
#
#     # Guardamos en la variable booleana de la tarea, su contrario
#     tarea.hecha = not tarea.hecha
#
#     # Ejecutar la operación pendiente de la base de datos return redirect(url_for('home')) # Esto nos redirecciona a
#     # la función home()
#     db.session.commit()
#
#     # Esto nos redirecciona a la función home() y si todo ha ido bien, al refrescar, la tarea eliminada ya no
#     # aparecera en el  listado
#     return redirect(url_for("home"))


@usuario.route("/usuarios/<int:usuario_id>/dashboard", methods=["GET", "POST"])
@login_required
def dashboard(usuario_id):
    """
    Generate the user's dashboard
    """

    # Get the user object from DB
    usuario_obj = Usuario.query.get_or_404(usuario_id)

    # Query the Venta table to get the products bought by the user
    user_products = (
        db.session.query(Producto, func.sum(Venta.cantidad).label("cantidad"))
        .join(Venta)
        .filter(Venta.usuario_id == usuario_obj.id)
        .group_by(Producto)
        .all()
    )
    print(f"===> user_products: {user_products}")
    return render_template(
        "home/dashboard.html",
        products=user_products,
        is_empty=True if user_products == [] else False,
        title="Home Dashboard",
    )
