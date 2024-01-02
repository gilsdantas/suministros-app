# Built-in imports
# Thirty part imports
# Local imports
from src.models import Producto
from . import usuario


# @producto.route("/crear-producto", methods=["POST"])
# def crear_producto():
#     categorias = {
#         0: "Sin categoria",
#         1: "Laptop",
#         2: "Desktop",
#         3: "Periferico",
#         4: "Otros",
#     }
#     producto = Producto(
#         descripcion=request.form["descripcion_producto"],
#         categoria=categorias[int(request.form["categoria_producto"])],
#         stock=request.form["stock_producto"],
#     )
#     db.session.add(producto)
#     db.session.commit()
#
#     return redirect(url_for("home"))
#
#
# @producto.route("/eliminar-producto/<id>")
# def eliminar_producto(id):
#     producto = db.session.query(Producto).filter_by(id=int(id)).delete()
#     db.session.commit()
#
#     return redirect(url_for("home"))
#
#
# @producto.route("/tarea-hecha/<id>")
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
