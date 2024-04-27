# Built-in imports
import os
from datetime import datetime
from pathlib import Path

from flask import current_app

# Thirty part imports
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, Table, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

# Local imports
# from src import db

db = SQLAlchemy()

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
    image = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Establishing the relationship between Usuario and Producto and Ventas
    usuarios = relationship("Usuario", secondary=usuario_producto, back_populates="productos")
    ventas = relationship("Venta", back_populates="producto")

    def save_images(self, image_file):
        filename = secure_filename(image_file.filename)
        file_path = Path("images") / filename
        file_full_path = current_app.config["UPLOAD_FOLDER"] / file_path
        image_file.save(str(file_full_path))
        self.image = str(file_path)

    def __init__(self, nombre, descripcion, categoria, precio, stock, image):
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.image = image

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
        self.password = generate_password_hash(password, method="pbkdf2:sha256")
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
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_de_venta = Column(String(23), nullable=False)

    # Establishing the one-to-many relationship with Producto
    producto = relationship("Producto", back_populates="ventas")

    def __init__(self, producto_id, usuario_id, cantidad, fecha_de_venta):
        self.producto_id = producto_id
        self.usuario_id = usuario_id
        self.cantidad = cantidad
        self.fecha_de_venta = fecha_de_venta

    def __repr__(self):
        return f"Venta {self.id}: ({self.producto_id}) ({self.usuario_id}) ({self.cantidad}) ({self.fecha_de_venta})"

    def __str__(self):
        return f"Venta {self.id}: ({self.producto_id}) ({self.usuario_id}) ({self.cantidad}) ({self.fecha_de_venta})"
