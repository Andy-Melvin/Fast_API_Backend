from sqlalchemy import create_engine, MetaData
from databases import Database

from databases import Database

DATABASE_URL = "sqlite:///./app/db.sqlite3"  # Path to your SQLite database
database = Database(DATABASE_URL)

metadata = MetaData()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})