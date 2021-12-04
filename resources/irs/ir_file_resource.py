from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.irs.ir import IR
from models.irs.ir_file import IRFile
from schemas.irs.ir_file_schema import IRFileSchema
from resources.utils import handle_request


class IRFileResource(Resource):
    @jwt_required()
    @handle_request()
    def post(self, ir_id: str):
        schema = IRFileSchema(partial=('id',))
        
        file = IRFile(
            ir=IR(ir_id).get()
        ).from_dict(
            data=schema.load(request.get_json())
        )

        file.set()
        return schema.dump(file.to_dict()), 201

    @jwt_required(optional=True)
    @handle_request()
    def get(self, ir_id: str):
        schema = IRFileSchema()

        file = IRFile(
            ir=IR(ir_id).get(), 
            id=request.args['id']
        ).get()
        
        return schema.dump(file.to_dict()), 200

    @jwt_required()
    @handle_request()
    def put(self, ir_id: str):
        schema = IRFileSchema(partial=('title', 'file_url'))
        
        file = IRFile(
            ir=IR(ir_id).get()
        ).from_dict(
            data=schema.load(request.get_json())
        )
        
        file.update()
        return {'message': 'File updated.'}, 200

    @jwt_required()
    @handle_request()
    def delete(self, ir_id: str):
        schema = IRFileSchema(partial=('title', 'file_url'), only=('id',))
        
        file = IRFile(
            ir=IR(ir_id).get()
        ).from_dict(
            data=schema.load(request.get_json())
        )
        
        file.delete()
        return {'message': 'File deleted.'}, 200
