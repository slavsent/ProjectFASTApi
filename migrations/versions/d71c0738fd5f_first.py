"""First

Revision ID: d71c0738fd5f
Revises:
Create Date: 2023-01-16 11:15:26.726921

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd71c0738fd5f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'dish',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_dish_title'), 'dish', ['title'], unique=True)
    op.create_table(
        'menu',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('submenus_count', sa.Integer(), nullable=True),
        sa.Column('dishes_count', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_menu_title'), 'menu', ['title'], unique=True)
    op.create_table(
        'submenu',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('dishes_count', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_submenu_title'),
        'submenu', ['title'], unique=True,
    )
    op.create_table(
        'dish_in_submenu',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('submenu', postgresql.UUID(), nullable=True),
        sa.Column('dish', postgresql.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['dish'], ['dish.id']),
        sa.ForeignKeyConstraint(['submenu'], ['submenu.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('dish'),
    )
    op.create_table(
        'submenu_in_menu',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('menu', postgresql.UUID(), nullable=True),
        sa.Column('submenu', postgresql.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['menu'], ['menu.id']),
        sa.ForeignKeyConstraint(['submenu'], ['submenu.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('submenu'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('submenu_in_menu')
    op.drop_table('dish_in_submenu')
    op.drop_index(op.f('ix_submenu_title'), table_name='submenu')
    op.drop_table('submenu')
    op.drop_index(op.f('ix_menu_title'), table_name='menu')
    op.drop_table('menu')
    op.drop_index(op.f('ix_dish_title'), table_name='dish')
    op.drop_table('dish')
    # ### end Alembic commands ###
