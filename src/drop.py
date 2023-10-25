from sqlalchemy import create_engine
from database_info import database
from models import Base  # Import the Base object from where you've defined it

# Create engine
engine = create_engine(database)

# Drop all tables associated with the Base metadata
Base.metadata.drop_all(engine)