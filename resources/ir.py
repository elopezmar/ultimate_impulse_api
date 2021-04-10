import uuid
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from schemas.ir import IRSchema, IRReviewSchema, BusinessError


class IRReview(Resource):
    ir_review_schema = IRReviewSchema()

    @jwt_required()
    def post(self, ir_id):
        try:
            json_data = request.get_json()
            review = self.ir_review_schema.load(json_data)
            return self.ir_review_schema.create(ir_id, review), 201
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    def get(self, ir_id):
        try:
            args = request.args
            review_id = args['id']
            return self.ir_review_schema.read(ir_id, review_id), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message


class IR(Resource):
    ir_schema = IRSchema()

    @jwt_required()
    def post(self):
        try:
            json_data = request.get_json()
            ir = self.ir_schema.load(json_data)
            return self.ir_schema.create(ir), 201
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    def get(self):
        try:
            args = request.args
            ir_id = args['id']
            samples = args.get('samples', '').lower() == 'true'
            files = args.get('files', '').lower() == 'true'
            reviews = args.get('reviews', '').lower() == 'true'
            return self.ir_schema.read(ir_id, samples, files, reviews), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message
