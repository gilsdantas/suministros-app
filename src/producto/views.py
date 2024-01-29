# src/producto/views.py
from flask import redirect, url_for, render_template, request, session

from decimal import Decimal
from . import producto
from ..models import Producto


@producto.route("/producto/lista-productos", methods=("GET", "POST"))
def lista_productos():
    page = request.args.get("page", 1, type=int)
    productos = Producto.query.filter(Producto.stock > 0).paginate(page=page, per_page=10, error_out=False)

    if request.method == "POST":
        selected_products = request.form.getlist("selected_products[]")
        quantities = {}

        for product_id in selected_products:
            quantity_key = f"product_quantity_{product_id}"
            quantity_value = request.form.get(quantity_key, 0)
            if quantity_value == "undefined":
                quantity_value = 0

            quantities[product_id] = int(quantity_value)

        # Store the selected products and quantities in the session
        session["selected_products"] = quantities

        return redirect(url_for("producto.review_checkout"))

    return render_template(
        "productos/productos.html", productos=productos, title="Lista productos", get_product_name=get_product_name
    )


@producto.route("/producto/review-checkout", methods=("GET", "POST"))
def review_checkout():
    # Retrieve selected products and quantities from the session
    selected_products = session.get("selected_products", {})
    print(f"selected_products: ", selected_products)

    # ToDo: Process the data, e.g., update the database, send confirmation emails, etc.

    return render_template(
        "productos/review_checkout.html", selected_products=selected_products, get_product_name=get_product_name
    )


@producto.route("/producto/confirm-checkout", methods=["POST"])
def confirm_checkout():
    # Retrieve selected products and quantities from the session
    selected_products = session.get("selected_products", {})

    # Process the data, e.g., update the database, send confirmation emails, etc.

    return render_template("productos/confirm_checkout.html", selected_products=selected_products)


@producto.route("/producto/buy-products", methods=["POST"])
def buy_products():
    selected_product_ids = request.form.getlist("selected_products")

    # Implement logic to create entries in the Sell table and update Product stock

    # Clear the session after completing the purchase
    session.pop("selected_products", None)

    return redirect(url_for("producto.lista_productos"))


def get_product_name(product_id):
    prod = Producto.query.get(product_id)
    return prod.nombre if prod else "Producto desconocido"
