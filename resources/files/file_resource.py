from base64 import b64decode

from flask_restful import Resource, request
from flask_jwt_extended import jwt_required

from cloud_storage.file import File
from schemas.files.file_schema import FileSchema
from resources.utils import handle_request


class FileResource(Resource):
    @jwt_required()
    @handle_request()
    def get(self):
        file = File(name=request.args['name'])
        return {'url': file.signed_url}, 200

    @jwt_required()
    @handle_request()
    def post(self):
        schema = FileSchema(partial=('url',))
        data = schema.load(request.get_json())
        file = File().upload(
            data=b64decode(data['b64_data'])
        )
        return {'url': file.url}, 201

    @jwt_required()
    @handle_request()
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
    @handle_request()
    def delete(self):
        schema = FileSchema(partial=('b64_data',))
        data = schema.load(request.get_json())
        File(url=data['url']).delete()
        return {'message': 'File deleted.'}, 200
