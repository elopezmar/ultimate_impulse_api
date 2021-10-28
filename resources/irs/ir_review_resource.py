from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.irs.ir import IR
from models.irs.ir_review import IRReview
from schemas.irs.ir_review_schema import IRReviewSchema
from resources.utils import get_requestor, handle_errors


class IRReviewResource(Resource):
    @jwt_required()
    @handle_errors()
    def post(self, ir_id: str):
        schema = IRReviewSchema(partial=('id',))
        
        review = IRReview(IR(ir_id)).from_dict(
            data=schema.load(request.get_json())
        )

        review.set(get_requestor())
        return schema.dump(review.to_dict()), 201

    @handle_errors()
    def get(self, ir_id: str):
        schema = IRReviewSchema()
        review = IRReview(IR(ir_id), id=request.args['id']).get()
        return schema.dump(review.to_dict()), 200

    @jwt_required()
    @handle_errors()
    def put(self, ir_id: str):
        schema = IRReviewSchema(partial=('title', 'rating'))
        
        review = IRReview(IR(ir_id)).from_dict(
            data=schema.load(request.get_json())
        )
        
        review.update(get_requestor())
        return {'message': 'Review updated.'}, 200

    @jwt_required()
    @handle_errors()
    def delete(self, ir_id: str):
        schema = IRReviewSchema(partial=('title', 'rating'), only=('id',))
        
        review = IRReview(IR(ir_id)).from_dict(
            data=schema.load(request.get_json())
        )
        
        review.delete(get_requestor())
        return {'message': 'Review deleted.'}, 200
