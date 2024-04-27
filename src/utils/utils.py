import os
from pathlib import Path

from flask import current_app
from unidecode import unidecode
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from src import db
from src.models import Usuario, Producto


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


def build_sample_db():
    """
    Populate db with some entries.
    """
    print("Initial database population...")
    db.drop_all()
    db.create_all()

    # Create an admin
    admin_user = Usuario(
        nombre="admin",
        apellido="admin",
        email="admin@admin.com",
        username="admin",
        is_admin=True,
        password=generate_password_hash("admin"),
    )
    db.session.add(admin_user)

    # Create other no admin users
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

    for i in range(len(first_names)):
        first_name = first_names[i]
        last_name = last_names[i]
        email = f"{unidecode(first_name).lower()}@{unidecode(last_name).lower()}.com"
        username = f"{unidecode(first_name).lower()}_{unidecode(last_name).lower()}"
        usuario = Usuario(
            nombre=first_name,
            apellido=last_name,
            email=email,
            username=username,
            password=generate_password_hash("123456", method="pbkdf2:sha256"),
        )
        db.session.add(usuario)

    db.session.commit()

    # Create productos for each category available
    productos = {
        "sin_categorias": [
            {
                "nombre": "Ultra Compact Lightwight",
                "descripcion": "Descripción del Ultra Compact Lightwight",
                "categoria": "Sin categoría",
                "precio": 29.99,
                "stock": 100,
                "image_name": "images/ultra-compact-lightwight.png",
            },
            {
                "nombre": "Reeferman Genetics Herb Grinder Metal",
                "descripcion": "Descripción del Reeferman Genetics Herb Grinder Metal",
                "categoria": "Sin categoría",
                "precio": 19.50,
                "stock": 80,
                "image_name": "images/reeferman-genetics-herb-grinder-metal.png",
            },
            {
                "nombre": "Carrete Electrico Para Pescar",
                "descripcion": "Descripción del Carrete Electrico Para Pescar",
                "categoria": "Sin categoría",
                "precio": 34.75,
                "stock": 120,
                "image_name": "images/carrete-electrico-para-pescar.jpg",
            },
            {
                "nombre": "Pelota Metálica Digital",
                "descripcion": "Descripción del Pelota Metálica Digital",
                "categoria": "Sin categoría",
                "precio": 25.00,
                "stock": 60,
                "image_name": "images/pelota-metalica-digital.png",
            },
            {
                "nombre": "Rubiks Cubo",
                "descripcion": "Descripción del Rubiks Cubo",
                "categoria": "Sin categoría",
                "precio": 39.50,
                "stock": 150,
                "image_name": "images/generic-product.png",
            },
        ],
        "laptops": [
            {
                "nombre": "Laptop Premium X",
                "descripcion": "Increíble Laptop con características premium",
                "categoria": "Laptop",
                "precio": 1599.99,
                "stock": 20,
                "image_name": "images/laptop-premium-x.png",
            },
            {
                "nombre": "Laptop Ultraligera Y",
                "descripcion": "Laptop ultraligera, perfecta para viajes",
                "categoria": "Laptop",
                "precio": 1299.50,
                "stock": 15,
                "image_name": "images/laptop-ultraligera-y.png",
            },
            {
                "nombre": "Laptop Gamer Z",
                "descripcion": "Potente laptop diseñada para juegos intensivos",
                "categoria": "Laptop",
                "precio": 1799.75,
                "stock": 10,
                "image_name": "images/laptop-gamer-z.png",
            },
            {
                "nombre": "Laptop Todo Terreno A1",
                "descripcion": "Laptop resistente y duradera para cualquier entorno",
                "categoria": "Laptop",
                "precio": 1499.00,
                "stock": 25,
                "image_name": "images/laptop-todo-terreno-a1.png",
            },
            {
                "nombre": "Laptop Económica B2",
                "descripcion": "Laptop asequible con buen rendimiento",
                "categoria": "Laptop",
                "precio": 899.99,
                "stock": 30,
                "image_name": "images/laptop-economica-b2.png",
            },
        ],
        "desktops": [
            {
                "nombre": "PC de Escritorio Potente X",
                "descripcion": "Potente computadora de escritorio para uso profesional",
                "categoria": "Desktop",
                "precio": 2299.99,
                "stock": 12,
                "image_name": "images/pc-de-escritorio-potente-x.png",
            },
            {
                "nombre": "PC de Escritorio Compacta Y",
                "descripcion": "Computadora de escritorio compacta, ideal para espacios reducidos",
                "categoria": "Desktop",
                "precio": 1499.50,
                "stock": 18,
                "image_name": "images/pc-de-escritorio-compacta-y.png",
            },
            {
                "nombre": "PC de Escritorio Gamer Z",
                "descripcion": "Computadora de escritorio diseñada para juegos de alta gama",
                "categoria": "Desktop",
                "precio": 1999.75,
                "stock": 8,
                "image_name": "images/pc-de-escritorio-gamer-z.png",
            },
            {
                "nombre": "PC de Escritorio Todo en Uno A1",
                "descripcion": "Computadora de escritorio todo en uno con pantalla integrada",
                "categoria": "Desktop",
                "precio": 1799.00,
                "stock": 15,
                "image_name": "images/pc-de-escritorio-todo-en-uno-a1.png",
            },
            {
                "nombre": "PC de Escritorio Básica B2",
                "descripcion": "Computadora de escritorio básica para tareas diarias",
                "categoria": "Desktop",
                "precio": 899.99,
                "stock": 25,
                "image_name": "images/pc-de-escritorio-basica-b2.png",
            },
        ],
        "perifericos": [
            {
                "nombre": "Teclado Mecánico Gaming X",
                "descripcion": "Teclado mecánico con retroiluminación RGB para jugadores",
                "categoria": "Periférico",
                "precio": 99.99,
                "stock": 50,
                "image_name": "images/teclado-mecánico-gaming-x.png",
            },
            {
                "nombre": "Ratón Inalámbrico Ergonómico Y",
                "descripcion": "Ratón inalámbrico ergonómico con sensor de alta precisión",
                "categoria": "Periférico",
                "precio": 49.50,
                "stock": 40,
                "image_name": "images/raton-inalambrico-ergonomico-y.png",
            },
            {
                "nombre": "Auriculares con Cancelación de Ruido Z",
                "descripcion": "Auriculares inalámbricos con cancelación de ruido para una experiencia inmersiva",
                "categoria": "Periférico",
                "precio": 129.75,
                "stock": 30,
                "image_name": "images/auriculares-con-cancelacion-de-ruido-z.png",
            },
            {
                "nombre": "Monitor Curvo de 27 Pulgadas A1",
                "descripcion": "Monitor curvo de alta resolución para una visualización envolvente",
                "categoria": "Periférico",
                "precio": 299.00,
                "stock": 20,
                "image_name": "images/monitor-curvo-de-27-pulgadas-a1.png",
            },
            {
                "nombre": "Impresora Multifuncional B2",
                "descripcion": "Impresora multifuncional para hogar y oficina",
                "categoria": "Periférico",
                "precio": 149.99,
                "stock": 35,
                "image_name": "images/impresora-multifuncional-b2.png",
            },
        ],
        "otros": [
            {
                "nombre": "Gadget Innovador X",
                "descripcion": "Gadget innovador con múltiples funciones",
                "categoria": "Otros",
                "precio": 79.99,
                "stock": 25,
                "image_name": "images/gadget-innovador-x.png",
            },
            {
                "nombre": "Accesorio Tecnológico Único Y",
                "descripcion": "Accesorio tecnológico único para mejorar la experiencia del usuario",
                "categoria": "Otros",
                "precio": 59.50,
                "stock": 15,
                "image_name": "images/accesorio-tecnológico-unico-y.png",
            },
            {
                "nombre": "Dispositivo Inteligente para el Hogar Z",
                "descripcion": "Dispositivo inteligente para el hogar con conectividad avanzada",
                "categoria": "Otros",
                "precio": 129.75,
                "stock": 12,
                "image_name": "images/dispositivo-iInteligente-para-el-hogar-z.png",
            },
            {
                "nombre": "Gafas de Realidad Virtual A1",
                "descripcion": "Gafas de realidad virtual para una experiencia inmersiva",
                "categoria": "Otros",
                "precio": 199.00,
                "stock": 18,
                "image_name": "images/gafas-de-realidad-virtual-a1.png",
            },
            {
                "nombre": "Batería Externa de Alta Capacidad B2",
                "descripcion": "Batería externa de alta capacidad para cargar dispositivos móviles",
                "categoria": "Otros",
                "precio": 49.99,
                "stock": 40,
                "image_name": "images/bateria-externa-de-alta-capacidad-b2.png",
            },
        ],
    }

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

    # Create some sample products for some users
    users = Usuario.query.all()
    products = Producto.query.all()
    products_per_user = len(products) // len(users)

    for user in users:
        # Use random products for each user
        user.productos = products[:products_per_user]

        # Remove the assigned products from the available products list
        products = products[products_per_user:]

        db.session.add(user)

    db.session.commit()

    return
