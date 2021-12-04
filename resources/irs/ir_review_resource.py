from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.irs.ir import IR
from models.irs.ir_review import IRReview
from schemas.irs.ir_review_schema import IRReviewSchema
from resources.utils import handle_request


class IRReviewResource(Resource):
    @jwt_required()
    @handle_request()
    def post(self, ir_id: str):
        schema = IRReviewSchema(partial=('id',))
        
        review = IRReview(IR(ir_id)).from_dict(
            data=schema.load(request.get_json())
        )

        review.set()
        return schema.dump(review.to_dict()), 201

    @handle_request()
    def get(self, ir_id: str):
        schema = IRReviewSchema()
        review = IRReview(IR(ir_id), id=request.args['id']).get()
        return schema.dump(review.to_dict()), 200

    @jwt_required()
    @handle_request()
    def put(self, ir_id: str):
        schema = IRReviewSchema(partial=('title', 'rating'))
        
        review = IRReview(IR(ir_id)).from_dict(
            data=schema.load(request.get_json())
        )
        
        review.update()
        return {'message': 'Review updated.'}, 200

    @jwt_required()
    @handle_request()
    def delete(self, ir_id: str):
        schema = IRReviewSchema(partial=('title', 'rating'), only=('id',))
        
        review = IRReview(IR(ir_id)).from_dict(
            data=schema.load(request.get_json())
        )
        
        review.delete()
        return {'message': 'Review deleted.'}, 200
