# Built-in imports
# Thirty part imports
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from werkzeug.security import check_password_hash, generate_password_hash

# Local imports
from src import login_manager, db


class Producto(db.Model):
    """
    Create a product (productos) table. This table stores the company's products
    """

    __tablename__ = "producto"
    id = Column(Integer, primary_key=True)
    # index=True is to improve the queries.
    # unique=True is to check if the data is already in the table
    nombre = Column(String(100), index=True, unique=True, nullable=False)
    descripcion = Column(String(20), index=True, unique=False, nullable=False)
    categoria = Column(Integer(), index=True, unique=False, nullable=False)
    stock = Column(Integer(), unique=False, nullable=False)

    def __init__(self, nombre, descripcion, categoria, stock):
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.stock = stock

    def __repr__(self):
        return "Tarea {}: {} ({}) ({}) ({})".format(self.id, self.nombre, self.descripcion, self.categoria, self.stock)

    def __str__(self):
        return "Tarea {}: {} ({}) ({}) ({})".format(self.id, self.nombre, self.descripcion, self.categoria, self.stock)


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
        return "Compra {}: {} ({}) ({})".format(self.id, self.producto_id, self.cantidad, self.fecha_de_compra)

    def __str__(self):
        return "Compra {}: {} ({}) ({})".format(self.id, self.producto_id, self.cantidad, self.fecha_de_compra)


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

    def __init__(self, producto_id, user_id, cantidad, fecha_de_compra):
        self.producto_id = producto_id
        self.user_id = user_id
        self.cantidad = cantidad
        self.fecha_de_venta = fecha_de_compra

    def __repr__(self):
        return "Venta {}: {} ({}) ({}) ({})".format(
            self.id, self.producto_id, self.user_id, self.cantidad, self.fecha_de_venta
        )

    def __str__(self):
        return "Venta {}: {} ({}) ({}) ({})".format(
            self.id, self.producto_id, self.user_id, self.cantidad, self.fecha_de_venta
        )


class Usuario(UserMixin, db.Model):
    """
    Create a User (usuario) table. This table stores the usuarios.
    UserMixin (from flask_login library) provides the implementation for the properties:
        - is_authenticated() method that returns True if the usuario has provided valid credentials
        - is_active() method that returns True if the usuario’s account is active
        - is_anonymous() method that returns True if the current usuario is an anonymous usuario
        - get_id() method which, given a User instance, returns the unique ID for that object
    """

    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), index=True, unique=False, nullable=False)
    apellido = Column(String(120), index=True, unique=False, nullable=False)
    username = Column(String(50), index=True, unique=True, nullable=False)
    email = Column(String(80), index=True, unique=True, nullable=False)
    password_hash = Column(String(128))
    is_admin = Column(Boolean, default=False)

    def check_password(self, password):
        """
        Check if hashed password matches with actual password
        """

        # More about the method below: https://tedboy.github.io/flask/generated/werkzeug.check_password_hash.html
        return check_password_hash(self.password_hash, password)

    def __init__(self, nombre, apellido, email, username, password, is_admin=False):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.username = username
        # More about the method below: https://tedboy.github.io/flask/generated/werkzeug.generate_password_hash.html
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def __repr__(self):
        return "User {}: {} ({}) ({}) ({})".format(self.id, self.nombre, self.apellido, self.username, self.email)

    def __str__(self):
        return "User {}: {} ({}) ({}) ({})".format(self.id, self.nombre, self.apellido, self.username, self.email)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
