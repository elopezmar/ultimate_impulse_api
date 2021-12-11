from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.irs.ir import IR
from models.irs.ir_review import IRReview
from schemas.irs.ir_review_schema import IRReviewSchema
from resources.utils import handle_request


class IRReviewResource(Resource):
    def review(self, ir_id: str, review_id: str=None) -> IRReview:
        ir = IR(ir_id).get()
        review = IRReview(ir, review_id)
        return review

    @jwt_required()
    @handle_request()
    def post(self, ir_id: str):
        schema = IRReviewSchema(partial=('id',))
        data = schema.load(request.get_json())
        review = self.review(ir_id).from_dict(data)
        review.set()
        return schema.dump(review.to_dict()), 201

    @handle_request()
    def get(self, ir_id: str):
        schema = IRReviewSchema()
        review_id = request.args['id']
        review = self.review(ir_id, review_id).get()
        return schema.dump(review.to_dict()), 200

    @jwt_required()
    @handle_request()
    def put(self, ir_id: str):
        schema = IRReviewSchema(partial=('title', 'rating'))
        data = schema.load(request.get_json())
        review_id = data['id']
        review = self.review(ir_id, review_id).get()
        review.from_dict(data)
        review.update()
        return {'message': 'Review updated.'}, 200

    @jwt_required()
    @handle_request()
    def delete(self, ir_id: str):
        schema = IRReviewSchema(partial=('title', 'rating'), only=('id',))
        data = schema.load(request.get_json())
        review_id = data['id']
        review = self.review(ir_id, review_id).get()
        review.delete()
        return {'message': 'Review deleted.'}, 200
