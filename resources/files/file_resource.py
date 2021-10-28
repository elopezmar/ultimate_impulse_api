from base64 import b64decode

from flask_restful import Resource, request
from flask_jwt_extended import jwt_required

from cloud_storage.file import File
from schemas.files.file_schema import FileSchema
from resources.utils import handle_errors


class FileResource(Resource):
    @jwt_required()
    @handle_errors()
    def get(self):
        schema = FileSchema(partial=('b64_data',))
        data = schema.load(request.get_json())
        file = File(url=data['url'])
        return {'url': file.signed_url}, 200

    @jwt_required()
    @handle_errors()
    def post(self):
        schema = FileSchema(partial=('url',))
        data = schema.load(request.get_json())
        file = File().upload(
            data=b64decode(data['b64_data'])
        )
        return {'url': file.url}, 201

    @jwt_required()
    @handle_errors()
    def put(self):
        schema = FileSchema()
        data = schema.load(request.get_json())
        File(
            url=data['url']
        ).upload(
            data=b64decode(data['b64_data'])
        )
        return {'message': 'File updated.'}, 200

    @jwt_required()
    @handle_errors()
    def delete(self):
        schema = FileSchema(partial=('b64_data',))
        data = schema.load(request.get_json())
        File(url=data['url']).delete()
        return {'message': 'File deleted.'}, 200
