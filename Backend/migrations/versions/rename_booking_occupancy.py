"""Rename occupancies_id to occupancy_id

Revision ID: rename_booking_occupancy
Revises: cd9586a14834
"""

from alembic import op


revision = "rename_booking_occupancy"
down_revision = "cd9586a14834"
branch_labels = None
depends_on = None


def upgrade():

    op.alter_column(
        "bookings",
        "occupancies_id",
        new_column_name="occupancy_id"
    )


def downgrade():

    op.alter_column(
        "bookings",
        "occupancy_id",
        new_column_name="occupancies_id"
    )