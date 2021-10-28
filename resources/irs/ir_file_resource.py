from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.irs.ir import IR
from models.irs.ir_file import IRFile
from schemas.irs.ir_file_schema import IRFileSchema
from resources.utils import get_requestor, handle_errors


class IRFileResource(Resource):
    @jwt_required()
    @handle_errors()
    def post(self, ir_id: str):
        requestor = get_requestor()
        schema = IRFileSchema(partial=('id',))
        
        file = IRFile(
            ir=IR(ir_id).get(requestor)
        ).from_dict(
            data=schema.load(request.get_json())
        )

        file.set(requestor)
        return schema.dump(file.to_dict()), 201

    @jwt_required(optional=True)
    @handle_errors()
    def get(self, ir_id: str):
        requestor = get_requestor()
        schema = IRFileSchema()

        file = IRFile(
            ir=IR(ir_id).get(requestor), 
            id=request.args['id']
        ).get(requestor)
        
        return schema.dump(file.to_dict()), 200

    @jwt_required()
    @handle_errors()
    def put(self, ir_id: str):
        requestor = get_requestor()
        schema = IRFileSchema(partial=('title', 'file_url'))
        
        file = IRFile(
            ir=IR(ir_id).get(requestor)
        ).from_dict(
            data=schema.load(request.get_json())
        )
        
        file.update(requestor)
        return {'message': 'File updated.'}, 200

    @jwt_required()
    @handle_errors()
    def delete(self, ir_id: str):
        requestor = get_requestor()
        schema = IRFileSchema(partial=('title', 'file_url'), only=('id',))
        
        file = IRFile(
            ir=IR(ir_id).get(requestor)
        ).from_dict(
            data=schema.load(request.get_json())
        )
        
        file.delete(requestor)
        return {'message': 'File deleted.'}, 200
