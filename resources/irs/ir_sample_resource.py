from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.irs.ir import IR
from models.irs.ir_sample import IRSample
from schemas.irs.ir_sample_schema import IRSampleSchema
from resources.utils import handle_request


class IRSampleResource(Resource):
    @jwt_required()
    @handle_request()
    def post(self, ir_id: str):
        schema = IRSampleSchema(partial=('id',))
        
        sample = IRSample(
            ir=IR(ir_id).get()
        ).from_dict(
            data=schema.load(request.get_json())
        )

        sample.set()
        return schema.dump(sample.to_dict()), 201

    @handle_request()
    def get(self, ir_id: str):
        schema = IRSampleSchema()
        sample = IRSample(ir=IR(ir_id), id=request.args['id']).get()
        return schema.dump(sample.to_dict()), 200

    @jwt_required()
    @handle_request()
    def put(self, ir_id: str):
        schema = IRSampleSchema(partial=('title', 'file_url'))
        
        sample = IRSample(
            ir=IR(ir_id).get()
        ).from_dict(
            data=schema.load(request.get_json())
        )
        
        sample.update()
        return {'message': 'Sample updated.'}, 200

    @jwt_required()
    @handle_request()
    def delete(self, ir_id: str):
        schema = IRSampleSchema(partial=('title', 'file_url'), only=('id',))
        
        sample = IRSample(
            ir=IR(ir_id).get()
        ).from_dict(
            data=schema.load(request.get_json())
        )
        
        sample.delete()
        return {'message': 'Sample deleted.'}, 200
