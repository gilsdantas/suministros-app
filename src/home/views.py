# Built-in imports
import base64
import json
from collections import defaultdict
from datetime import datetime, timedelta
from io import BytesIO

# Thirty part imports
import matplotlib

matplotlib.use("agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import render_template, abort, url_for
from flask_login import login_required, current_user

from sqlalchemy import func, extract
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

    num_users = Usuario.query.count()
    registration_dates = [
        datetime.strptime(usuario.fecha_de_registro, "%Y-%m-%d %H:%M:%S.%f") for usuario in Usuario.query.all()
    ]
    num_products = Producto.query.distinct(Producto.id).count()
    total_sales_all_time = calculate_total_sales_all_time()
    sales_current_month = fetch_sales_data_current_month()
    daily_sales_current_month = calculate_daily_sales_current_month(sales_current_month)
    total_sales_month = sum(daily_sales_current_month)
    total_sales_by_month = calculate_total_sales_by_month()
    visualize_total_sales_by_month(total_sales_by_month)
    visualize_sales_distribution_by_category(sales_current_month)
    top_selling_products = identify_top_selling_products(sales_current_month)

    user_chart_image = generate_user_chart(registration_dates)
    sales_chart_image = generate_sales_chart(sales_current_month, total_sales_all_time, total_sales_month)
    product_chart_image = generate_product_chart()
    monthly_sales_chart_image = generate_monthly_sales_chart(sales_current_month)

    return render_template(
        "home/admin_dashboard.html",
        user_chart_image=user_chart_image,
        sales_chart_image=sales_chart_image,
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
    print(f"=====> Current user Id: {current_user.id}")
    return redirect(url_for("usuario_bp.dashboard", usuario_id=current_user.id))


def fetch_sales_data():
    try:
        sales = Venta.query.all()
        sales_data = [sale.fecha_de_venta for sale in sales]
        return sales_data
    except Exception as e:
        print(f"Error fetching sales data: {str(e)}")
        return []


def fetch_sales_data_current_month():
    try:
        current_month = datetime.now().month
        current_year = datetime.now().year
        start_date = datetime(current_year, current_month, 1)
        end_date = start_date + timedelta(days=30)  # Assuming each month has 30 days for simplicity
        sales_current_month = Venta.query.filter(
            Venta.fecha_de_venta >= start_date, Venta.fecha_de_venta <= end_date
        ).all()

        return sales_current_month
    except Exception as e:
        print(f"Error fetching sales data for the current month: {str(e)}")
        return []


def calculate_total_sales_all_time():
    sales = Venta.query.all()
    total_amount = sum(s.producto.precio * s.cantidad for s in sales)
    return total_amount


# Function to calculate total sales amount for the current month and previous months
def calculate_total_sales_by_month():
    current_month = datetime.now().month
    current_year = datetime.now().year
    total_sales_by_month = {}
    for month in range(1, current_month + 1):
        start_date = datetime(current_year, month, 1)
        end_date = start_date + timedelta(days=30)  # Assuming each month has 30 days for simplicity
        sales_month = Venta.query.filter(Venta.fecha_de_venta >= start_date, Venta.fecha_de_venta <= end_date).all()
        total_amount_month = sum(s.producto.precio * s.cantidad for s in sales_month)
        total_sales_by_month[start_date.strftime("%B")] = total_amount_month
    return total_sales_by_month


def calculate_daily_sales_current_month(sales_current_month):
    daily_sales = {}
    for sale in sales_current_month:
        print(f"---> sale: {sale}")
        sale_date = sale.fecha_de_venta  # Accessing the 'fecha_de_venta' attribute directly
        if sale_date:  # Check if the date object is not None
            sale_day = sale_date.day
            if sale_day in daily_sales:
                daily_sales[sale_day] += 1
            else:
                daily_sales[sale_day] = 1
    return daily_sales


# Function to visualize total sales amount by month
def visualize_total_sales_by_month(total_sales_by_month):
    months = list(total_sales_by_month.keys())
    sales_amounts = list(total_sales_by_month.values())

    plt.figure(figsize=(10, 6))
    plt.bar(months, sales_amounts, color="blue")
    plt.title("Total Sales Amount by Month")
    plt.xlabel("Month")
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


# Function to visualize sales distribution by product category for the current month
def visualize_sales_distribution_by_category(sales_current_month):
    sales_data = [(sale.producto.categoria, sale.producto.precio * sale.cantidad) for sale in sales_current_month]
    sales_df = pd.DataFrame(sales_data, columns=["Category", "Sales Amount"])
    sales_by_category = sales_df.groupby("Category")["Sales Amount"].sum().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sales_by_category.plot(kind="bar", color="green")
    plt.title("Sales Distribution by Product Category (Current Month)")
    plt.xlabel("Product Category")
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
    plt.title("Distribution of User Registration Dates")
    plt.xlabel("Registration Date")
    plt.ylabel("Number of Users")
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

    # Select the top N products to display
    top_n = 10  # You can adjust this value based on how many top products you want to display

    # Extract product names and sales counts for plotting
    top_product_names = [product[0] for product in product_sales[:top_n]]
    top_product_sales = [product[1] for product in product_sales[:top_n]]

    # Create a bar chart for the top N products
    plt.figure(figsize=(10, 6))
    plt.bar(top_product_names, top_product_sales, color="purple")
    plt.title(f"Top {top_n} Products by Sales")
    plt.xlabel("Product")
    plt.ylabel("Number of Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the chart to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the image as base64 for embedding in HTML
    chart_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return chart_image


def generate_sales_chart(sales_data, total_sales_all_time, total_sales_month, period="monthly"):
    # Extract the sale dates from the list of Venta objects
    sale_dates = [sale.fecha_de_venta for sale in sales_data]

    # Convert sales data to a DataFrame
    sales_df = pd.DataFrame({"date": sale_dates, "sales": 1})

    # Set the 'date' column as the index
    sales_df["date"] = pd.to_datetime(sales_df["date"])  # This line is causing the error
    sales_df.set_index("date", inplace=True)

    # Resample the sales data based on the specified period (e.g., monthly, quarterly)
    if period == "monthly":
        sales_df_resampled = sales_df.resample("M").sum().asfreq("M", fill_value=0)
    elif period == "quarterly":
        sales_df_resampled = sales_df.resample("Q").sum()
    else:
        raise ValueError("Invalid period. Please specify 'monthly' or 'quarterly'.")

    # Create a line chart for the sales data
    plt.figure(figsize=(10, 6))
    plt.plot(sales_df_resampled.index, sales_df_resampled["sales"], marker="o", linestyle="-")
    plt.title(f"Sales Trend ({period.capitalize()} Sales)")
    plt.xlabel("Date")
    plt.ylabel("Number of Sales")
    plt.grid(True)
    plt.xticks(rotation=45)

    # Annotate total sales amounts on the chart
    plt.text(
        sales_df_resampled.index[-1],
        sales_df_resampled["sales"].iloc[-1],
        f"Total All Time: ${total_sales_all_time:.2f}",
        ha="right",
        va="bottom",
    )
    plt.text(
        sales_df_resampled.index[-1],
        sales_df_resampled["sales"].iloc[-1],
        f"Total This Month: ${total_sales_month:.2f}",
        ha="right",
        va="top",
    )

    plt.tight_layout()

    # Save the chart to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the image as base64 for embedding in HTML
    chart_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    plt.close()  # Close the plot to avoid memory leaks

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
    plt.title("Daily Sales for Current Month")
    plt.xlabel("Day")
    plt.ylabel("Sales Amount")
    plt.tight_layout()

    # Save the chart to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the image as base64 for embedding in HTML
    chart_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return chart_image
