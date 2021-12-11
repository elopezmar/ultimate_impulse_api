from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.irs.ir import IR
from models.irs.ir_file import IRFile
from schemas.irs.ir_file_schema import IRFileSchema
from resources.utils import handle_request


class IRFileResource(Resource):
    def file(self, ir_id: str, file_id: str=None) -> IRFile:
        ir = IR(ir_id).get()
        file = IRFile(ir, file_id)
        return file

    @jwt_required()
    @handle_request()
    def post(self, ir_id: str):
        schema = IRFileSchema(partial=('id',))
        data = schema.load(request.get_json())
        file = self.file(ir_id).from_dict(data)
        file.set()
        return schema.dump(file.to_dict()), 201

    @jwt_required(optional=True)
    @handle_request()
    def get(self, ir_id: str):
        schema = IRFileSchema()
        file_id = request.args['id']
        file = self.file(ir_id, file_id).get()
        return schema.dump(file.to_dict()), 200

    @jwt_required()
    @handle_request()
    def put(self, ir_id: str):
        schema = IRFileSchema(partial=('title', 'file_url'))
        data = schema.load(request.get_json())
        file_id = data['id']
        file = self.file(ir_id, file_id).get()
        file.from_dict(data)
        file.update()
        return {'message': 'File updated.'}, 200

    @jwt_required()
    @handle_request()
    def delete(self, ir_id: str):
        schema = IRFileSchema(partial=('title', 'file_url'), only=('id',))
        data = schema.load(request.get_json())
        file_id = data['id']
        file = self.file(ir_id, file_id).get()
        file.delete()
        return {'message': 'File deleted.'}, 200
