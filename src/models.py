from src import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from werkzeug.security import check_password_hash, generate_password_hash

from src.main import login_manager


class Producto(db.Base):
    """
    Create a product (productos) table. This table stores the company's products
    """

    __tablename__ = "producto"
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(20), nullable=False)
    categoria = Column(Integer(), nullable=False)
    stock = Column(Integer(), nullable=False)

    def __init__(self, contenido, categoria, stock):
        self.descripcion = contenido
        self.categoria = categoria
        self.stock = stock

    def __repr__(self):
        return "Tarea {}: {} ({}) ({})".format(self.id, self.descripcion, self.categoria, self.stock)

    def __str__(self):
        return "Tarea {}: {} ({}) ({})".format(self.id, self.descripcion, self.categoria, self.stock)


class Compra(db.Base):
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


class Venta(db.Base):
    """
    Create a sell (venta) table. This table stores the sells done by company
    """

    __tablename__ = "venta"
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("producto.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
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


class Usuario(UserMixin, db.Base):
    """
    Create a User (usuario) table. This table stores the users.
    UserMixin (from flask_login library) provides the implementation for the properties:
        - is_authenticated() method that returns True if the user has provided valid credentials
        - is_active() method that returns True if the user’s account is active
        - is_anonymous() method that returns True if the current user is an anonymous user
        - get_id() method which, given a User instance, returns the unique ID for that object
    """

    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(120), index=True, unique=False, nullable=False)
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

    def __init__(self, fullname, email, username, password, is_admin=False):
        self.fullname = fullname
        self.email = email
        self.username = username
        # More about the method below: https://tedboy.github.io/flask/generated/werkzeug.generate_password_hash.html
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def __repr__(self):
        return f"<User: {self.username}>"


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
