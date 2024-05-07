from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
import datetime

db = SQLAlchemy()
manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')
    url = app.config['SQLALCHEMY_DATABASE_URI']
    # url = "postgresql://postgres:root@db:5432/ArdAppDB"
    engine = create_engine(url)
    if not database_exists(url):
        create_database(url)

    db.init_app(app)
    manager.init_app(app)

    from app.routes import main
    app.register_blueprint(main)
    

    with app.app_context():
        db.create_all()

    return app
