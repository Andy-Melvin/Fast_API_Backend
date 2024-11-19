import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.models import metadata
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./app/db.sqlite3"
engine = create_engine(DATABASE_URL)

# Create tables
metadata.create_all(engine)
print("Tables created successfully.")