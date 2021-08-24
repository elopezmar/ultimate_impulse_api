from flask_restful import Resource

from models.reviews.review import Review
from models.reviews.review_comment_list import ReviewCommentList
from models.exceptions import BusinessError
from schemas.reviews.review_comment_list_schema import ReviewCommentListSchema

class ReviewCommentListResource(Resource):
    def get(self, review_id: str):
        try:
            schema = ReviewCommentListSchema()
            comments = ReviewCommentList(review=Review(id=review_id)).get()
            return schema.dump(comments.to_dict()), 200
        except BusinessError as err:
            return err.message
