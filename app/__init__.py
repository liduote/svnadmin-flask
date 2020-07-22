import logging

from flask import Flask
from flask_cors import CORS
from flasgger import Flasgger

from config import Config
from app.extensions import db, jwt_manager


def create_app():
    app = Flask(__name__)
    app.logger.setLevel(logging.DEBUG)
    app.config.from_object(Config)
    db.init_app(app)

    jwt_manager.init_app(app)
    CORS(app, resources=r'/*')
    Flasgger(app)

    from .web import main as main_bludprint
    app.register_blueprint(main_bludprint)

    return app
