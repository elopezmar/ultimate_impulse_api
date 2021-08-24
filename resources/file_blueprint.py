from flask import Blueprint
from flask_restful import Api

from resources.files.file_resource import FileResource

file_blueprint = Blueprint('file', __name__)
api = Api(file_blueprint)

api.add_resource(FileResource, '/file')
