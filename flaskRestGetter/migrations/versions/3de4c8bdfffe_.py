"""empty message

Revision ID: 3de4c8bdfffe
Revises: 
Create Date: 2024-10-22 15:21:45.005327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3de4c8bdfffe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('maquina',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('dadosDict', sa.JSON(), nullable=True),
    sa.Column('maxDict', sa.JSON(), nullable=True),
    sa.Column('tipoMensagemMax', sa.JSON(), nullable=True),
    sa.Column('minDict', sa.JSON(), nullable=True),
    sa.Column('tipoMensagemMin', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('memento_notificacao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idMaquina', sa.Integer(), nullable=False),
    sa.Column('dados', sa.JSON(), nullable=True),
    sa.Column('data', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('operador',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('operador_maquina',
    sa.Column('operador_id', sa.Integer(), nullable=False),
    sa.Column('maquina_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['maquina_id'], ['maquina.id'], ),
    sa.ForeignKeyConstraint(['operador_id'], ['operador.id'], ),
    sa.PrimaryKeyConstraint('operador_id', 'maquina_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('operador_maquina')
    op.drop_table('operador')
    op.drop_table('memento_notificacao')
    op.drop_table('maquina')
    # ### end Alembic commands ###
