# Built-in imports
import base64
from collections import defaultdict
from datetime import datetime, timedelta
from io import BytesIO

# Thirty part imports
import matplotlib

matplotlib.use("agg")  # Using Non-GUI Backend
import matplotlib.pyplot as plt
import pandas as pd
from flask import render_template, abort, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from werkzeug.utils import redirect

# Local imports
from . import home
from ..models import Producto, Usuario, Venta


@home.route("/")
@home.route("/index")
def homepage():
    """
    Render the homepage templates on the '/' or '/index' route
    """
    carousel_products = Producto.query.order_by(func.random()).limit(15).all()
    return render_template("home/index.html", title="Home", carousel_products=carousel_products)


@home.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)

    registration_dates = [parse_date(usuario.fecha_de_registro) for usuario in Usuario.query.all()]
    sales_current_month = fetch_sales_data_current_month()
    top_selling_products = identify_top_selling_products(sales_current_month)

    user_chart_image = generate_user_chart(registration_dates)
    product_chart_image = generate_product_chart()
    monthly_sales_chart_image = generate_monthly_sales_chart(sales_current_month)

    return render_template(
        "home/admin_dashboard.html",
        user_chart_image=user_chart_image,
        product_chart_image=product_chart_image,
        monthly_sales_chart_image=monthly_sales_chart_image,
        top_selling_products=top_selling_products,
    )


@home.route("/usuarios/dashboard")
@login_required
def dashboard():
    """
    Render the dashboard template on the /usuarios/dashboard route
    """
    return redirect(url_for("usuario_bp.dashboard", usuario_id=current_user.id))


def parse_date(date_str):
    """
    Parse the date string into a datetime object
    """
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")


def fetch_sales_data():
    try:
        sales = Venta.query.all()
        sales_data = [sale.fecha_de_venta for sale in sales]
        return sales_data
    except Exception as e:
        print(f"Error fetching sales data: {str(e)}")
        return []


def fetch_sales_data_current_month():
    """
    Fetch sales data for the current month
    """
    current_month = datetime.now().month
    current_year = datetime.now().year
    start_date = datetime(current_year, current_month, 1)
    end_date = start_date + timedelta(days=30)  # Assuming each month has 30 days for simplicity
    return Venta.query.filter(Venta.fecha_de_venta >= start_date, Venta.fecha_de_venta <= end_date).all()


def calculate_daily_sales_current_month(sales_current_month):
    daily_sales = {}
    for sale in sales_current_month:
        sale_date = sale.fecha_de_venta  # Accessing the 'fecha_de_venta' attribute directly
        if sale_date:  # Check if the date object is not None
            sale_day = sale_date.day
            if sale_day in daily_sales:
                daily_sales[sale_day] += 1
            else:
                daily_sales[sale_day] = 1
    return daily_sales


# Function to identify top-selling products for the current month
def identify_top_selling_products(sales_current_month, n=5):
    sales_data = [(sale.producto.nombre, sale.producto.precio * sale.cantidad) for sale in sales_current_month]
    sales_df = pd.DataFrame(sales_data, columns=["Product", "Sales Amount"])
    top_selling_products = sales_df.groupby("Product")["Sales Amount"].sum().nlargest(n)

    plt.figure(figsize=(10, 6))
    top_selling_products.plot(kind="bar", color="purple")
    plt.title(f"Top {n} Selling Products for the Current Month")
    plt.xlabel("Product")
    plt.ylabel("Total Sales Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the chart to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the image as base64 for embedding in HTML
    chart_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    plt.close()  # Close the plot to avoid memory leaks

    return chart_image


def generate_user_chart(registration_dates):
    plt.figure(figsize=(8, 6))
    plt.hist(registration_dates, bins=20, color="blue", alpha=0.7)
    plt.title("Distribución de Fechas de Registro de Usuarios")
    plt.xlabel("Fecha de Registro")
    plt.ylabel("Numero de usuarios")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the chart to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the image as base64 for embedding in HTML
    chart_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    plt.close()  # Close the plot to avoid memory leaks

    return chart_image


def generate_product_chart():
    # Fetch sales data for each product
    products = Producto.query.all()
    product_sales = [(product.nombre, sum([venta.cantidad for venta in product.ventas])) for product in products]

    # Sort products based on the number of sales
    product_sales.sort(key=lambda x: x[1], reverse=True)

    # Select the top 10 products to display
    top_n = 10  # We can adjust this value based on how many top products we want to display

    # Extract product names and sales counts for plotting
    top_product_names = [product[0] for product in product_sales[:top_n]]
    top_product_sales = [product[1] for product in product_sales[:top_n]]

    # Create a bar chart for the top N products
    plt.figure(figsize=(10, 6))
    plt.bar(top_product_names, top_product_sales, color="purple")
    plt.title(f"Principales {top_n} productos por ventas")
    plt.xlabel("Producto")
    plt.ylabel("Número de ventas")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the chart to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the image as base64 for embedding in HTML
    chart_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return chart_image


def generate_monthly_sales_chart(sales_current_month):
    # Initialize a dictionary to store daily sales amounts
    daily_sales_data = defaultdict(float)

    # Iterate through the sales for the current month and aggregate sales by day
    for sale in sales_current_month:
        day = sale.fecha_de_venta.day
        daily_sales_data[day] += sale.producto.precio * sale.cantidad

    # Extract days and corresponding sales amounts
    days = list(daily_sales_data.keys())
    sales_amounts = list(daily_sales_data.values())

    # Create a bar chart for the daily sales amount for the current month
    plt.figure(figsize=(10, 6))
    plt.bar(days, sales_amounts, color="orange")
    plt.title("Ventas diarias del mes actual")
    plt.xlabel("Día")
    plt.ylabel("Cantidad de ventas")
    plt.tight_layout()

    # Save the chart to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the image as base64 for embedding in HTML
    chart_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return chart_image
