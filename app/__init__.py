from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_cors import CORS

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from app.businesses.views import businesses_blueprint
    app.register_blueprint(businesses_blueprint)

    from app.reviews.views import reviews_blueprint
    app.register_blueprint(reviews_blueprint)

    from app.users.views import users_blueprint
    app.register_blueprint(users_blueprint)

    return app
