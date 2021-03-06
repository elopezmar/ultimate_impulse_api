from flask_restful import Resource

from models.reviews.review import Review
from models.reviews.review_comment_list import ReviewCommentList
from schemas.reviews.review_comment_list_schema import ReviewCommentListSchema
from resources.utils import handle_request


class ReviewCommentListResource(Resource):
    @handle_request()
    def get(self, review_id: str):
        schema = ReviewCommentListSchema()
        comments = ReviewCommentList(review=Review(id=review_id)).get()
        return schema.dump(comments.to_dict('comments')), 200
