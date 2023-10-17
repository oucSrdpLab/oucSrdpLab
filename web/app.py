import sys
sys.path.append(r'.')
from apps import app
from apps import config
from web.apps.exts import db

import os



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run('0.0.0.0', 8000)
