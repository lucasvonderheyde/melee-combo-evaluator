from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

combo_db = SQLAlchemy()
migrate = Migrate()