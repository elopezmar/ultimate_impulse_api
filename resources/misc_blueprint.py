from flask import Blueprint
from flask.app import Flask
from flask_restful import Api

from resources.misc.home_resource import HomeResource

misc_blueprint = Blueprint('misc', __name__)
api = Api(misc_blueprint, errors=Flask.errorhandler)

api.add_resource(HomeResource, '/home')
