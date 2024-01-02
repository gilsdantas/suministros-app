"""empty message

Revision ID: 93a2e3cc9493
Revises:
Create Date: 2024-01-02 16:03:35.004141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "93a2e3cc9493"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "producto",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("descripcion", sa.String(length=20), nullable=False),
        sa.Column("categoria", sa.Integer(), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("producto", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_producto_categoria"), ["categoria"], unique=False)
        batch_op.create_index(batch_op.f("ix_producto_descripcion"), ["descripcion"], unique=False)
        batch_op.create_index(batch_op.f("ix_producto_nombre"), ["nombre"], unique=True)

    op.create_table(
        "usuario",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("apellido", sa.String(length=120), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=80), nullable=False),
        sa.Column("password_hash", sa.String(length=128), nullable=True),
        sa.Column("is_admin", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("usuario", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_usuario_apellido"), ["apellido"], unique=False)
        batch_op.create_index(batch_op.f("ix_usuario_email"), ["email"], unique=True)
        batch_op.create_index(batch_op.f("ix_usuario_nombre"), ["nombre"], unique=False)
        batch_op.create_index(batch_op.f("ix_usuario_username"), ["username"], unique=True)

    op.create_table(
        "compra",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("producto_id", sa.Integer(), nullable=False),
        sa.Column("cantidad", sa.Integer(), nullable=False),
        sa.Column("fecha_de_compra", sa.String(length=23), nullable=False),
        sa.ForeignKeyConstraint(
            ["producto_id"],
            ["producto.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "venta",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("producto_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("cantidad", sa.Integer(), nullable=False),
        sa.Column("fecha_de_venta", sa.String(length=23), nullable=False),
        sa.ForeignKeyConstraint(
            ["producto_id"],
            ["producto.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["usuario.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("venta")
    op.drop_table("compra")
    with op.batch_alter_table("usuario", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_usuario_username"))
        batch_op.drop_index(batch_op.f("ix_usuario_nombre"))
        batch_op.drop_index(batch_op.f("ix_usuario_email"))
        batch_op.drop_index(batch_op.f("ix_usuario_apellido"))

    op.drop_table("usuario")
    with op.batch_alter_table("producto", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_producto_nombre"))
        batch_op.drop_index(batch_op.f("ix_producto_descripcion"))
        batch_op.drop_index(batch_op.f("ix_producto_categoria"))

    op.drop_table("producto")
    # ### end Alembic commands ###
