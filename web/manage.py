from flask_migrate import Migrate
from apps import app, db

migrate = Migrate(app, db)
