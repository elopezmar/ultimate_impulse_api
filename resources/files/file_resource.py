from base64 import b64decode

from flask_restful import Resource, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from cloud_storage.file import File
from schemas.files.file_schema import FileSchema


class FileResource(Resource):
    @jwt_required()
    def get(self):
        try:
            schema = FileSchema(partial=('b64_data',))
            data = schema.load(request.get_json())
            file = File(url=data['url'])
            return {'url': file.signed_url}, 200
        except ValidationError as err:
            return err.messages

    @jwt_required()
    def post(self):
        try:
            schema = FileSchema(partial=('url',))
            data = schema.load(request.get_json())
            file = File().upload(
                data=b64decode(data['b64_data'])
            )
            return {'url': file.url}, 201
        except ValidationError as err:
            return err.messages

    @jwt_required()
    def put(self):
        try:
            schema = FileSchema()
            data = schema.load(request.get_json())
            File(
                url=data['url']
            ).upload(
                data=b64decode(data['b64_data'])
            )
            return {'message': 'File updated.'}, 200
        except ValidationError as err:
            return err.messages

    @jwt_required()
    def delete(self):
        try:
            schema = FileSchema(partial=('b64_data',))
            data = schema.load(request.get_json())
            File(url=data['url']).delete()
            return {'message': 'File deleted.'}, 200
        except ValidationError as err:
            return err.messages
