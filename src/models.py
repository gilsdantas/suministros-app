# Built-in imports
# Thirty part imports
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, Table
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

# Local imports
from src import db

# User-Product association table
usuario_producto = Table(
    "usuario_producto",
    db.Model.metadata,
    Column("usuario_id", Integer, ForeignKey("usuario.id")),
    Column("producto_id", Integer, ForeignKey("producto.id")),
)


class Producto(db.Model):
    """
    Create a product (productos) table. This table stores the company's products
    """

    __tablename__ = "producto"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), index=True, unique=True, nullable=False)
    descripcion = Column(String(20), index=True, nullable=True)
    categoria = Column(Integer(), index=True, nullable=False)
    precio = Column(Float(), index=True, nullable=False)
    stock = Column(Integer(), unique=False, nullable=False)

    # Establishing the relationship between Usuario and Producto and Ventas
    usuarios = relationship("Usuario", secondary=usuario_producto, back_populates="productos")
    ventas = relationship("Venta", back_populates="producto")

    def __init__(self, nombre, descripcion, categoria, precio, stock):
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    def __repr__(self):
        return (
            f"Producto {self.id}: ({self.nombre}) ({self.descripcion}) "
            f"({self.categoria}) ({self.precio}) ({self.stock})"
        )

    def __str__(self):
        return (
            f"Producto {self.id}: ({self.nombre}) ({self.descripcion}) "
            f"({self.categoria}) ({self.precio}) ({self.stock})"
        )


class Usuario(UserMixin, db.Model):
    """
    Create a User (usuarios) table. This table stores the usuarios.
    UserMixin (from flask_login library) provides the implementation for the properties:
        - is_authenticated() method that returns True if the usuarios has provided valid credentials
        - is_active() method that returns True if the usuarios’s account is active
        - is_anonymous() method that returns True if the current usuarios is an anonymous usuarios
        - get_id() method which, given a User instance, returns the unique ID for that object
    """

    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), index=True, unique=False, nullable=False)
    apellido = Column(String(120), index=True, unique=False, nullable=False)
    username = Column(String(50), index=True, unique=True, nullable=False)
    email = Column(String(80), index=True, unique=True, nullable=False)
    password = Column(String(128))
    is_admin = Column(Boolean, default=False)

    # Establishing the relationship between Usuario and Producto
    productos = relationship("Producto", secondary=usuario_producto, back_populates="usuarios")

    # Flask-Login integration: is_authenticated, is_active, and is_anonymous are methods from Flask-Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def check_password(self, password):
        """
        Check if hashed password matches with actual password
        """

        # More about the method below: https://tedboy.github.io/flask/generated/werkzeug.check_password_hash.html
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    def __init__(self, nombre, apellido, email, username, password, is_admin=False):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.username = username
        # More about the method below: https://tedboy.github.io/flask/generated/werkzeug.generate_password_hash.html
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def __repr__(self):
        return f"Usuario {self.id}: ({self.nombre}) ({self.apellido}) ({self.username}) ({self.email})"

    def __str__(self):
        return f"Usuario {self.id}: ({self.nombre}) ({self.apellido}) ({self.username}) ({self.email})"


