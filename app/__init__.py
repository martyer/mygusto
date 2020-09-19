import configparser

from flask import Flask
from flask_migrate import Migrate

from app.api.api import blueprint as api_blueprint
from app.database import db

config = configparser.ConfigParser()
config.read('/mygusto/app/config.ini')


def create_app():
    app = Flask(__name__)
    app.config.from_object(config['FLASK'])
    db_url = (f'postgresql://{config["POSTGRES"]["USER"]}:{config["POSTGRES"]["PASSWORD"]}'
              f'@{config["POSTGRES"]["HOST"]}/{config["POSTGRES"]["DB"]}')
    app.config.update(SQLALCHEMY_DATABASE_URI=db_url)
    app.url_map.strict_slashes = False  # Routes don't need to end with a trailing slash

    init_extensions(app)

    app.register_blueprint(api_blueprint)

    return app


def init_extensions(app):
    db.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, db, directory='/mygusto/app/database/migrations')
