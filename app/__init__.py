from flask import Flask
from flask_cors import CORS
from .db import db, migrate
from .models.task import Task
from .models.goal import Goal
from .routes.task_routes import bp as tasks_bp
from .routes.goal_routes import bp as goals_bp
import os

def create_app(config=None):
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['CORS_HEADERS'] = 'Content-Type'

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(tasks_bp)
    app.register_blueprint(goals_bp)

    return app
