from flask_jwt_extended import jwt_required
from flask_restful import Resource, request
from marshmallow import ValidationError

from models.exceptions import BusinessError
from models.irs.ir import IR
from models.irs.ir_sample import IRSample
from schemas.irs.ir_sample_schema import IRSampleSchema
from resources.utils import get_requestor


class IRSampleResource(Resource):
    @jwt_required()
    def post(self, ir_id: str):
        try:
            requestor = get_requestor()
            schema = IRSampleSchema(partial=('id',))
            
            sample = IRSample(
                ir=IR(ir_id).get(requestor)
            ).from_dict(
                data=schema.load(request.get_json())
            )

            sample.set(requestor)
            return schema.dump(sample.to_dict()), 201
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    def get(self, ir_id: str):
        try:
            schema = IRSampleSchema()
            sample = IRSample(ir=IR(ir_id), id=request.args['id']).get()
            return schema.dump(sample.to_dict()), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message

    @jwt_required()
    def put(self, ir_id: str):
        try:
            requestor = get_requestor()
            schema = IRSampleSchema(partial=('title', 'file_url'))
            
            sample = IRSample(
                ir=IR(ir_id).get(requestor)
            ).from_dict(
                data=schema.load(request.get_json())
            )
            
            sample.update(requestor)
            return {'message': 'Sample updated.'}, 200
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    @jwt_required()
    def delete(self, ir_id: str):
        try:
            requestor = get_requestor()
            schema = IRSampleSchema(partial=('title', 'file_url'), only=('id',))
            
            sample = IRSample(
                ir=IR(ir_id).get(requestor)
            ).from_dict(
                data=schema.load(request.get_json())
            )
            
            sample.delete(requestor)
            return {'message': 'Sample deleted.'}, 200
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message
