from flask import Blueprint
from flask.app import Flask
from flask_restful import Api

from resources.files.file_resource import FileResource

file_blueprint = Blueprint('file', __name__)
api = Api(file_blueprint, errors=Flask.errorhandler)

api.add_resource(FileResource, '/file')
