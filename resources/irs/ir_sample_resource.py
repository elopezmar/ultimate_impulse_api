from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.irs.ir import IR
from models.irs.ir_sample import IRSample
from schemas.irs.ir_sample_schema import IRSampleSchema
from resources.utils import handle_request


class IRSampleResource(Resource):
    def sample(self, ir_id: str, sample_id: str=None) -> IRSample:
        ir = IR(ir_id).get()
        sample = IRSample(ir, sample_id)
        return sample

    @jwt_required()
    @handle_request()
    def post(self, ir_id: str):
        schema = IRSampleSchema(partial=('id',))
        data = schema.load(request.get_json())
        sample = self.sample(ir_id).from_dict(data)
        sample.set()
        return schema.dump(sample.to_dict()), 201

    @handle_request()
    def get(self, ir_id: str):
        schema = IRSampleSchema()
        sample_id = request.args['id']
        sample = self.sample(ir_id, sample_id).get()
        return schema.dump(sample.to_dict()), 200

    @jwt_required()
    @handle_request()
    def put(self, ir_id: str):
        schema = IRSampleSchema(partial=('title', 'file_url'))
        data = schema.load(request.get_json())
        sample_id = data['id']
        sample = self.sample(ir_id, sample_id).get()
        sample.from_dict(data)
        sample.update()
        return {'message': 'Sample updated.'}, 200

    @jwt_required()
    @handle_request()
    def delete(self, ir_id: str):
        schema = IRSampleSchema(partial=('title', 'file_url'), only=('id',))
        data = schema.load(request.get_json())
        sample_id = data['id']
        sample = self.sample(ir_id, sample_id).get()
        sample.delete()
        return {'message': 'Sample deleted.'}, 200