class Compra(db.Model):
    """
    Create a purchase (compra) table. This table stores the purchases done by company
    """

    __tablename__ = "compra"
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("producto.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_de_compra = Column(String(23), nullable=False)

    def __init__(self, producto_id, cantidad, fecha_de_compra):
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.fecha_de_compra = fecha_de_compra

    def __repr__(self):
        return f"Compra {self.id}: ({self.producto_id}) ({self.cantidad}) " f"({self.fecha_de_compra})"

    def __str__(self):
        return f"Compra {self.id}: ({self.producto_id}) ({self.cantidad}) " f"({self.fecha_de_compra})"


class Venta(db.Model):
    """
    Create a sell (venta) table. This table stores the sells done by company
    """

    __tablename__ = "venta"
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("producto.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_de_venta = Column(String(23), nullable=False)

    # Establishing the one-to-many relationship with Producto
    producto = relationship("Producto", back_populates="ventas")

    def __init__(self, producto_id, user_id, cantidad, fecha_de_compra):
        self.producto_id = producto_id
        self.user_id = user_id
        self.cantidad = cantidad
        self.fecha_de_venta = fecha_de_compra

    def __repr__(self):
        return f"Venta {self.id}: ({self.producto_id}) ({self.user_id}) ({self.cantidad}) ({self.fecha_de_venta})"

    def __str__(self):
        return f"Venta {self.id}: ({self.producto_id}) ({self.user_id}) ({self.cantidad}) ({self.fecha_de_venta})"


def build_sample_db():
    """
    Populate db with some entries.
    """

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
        usuario = Usuario(
            nombre=first_names[i],
            apellido=last_names[i],
            email=f"{first_names[i].lower()}@{last_names[i].lower()}.com",
            username=f"{first_names[i].lower()}_{last_names[i].lower()}",
            password=generate_password_hash("123456", method="pbkdf2:sha256"),
        )
        db.session.add(usuario)

    db.session.commit()

    # Create productos for each category available
    productos = {
        "sin_categorias": [
            {
                "nombre": "Artículo sin Categoría 1",
                "descripcion": "Descripción del Artículo sin Categoría 1",
                "categoria": "Sin categoría",
                "precio": 29.99,
                "stock": 100,
            },
            {
                "nombre": "Artículo sin Categoría 2",
                "descripcion": "Descripción del Artículo sin Categoría 2",
                "categoria": "Sin categoría",
                "precio": 19.50,
                "stock": 80,
            },
            {
                "nombre": "Artículo sin Categoría 3",
                "descripcion": "Descripción del Artículo sin Categoría 3",
                "categoria": "Sin categoría",
                "precio": 34.75,
                "stock": 120,
            },
            {
                "nombre": "Artículo sin Categoría 4",
                "descripcion": "Descripción del Artículo sin Categoría 4",
                "categoria": "Sin categoría",
                "precio": 25.00,
                "stock": 60,
            },
            {
                "nombre": "Artículo sin Categoría 5",
                "descripcion": "Descripción del Artículo sin Categoría 5",
                "categoria": "Sin categoría",
                "precio": 39.50,
                "stock": 150,
            },
        ],
        "laptops": [
            {
                "nombre": "Laptop Premium X",
                "descripcion": "Increíble Laptop con características premium",
                "categoria": "Laptop",
                "precio": 1599.99,
                "stock": 20,
            },
            {
                "nombre": "Laptop Ultraligera Y",
                "descripcion": "Laptop ultraligera, perfecta para viajes",
                "categoria": "Laptop",
                "precio": 1299.50,
                "stock": 15,
            },
            {
                "nombre": "Laptop Gamer Z",
                "descripcion": "Potente laptop diseñada para juegos intensivos",
                "categoria": "Laptop",
                "precio": 1799.75,
                "stock": 10,
            },
            {
                "nombre": "Laptop Todo Terreno A1",
                "descripcion": "Laptop resistente y duradera para cualquier entorno",
                "categoria": "Laptop",
                "precio": 1499.00,
                "stock": 25,
            },
            {
                "nombre": "Laptop Económica B2",
                "descripcion": "Laptop asequible con buen rendimiento",
                "categoria": "Laptop",
                "precio": 899.99,
                "stock": 30,
            },
        ],
        "desktops": [
            {
                "nombre": "PC de Escritorio Potente X",
                "descripcion": "Potente computadora de escritorio para uso profesional",
                "categoria": "Desktop",
                "precio": 2299.99,
                "stock": 12,
            },
            {
                "nombre": "PC de Escritorio Compacta Y",
                "descripcion": "Computadora de escritorio compacta, ideal para espacios reducidos",
                "categoria": "Desktop",
                "precio": 1499.50,
                "stock": 18,
            },
            {
                "nombre": "PC de Escritorio Gamer Z",
                "descripcion": "Computadora de escritorio diseñada para juegos de alta gama",
                "categoria": "Desktop",
                "precio": 1999.75,
                "stock": 8,
            },
            {
                "nombre": "PC de Escritorio Todo en Uno A1",
                "descripcion": "Computadora de escritorio todo en uno con pantalla integrada",
                "categoria": "Desktop",
                "precio": 1799.00,
                "stock": 15,
            },
            {
                "nombre": "PC de Escritorio Básica B2",
                "descripcion": "Computadora de escritorio básica para tareas diarias",
                "categoria": "Desktop",
                "precio": 899.99,
                "stock": 25,
            },
        ],
        "perifericos": [
            {
                "nombre": "Teclado Mecánico Gaming X",
                "descripcion": "Teclado mecánico con retroiluminación RGB para jugadores",
                "categoria": "Periférico",
                "precio": 99.99,
                "stock": 50,
            },
            {
                "nombre": "Ratón Inalámbrico Ergonómico Y",
                "descripcion": "Ratón inalámbrico ergonómico con sensor de alta precisión",
                "categoria": "Periférico",
                "precio": 49.50,
                "stock": 40,
            },
            {
                "nombre": "Auriculares con Cancelación de Ruido Z",
                "descripcion": "Auriculares inalámbricos con cancelación de ruido para una experiencia inmersiva",
                "categoria": "Periférico",
                "precio": 129.75,
                "stock": 30,
            },
            {
                "nombre": "Monitor Curvo de 27 Pulgadas A1",
                "descripcion": "Monitor curvo de alta resolución para una visualización envolvente",
                "categoria": "Periférico",
                "precio": 299.00,
                "stock": 20,
            },
            {
                "nombre": "Impresora Multifuncional B2",
                "descripcion": "Impresora multifuncional para hogar y oficina",
                "categoria": "Periférico",
                "precio": 149.99,
                "stock": 35,
            },
        ],
        "otros": [
            {
                "nombre": "Gadget Innovador X",
                "descripcion": "Gadget innovador con múltiples funciones",
                "categoria": "Otros",
                "precio": 79.99,
                "stock": 25,
            },
            {
                "nombre": "Accesorio Tecnológico Único Y",
                "descripcion": "Accesorio tecnológico único para mejorar la experiencia del usuario",
                "categoria": "Otros",
                "precio": 59.50,
                "stock": 15,
            },
            {
                "nombre": "Dispositivo Inteligente para el Hogar Z",
                "descripcion": "Dispositivo inteligente para el hogar con conectividad avanzada",
                "categoria": "Otros",
                "precio": 129.75,
                "stock": 12,
            },
            {
                "nombre": "Gafas de Realidad Virtual A1",
                "descripcion": "Gafas de realidad virtual para una experiencia inmersiva",
                "categoria": "Otros",
                "precio": 199.00,
                "stock": 18,
            },
            {
                "nombre": "Batería Externa de Alta Capacidad B2",
                "descripcion": "Batería externa de alta capacidad para cargar dispositivos móviles",
                "categoria": "Otros",
                "precio": 49.99,
                "stock": 40,
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
