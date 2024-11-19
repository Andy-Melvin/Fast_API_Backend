from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Text, Boolean
from .database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column("role", String, default="gardener"),  # admin or gardener
    Column("phone_number", String, unique=True, nullable=False),
)

garden_plots = Table(
    "garden_plots",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("plot_number", String, nullable=False),
    Column("size", String, nullable=False),
    Column("location", String, nullable=False),
    Column("status", String, default="available"),  # available, pending, occupied
    Column("gardener_id", Integer, ForeignKey("users.id"), nullable=True),
)

events = Table(
    "events",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("description", Text, nullable=False),
    Column("date", Date, nullable=False),
    Column("volunteers_needed", Integer, nullable=False),
    Column("assigned_volunteers", Text, default=""),  # Comma-separated user IDs
)

crop_records = Table(
    "crop_records",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("gardener_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("plot_id", Integer, ForeignKey("garden_plots.id"), nullable=False),
    Column("crop_type", String, nullable=False),
    Column("planting_date", Date, nullable=False),
    Column("expected_harvest_date", Date, nullable=False),
    Column("notes", Text, nullable=True),
)