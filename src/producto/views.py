# src/producto/views.py
from io import BytesIO

from PIL import Image
from flask import redirect, url_for, render_template, request, session, send_file, jsonify, flash

from decimal import Decimal

from flask_login import login_required, current_user

from . import producto
from .. import db
from ..models import Producto


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
    return send_file(BytesIO(producto.image), mimetype="image/jpeg")


@producto.route("/lista-productos", methods=("GET", "POST"))
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


@producto.route("/review-checkout", methods=("GET", "POST"))
@login_required
def review_checkout():
    selected_products = {}
    for key, value in request.form.items():
        if "selected_products" in key:
            product_id = value
            quantity_key = f"product_quantity_{product_id}"
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


@producto.route("/confirm-checkout", methods=["POST"])
@login_required
def confirm_checkout():
    selected_products = {}
    for key, value in request.form.items():
        if "selected_products" in key:
            product_id = value
            quantity_key = f"product_quantity_{product_id}"
            quantity_value = request.form.get(quantity_key, 0)
            selected_products[product_id] = int(quantity_value)

    total_amount = total_amount_to_pay(selected_products)

    product_names = {product_id: get_product_name(product_id) for product_id in selected_products.keys()}

    return render_template(
        "productos/confirm_checkout.html",
        selected_products=selected_products,
        product_names=product_names,
        total_amount=total_amount,
    )


@producto.route("/buy-products", methods=["GET", "POST"])
@login_required
def buy_products():
    if not current_user.is_authenticated:
        flash("Por favor inicia sesión para comprar productos", "info")
        next_page = request.url
        return redirect(url_for("auth.login", next=next_page))

    selected_product_ids = request.form.getlist("selected_products")
    print("===> ", selected_product_ids)

    return redirect(url_for("producto.lista_productos"))


def get_product_name(product_id):
    prod = Producto.query.get(product_id)
    return prod.nombre if prod else "Producto desconocido"


def get_product_price(product_id):
    producto = Producto.query.get_or_404(product_id)
    return producto.precio


def total_amount_to_pay(selected_products):
    total_amount = 0
    for product_id, quantity in selected_products.items():
        price = get_product_price(product_id)
        total_amount += price * quantity
    return total_amount
