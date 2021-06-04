from functools import partial
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from schemas.file import FileSchema


class File(Resource):
    file_schema = FileSchema()

    @jwt_required()
    def get(self):
        try:
            json_data = request.get_json()
            file = self.file_schema.load(json_data, partial=('b64_data',))
            return self.file_schema.read(file), 200
        except ValidationError as err:
            return err.messages

    @jwt_required()
    def post(self):
        try:
            json_data = request.get_json()
            file = self.file_schema.load(json_data, partial=('url',))
            return self.file_schema.create(file), 201
        except ValidationError as err:
            return err.messages

    @jwt_required()
    def put(self):
        try:
            json_data = request.get_json()
            file = self.file_schema.load(json_data)
            self.file_schema.update(file)
            return {'message': 'File updated.'}, 200
        except ValidationError as err:
            return err.messages

    @jwt_required()
    def delete(self):
        try:
            json_data = request.get_json()
            file = self.file_schema.load(json_data, partial=('b64_data',))
            self.file_schema.delete(file)
            return {'message': 'File deleted.'}, 200
        except ValidationError as err:
            return err.messages
