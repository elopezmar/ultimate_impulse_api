from flask_jwt_extended import jwt_required
from flask_restful import Resource, request
from marshmallow import ValidationError

from models.exceptions import BusinessError
from models.irs.ir import IR
from models.irs.ir_review import IRReview
from schemas.irs.ir_review_schema import IRReviewSchema
from resources.utils import get_requestor


class IRReviewResource(Resource):
    @jwt_required()
    def post(self, ir_id: str):
        try:
            schema = IRReviewSchema(partial=('id',))
            
            review = IRReview(IR(ir_id)).from_dict(
                data=schema.load(request.get_json())
            )

            review.set(get_requestor())
            return schema.dump(review.to_dict()), 201
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    def get(self, ir_id: str):
        try:
            schema = IRReviewSchema()
            review = IRReview(IR(ir_id), id=request.args['id']).get()
            return schema.dump(review.to_dict()), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message

    @jwt_required()
    def put(self, ir_id: str):
        try:
            schema = IRReviewSchema(partial=('title', 'rating'))
            
            review = IRReview(IR(ir_id)).from_dict(
                data=schema.load(request.get_json())
            )
            
            review.update(get_requestor())
            return {'message': 'Review updated.'}, 200
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    @jwt_required()
    def delete(self, ir_id: str):
        try:
            schema = IRReviewSchema(partial=('title', 'rating'), only=('id',))
            
            review = IRReview(IR(ir_id)).from_dict(
                data=schema.load(request.get_json())
            )
            
            review.delete(get_requestor())
            return {'message': 'Review deleted.'}, 200
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message
