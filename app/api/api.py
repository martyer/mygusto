import configparser

from flask import Blueprint
from flask_restplus import Api
from app.api.v1.test import ns as test_ns

config = configparser.ConfigParser()
config.read('/mygusto/app/config.ini')

blueprint = Blueprint('mygusto', __name__, url_prefix='')
api = Api(
    blueprint,
    version=config['FLASK']['VERSION'],
    title=config['FLASK']['TITLE'],
    description=config['FLASK']['DESCRIPTION']
)

api.add_namespace(test_ns)
