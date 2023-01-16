"""End6

Revision ID: d4c7d6984fe0
Revises: 731f4e479e08
Create Date: 2023-01-16 11:51:43.251245

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd4c7d6984fe0'
down_revision = '731f4e479e08'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dish_in_submenu', sa.Column('submenus', postgresql.UUID(), nullable=True))
    op.drop_constraint('dish_in_submenu_submenu_fkey', 'dish_in_submenu', type_='foreignkey')
    op.create_foreign_key(None, 'dish_in_submenu', 'submenu', ['submenus'], ['id'])
    op.drop_column('dish_in_submenu', 'submenu')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dish_in_submenu', sa.Column('submenu', postgresql.UUID(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'dish_in_submenu', type_='foreignkey')
    op.create_foreign_key('dish_in_submenu_submenu_fkey', 'dish_in_submenu', 'submenu', ['submenu'], ['id'])
    op.drop_column('dish_in_submenu', 'submenus')
    # ### end Alembic commands ###