# Built-in imports
# Thirty part imports
from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

# Local imports
from . import store
from .forms import ProductoForm
from .. import db, CURRENT_DIR, allowed_file
from ..models import Usuario, Producto


def check_admin():
    """
    Prevent non-admins from accessing the page
    """

    if not current_user.is_admin:
        abort(403)


@store.route("/admin/productos", methods=["GET", "POST"])
@login_required
def lista_productos():
    """
    List all products
    """

    check_admin()

    todos_los_productos = Producto.query.all()
    return render_template("admin/productos/productos.html", productos=todos_los_productos, title="Lista de Productos")


@store.route("/admin/productos/adiciona", methods=["GET", "POST"])
@login_required
def crear_producto():
    """
    Add a product to the database
    """

    check_admin()

    crea_un_producto = True

    form = ProductoForm()
    if form.validate_on_submit():
        producto = Producto(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            categoria=form.categoria.data,
            stock=form.stock.data,
        )
        try:
            # add productos to the database
            db.session.add(producto)
            db.session.commit()
            flash("Ha agregado exitosamente un nuevo producto.", "info")
        except SQLAlchemyError:
            db.session.rollback()
            abort(403, f"Lo producto ya existe en la base de datos. ({producto.nombre}).")
        except Exception as error:
            abort(500, error)

        # redirect to productos page
        return redirect(url_for("admin.lista_productos"))

    # load question template
    return render_template(
        "admin/productos/producto.html",
        action="Add",
        crea_un_producto=crea_un_producto,
        form=form,
        title="Crea Producto",
    )


@store.route("/admin/productos/edita/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id_producto):
    """
    Edit a product
    """

    check_admin()

    editar_un_producto = True

    producto = Producto.query.get_or_404(id_producto)

    form = ProductoForm(obj=producto)
    if form.validate_on_submit():
        producto.nombre = form.nombre.data
        producto.descripcion = form.descripcion.data
        producto.categoria = form.categoria.data
        producto.stock = form.stock.data

        try:
            # edit product in the database
            db.session.commit()
            flash("Ha editado correctamente el producto.", "info")
        except SQLAlchemyError:
            db.session.rollback()
            abort(403, f"El nombre del producto ya existe en la base de datos ({producto.nombre}).")
        except Exception as error:
            abort(500, error)

        # redirect to the productos page
        return redirect(url_for("admin.lista_productos"))

    form.nombre.data = producto.nombre
    form.descripcion.data = producto.descripcion
    form.categoria.data = producto.categoria
    form.stock.data = producto.stock

    return render_template(
        "admin/productos/producto.html",
        action="Edit",
        edit_question=editar_un_producto,
        form=form,
        question=producto,
        title="Editar Producto",
    )


@store.route("/admin/productos/elimina/<int:id>", methods=["GET", "DELETE"])
@login_required
def eliminar_productos(id_producto):
    """
    Delete a product from the database
    """

    check_admin()

    producto = Producto.query.get_or_404(id_producto)

    db.session.delete(producto)
    db.session.commit()
    flash("Ha eliminado correctamente el producto.", "info")

    # redirect to the product page
    return redirect(url_for("admin.lista_productos"))


@store.route("/admin/usuarios", methods=["GET", "POST"])
@login_required
def lista_usuarios():
    """
    List all users
    """

    check_admin()

    all_users = Usuario.query.all()
    return render_template("admin/usuarios/usuarios.html", users=all_users, title="Lista Usuarios")


@store.route("/admin/usuarios/edita/<int:id>", methods=["GET", "POST"])
@login_required
def edit_users(id_usuario):
    """
    Edit a usuarios
    """

    check_admin()

    editar_un_usuario = False

    usuario = Usuario.query.get_or_404(id_usuario)

    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        usuario.nombre = form.nombre.data
        usuario.apellido = form.apellido.data
        usuario.username = form.username.data
        usuario.email = form.email.data
        usuario.is_admin = True if form.is_admin.data == "True" else False

        try:
            # edit usuarios in the database
            db.session.commit()
            flash("Ha editado exitosamente al usuarios.", "info")
        except SQLAlchemyError:
            db.session.rollback()
            abort(403, f'Usuario "{usuario.username}" o e-mail "{usuario.email}" ya existen en la base de datos.')
        except Exception as error:
            abort(500, error)

        # redirect to the usuarios page
        return redirect(url_for("admin.lista_usuarios"))

    form.nombre.data = usuario.nombre
    form.apellido.data = usuario.apellido
    form.username.data = usuario.username
    form.email.data = usuario.email
    form.is_admin.data = str(usuario.is_admin)
    return render_template(
        "admin/usuarios/usuarios.html",
        action="Edit",
        edit_user=editar_un_usuario,
        form=form,
        user=usuario,
        title="Editar Usuario",
    )
