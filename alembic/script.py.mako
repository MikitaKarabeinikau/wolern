"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'xxxx'
down_revision: Union[str, Sequence[str], None] = '<previous_revision_id>'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add columns as nullable first
    op.add_column('words', sa.Column('correct_answers', sa.Integer(), nullable=True))
    op.add_column('words', sa.Column('wrong_answers', sa.Integer(), nullable=True))

    # Set default values for existing rows
    op.execute("UPDATE words SET correct_answers = 0 WHERE correct_answers IS NULL")
    op.execute("UPDATE words SET wrong_answers = 0 WHERE wrong_answers IS NULL")

    # Alter columns to set NOT NULL constraint
    op.alter_column('words', 'correct_answers', nullable=False)
    op.alter_column('words', 'wrong_answers', nullable=False)


def downgrade():
    op.drop_column('words', 'correct_answers')
    op.drop_column('words', 'wrong_answers')