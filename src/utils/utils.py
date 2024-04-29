# built-in imports
import datetime
import random
from pathlib import Path

# Third-party imports
from flask import current_app
from unidecode import unidecode
from werkzeug.utils import secure_filename

# Local imports
from src.utils.sample_products_data import productos
from src import db
from src.models import Usuario, Producto, Venta


def read_an_image(image_name: str):
    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    image_path = upload_folder / "images" / secure_filename(image_name)

    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
    except FileNotFoundError:
        with open(upload_folder / "images" / "generic-product.png", "rb") as f:
            image_data = f.read()

    print(f"---> image_data: {image_data}")
    return image_data


def create_admin():
    """
    Create an admin user.
    """
    admin_registration_date = datetime.datetime.now() - datetime.timedelta(days=3 * 365)
    admin_user = Usuario(
        nombre="admin",
        apellido="admin",
        email="admin@admin.com",
        username="admin",
        fecha_de_registro=admin_registration_date,
        is_admin=True,
        password="admin",
    )
    db.session.add(admin_user)
    db.session.commit()


def create_users():
    """
    Create non-admin users.
    """
    first_names = ["Ana", "Maria", "Laura", "Isabel", "Elena", "Juan", "Carlos", "José", "Antonio", "Francisco"]
    last_names = [
        "García",
        "Rodríguez",
        "López",
        "Martínez",
        "González",
        "Hernández",
        "Pérez",
        "Sánchez",
        "Ramírez",
        "Fernández",
    ]

    start_date = datetime.datetime.now() - datetime.timedelta(days=2 * 365)
    end_date = datetime.datetime.now() - datetime.timedelta(days=1)

    for i in range(len(first_names)):
        first_name = first_names[i]
        last_name = last_names[i]
        email = f"{unidecode(first_name).lower()}@{unidecode(last_name).lower()}.com"
        username = f"{unidecode(first_name).lower()}_{unidecode(last_name).lower()}"
        random_registration_date = random_date(start_date, end_date)
        usuario = Usuario(
            nombre=first_name,
            apellido=last_name,
            email=email,
            fecha_de_registro=random_registration_date,
            username=username,
            password="123456",
        )
        db.session.add(usuario)
    db.session.commit()


def create_products():
    """
    Create products for each category.
    """

    for key, values in productos.items():
        for value in values:
            producto = Producto(
                nombre=value.get("nombre", "Producto sin nombre"),
                descripcion=value.get("descripcion", "Producto sin descripción"),
                categoria=value.get("categoria", "Sin categoría"),
                precio=value.get("precio", 0.0),
                stock=value.get("stock", 0),
                image=value.get("image_name", read_an_image("generic-product.png")),
            )
            db.session.add(producto)
    db.session.commit()


def create_sales():
    """
    Create some sample sales.
    """
    product_ids = [product.id for product in Producto.query.all()]
    user_ids = [user.id for user in Usuario.query.all()]

    sales_data = []

    start_date = datetime.datetime.now() - datetime.timedelta(days=2 * 365)
    end_date = datetime.datetime.now() - datetime.timedelta(days=1)

    for _ in range(100):
        producto_id = random.choice(product_ids)
        usuario_id = random.choice(user_ids)
        cantidad = random.randint(1, 10)
        fecha_de_venta = random_date(start_date, end_date)
        sale = Venta(producto_id=producto_id, usuario_id=usuario_id, cantidad=cantidad, fecha_de_venta=fecha_de_venta)
        sales_data.append(sale)
        product = Producto.query.get(producto_id)
        if product:
            product.stock -= cantidad

    db.session.add_all(sales_data)
    db.session.commit()


def build_sample_db():
    """
    Populate db with some entries.
    """
    print("Initial database population...")
    db.drop_all()
    db.create_all()

    create_admin()
    create_users()
    create_products()
    create_sales()

    return


# Function to generate a random date within a given range
def random_date(start_date, end_date):
    return start_date + datetime.timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
