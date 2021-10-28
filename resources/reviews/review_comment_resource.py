from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.reviews.review import Review
from models.reviews.review_comment import ReviewComment
from schemas.reviews.review_comment_schema import ReviewCommentSchema
from resources.utils import get_requestor, handle_errors


class ReviewCommentResource(Resource):
    @jwt_required()
    @handle_errors()
    def post(self, review_id: str):
        schema = ReviewCommentSchema(partial=('id',))
        
        review = ReviewComment(
            review=Review(id=review_id).get()
        ).from_dict(
            data=schema.load(request.get_json())
        ).set(get_requestor())

        return schema.dump(review.to_dict()), 201

    @handle_errors()
    def get(self, review_id: str):
        schema = ReviewCommentSchema()

        review = ReviewComment(
            review=Review(id=review_id).get(),
            id=request.args['id']
        ).get()

        return schema.dump(review.to_dict()), 200

    @jwt_required()
    @handle_errors()
    def put(self, review_id: str):
        schema = ReviewCommentSchema(
            partial=('description',)
        )

        ReviewComment(
            review=Review(id=review_id).get()
        ).from_dict(
            data=schema.load(request.get_json())
        ).update(get_requestor())

        return {'message': 'Comment updated.'}, 200

    @jwt_required()
    @handle_errors()
    def delete(self, review_id: str):
        schema = ReviewCommentSchema(
            partial=('description',),
            only=('id',)
        )

        ReviewComment(
            review=Review(id=review_id).get()
        ).from_dict(
            data=schema.load(request.get_json())
        ).delete(get_requestor())

        return {'message': 'Comment deleted.'}, 200
