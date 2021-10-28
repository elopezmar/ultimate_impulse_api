from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.irs.ir import IR
from models.irs.ir_sample import IRSample
from schemas.irs.ir_sample_schema import IRSampleSchema
from resources.utils import get_requestor, handle_errors


class IRSampleResource(Resource):
    @jwt_required()
    @handle_errors()
    def post(self, ir_id: str):
        requestor = get_requestor()
        schema = IRSampleSchema(partial=('id',))
        
        sample = IRSample(
            ir=IR(ir_id).get(requestor)
        ).from_dict(
            data=schema.load(request.get_json())
        )

        sample.set(requestor)
        return schema.dump(sample.to_dict()), 201

    @handle_errors()
    def get(self, ir_id: str):
        schema = IRSampleSchema()
        sample = IRSample(ir=IR(ir_id), id=request.args['id']).get()
        return schema.dump(sample.to_dict()), 200

    @jwt_required()
    @handle_errors()
    def put(self, ir_id: str):
        requestor = get_requestor()
        schema = IRSampleSchema(partial=('title', 'file_url'))
        
        sample = IRSample(
            ir=IR(ir_id).get(requestor)
        ).from_dict(
            data=schema.load(request.get_json())
        )
        
        sample.update(requestor)
        return {'message': 'Sample updated.'}, 200

    @jwt_required()
    @handle_errors()
    def delete(self, ir_id: str):
        requestor = get_requestor()
        schema = IRSampleSchema(partial=('title', 'file_url'), only=('id',))
        
        sample = IRSample(
            ir=IR(ir_id).get(requestor)
        ).from_dict(
            data=schema.load(request.get_json())
        )
        
        sample.delete(requestor)
        return {'message': 'Sample deleted.'}, 200
