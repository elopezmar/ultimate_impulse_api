from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.irs.ir import IR
from schemas.irs.ir_schema import IRSchema
from resources.utils import handle_request, get_bool_arg


class IRResource(Resource):
    @jwt_required()
    @handle_request()
    def post(self):
        schema = IRSchema(partial=('id', 'samples.id', 'files.id'))
        data = schema.load(request.get_json())
        ir = IR().from_dict(data)
        ir.set()
        return schema.dump(ir.to_dict()), 201

    @jwt_required(optional=True)
    @handle_request()
    def get(self):
        schema = IRSchema()
        ir = IR(id=request.args['id']).get(
            samples=get_bool_arg('samples'),
            files=get_bool_arg('files'),
            reviews=get_bool_arg('reviews')
        )
        return schema.dump(ir.to_dict()), 200

    @jwt_required()
    @handle_request()
    def put(self):
        schema = IRSchema(
            partial=(
                'title', 
                'samples.title',
                'samples.file_url',
                'files.title',
                'files.file_url'
            )
        )
        data = schema.load(request.get_json())
        ir = IR(id=data['id']).get()
        ir.from_dict(data)
        ir.update()
        return {'message': 'IR updated.'}, 200

    @jwt_required()
    @handle_request()
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
        ir = IR(id=data['id']).get()
        ir.delete()
        return {'message': 'IR deleted.'}, 200
