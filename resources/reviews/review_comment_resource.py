from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.reviews.review import Review
from models.reviews.review_comment import ReviewComment
from schemas.reviews.review_comment_schema import ReviewCommentSchema
from resources.utils import handle_request


class ReviewCommentResource(Resource):
    def comment(self, review_id: str, comment_id: str=None) -> ReviewComment:
        review = Review(review_id).get()
        comment = ReviewComment(review, comment_id)
        return comment

    @jwt_required()
    @handle_request()
    def post(self, review_id: str):
        schema = ReviewCommentSchema(partial=('id',))
        data = schema.load(request.get_json())
        comment = self.comment(review_id).from_dict(data)
        comment.set()
        return schema.dump(comment.to_dict()), 201

    @handle_request()
    def get(self, review_id: str):
        schema = ReviewCommentSchema()
        comment_id = request.args['id']
        comment = self.comment(review_id, comment_id).get()
        return schema.dump(comment.to_dict()), 200

    @jwt_required()
    @handle_request()
    def put(self, review_id: str):
        schema = ReviewCommentSchema(
            partial=('description',)
        )
        data = schema.load(request.get_json())
        comment_id = data['id']
        comment = self.comment(review_id, comment_id).get()
        comment.from_dict(data)
        comment.update()
        return {'message': 'Comment updated.'}, 200

    @jwt_required()
    @handle_request()
    def delete(self, review_id: str):
        schema = ReviewCommentSchema(
            partial=('description',),
            only=('id',)
        )
        data = schema.load(request.get_json())
        comment_id = data['id']
        comment = self.comment(review_id, comment_id).get()
        comment.delete()
        return {'message': 'Comment deleted.'}, 200
