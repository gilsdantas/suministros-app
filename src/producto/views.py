# src/producto/views.py
# Built-in imports
import json
import os
from datetime import datetime
from io import BytesIO

# Third-party imports
from flask import redirect, url_for, render_template, request, session, send_file, jsonify, flash, current_app
from flask_login import login_required, current_user

# Local imports
from src.models import Producto, db, Venta
from . import producto


@producto.route("/add_producto", methods=["POST"])
@login_required
def add_producto():
    image_file = request.files["image"]
    image_data = image_file.read()

    # Create a new Producto instance
    producto = Producto(
        nombre=request.form["nombre"],
        descripcion=request.form["descripcion"],
        categoria=request.form["categoria"],
        precio=float(request.form["precio"]),
        stock=int(request.form["stock"]),
        image=image_data,  # Store the binary image data
    )

    # Save the Producto instance to the database
    db.session.add(producto)
    db.session.commit()

    return "Producto added successfully"


@producto.route("/get_producto/<int:producto_id>")
def get_producto(producto_id):
    product_fetched = Producto.query.get_or_404(producto_id)

    return jsonify(
        {
            "id": product_fetched.id,
            "nombre": product_fetched.nombre,
            "descripcion": product_fetched.descripcion,
            "categoria": product_fetched.categoria,
            "precio": product_fetched.precio,
            "stock": product_fetched.stock,
            "image": product_fetched.image,
        }
    )


@producto.route("/get_producto_image/<int:producto_id>")
def get_producto_image(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], producto.image)

    # Check if the image file exists
    if not os.path.exists(image_path):
        return "Image not found", 404

    # Read the image file and return its data
    with open(image_path, "rb") as f:
        image_data = f.read()

    return send_file(BytesIO(image_data), mimetype="image/jpeg")


@producto.route("/lista_productos", methods=("GET", "POST"))
def lista_productos():
    print("1. Inside endpoint List Productos")
    page = request.args.get("page", 1, type=int)
    productos = Producto.query.filter(Producto.stock > 0).paginate(page=page, per_page=10, error_out=False)

    if request.method == "POST":
        print("2. Inside POST IF")
        selected_products = {}
        for key, value in request.form.items():
            print("3. Inside FOR")
            if key.startswith("selected_products[]"):
                print("4. Inside Second IF")
                product_id = value
                quantity_key = f"product_quantity_{product_id}"
                quantity_value = request.form.get(quantity_key, 0)
                selected_products[product_id] = int(quantity_value)

        print("5. Selected Products: ", selected_products)
        session["selected_products"] = selected_products

        return redirect(url_for("producto.review_checkout"))

    return render_template(
        "productos/productos.html", productos=productos, title="Lista productos", get_product_name=get_product_name
    )


@producto.route("/review_checkout", methods=["POST"])
@login_required
def review_checkout():
    selected_products = {}
    for key, value in request.form.items():
        if "selected_products" in key:
            continue
        product_id = key.replace("product_", "")
        quantity_key = f"product_{product_id}"
        quantity_value = request.form.get(quantity_key, 0)
        selected_products[product_id] = int(quantity_value)

    total_amount = total_amount_to_pay(selected_products)

    product_names = {product_id: get_product_name(product_id) for product_id in selected_products.keys()}

    return render_template(
        "productos/review_checkout.html",
        selected_products=selected_products,
        product_names=product_names,
        total_amount=total_amount,
    )


@producto.route("/confirm_checkout", methods=["POST"])
@login_required
def confirm_checkout():
    # Gets the key 'selected_products'. It returns a dict as a string.
    # We need also replace single quotes to double quotes to use json.loads (to convert to real dict)
    selected_products = request.form.get("selected_products").replace("'", '"')
    selected_products = json.loads(selected_products)

    total_amount = total_amount_to_pay(selected_products)
    product_names = {product_id: get_product_name(product_id) for product_id in selected_products.keys()}

    # Save the purchased products to the database
    for product_id, quantity in selected_products.items():
        venta = Venta(
            producto_id=int(product_id),
            usuario_id=current_user.id,
            cantidad=int(quantity),
            fecha_de_venta=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        db.session.add(venta)
    db.session.commit()

    return render_template(
        "productos/confirm_checkout.html",
        selected_products=selected_products,
        product_names=product_names,
        total_amount=total_amount,
    )


@producto.route("/buy_products", methods=["GET", "POST"])
@login_required
def buy_products():
    if not current_user.is_authenticated:
        flash("Por favor inicia sesión para comprar productos", "info")
        next_page = request.url
        return redirect(url_for("auth.login", next=next_page))

    selected_product_ids = request.form.getlist("selected_products")

    return redirect(url_for("producto_bp.lista_productos"))


def get_product_name(product_id):
    prod = Producto.query.get(product_id)
    return prod.nombre if prod else "Producto desconocido"


def get_product_price(product_id):
    producto = Producto.query.get_or_404(product_id)
    return producto.precio


def total_amount_to_pay(selected_products):
    # {6: 2, 7: 2}
    total_amount = 0
    for product_id, quantity in selected_products.items():
        price = get_product_price(product_id)
        total_amount += price * quantity
    return total_amount
