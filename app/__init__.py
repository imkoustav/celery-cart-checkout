from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()  
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL"),
        CELERY_RESULT_BACKEND=os.getenv("CELERY_RESULT_BACKEND")
    )
    print("Database URI:", app.config["SQLALCHEMY_DATABASE_URI"])

    from . import models
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import bp
    app.register_blueprint(bp)

    return app
