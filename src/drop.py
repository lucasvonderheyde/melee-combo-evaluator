from sqlalchemy import create_engine
from database_info import username, password
from models import Base  # Import the Base object from where you've defined it

# Create engine
engine = create_engine(f'postgresql://{username}:{password}@localhost/Melee_Combo_Database')

# Drop all tables associated with the Base metadata
Base.metadata.drop_all(engine)