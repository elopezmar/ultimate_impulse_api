from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.irs.ir import IR
from schemas.irs.ir_schema import IRSchema
from resources.utils import get_requestor, handle_errors


class IRResource(Resource):
    @jwt_required()
    @handle_errors()
    def post(self):
        schema = IRSchema(partial=('id', 'samples.id', 'files.id'))
        data = schema.load(request.get_json())
        ir = IR().from_dict(data)
        ir.set(get_requestor())
        return schema.dump(ir.to_dict()), 201

    @jwt_required(optional=True)
    @handle_errors()
    def get(self):
        schema = IRSchema()
        ir = IR(id=request.args['id']).get(
            requestor=get_requestor(),
            samples=request.args.get('samples', '').lower() == 'true',
            files=request.args.get('files', '').lower() == 'true',
            reviews=request.args.get('reviews', '').lower() == 'true'
        )
        return schema.dump(ir.to_dict()), 200

    @jwt_required()
    @handle_errors()
    def put(self):
        schema = IRSchema(
            partial=(
                'title', 
                'samples.title',
                'samples.file_url',
                'files.title',
                'files.file_url'
        ))
        data = schema.load(request.get_json())
        ir = IR().from_dict(data)
        ir.update(get_requestor())
        return {'message': 'IR updated.'}, 200

    @jwt_required()
    @handle_errors()
    def delete(self):
        schema = IRSchema(
            partial=(
                'title', 
                'samples.title',
                'samples.file_url',
                'files.title',
                'files.file_url'
            ),
            only=('id',)
        )
        data = schema.load(request.get_json())
        ir = IR().from_dict(data)
        ir.delete(get_requestor())
        return {'message': 'IR deleted.'}, 200
