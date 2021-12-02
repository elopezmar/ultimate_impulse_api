from flask_restful import Resource

from models.reviews.review_list import ReviewList
from schemas.reviews.review_list_schema import ReviewListSchema
from resources.utils import handle_request


class ReviewListResource(Resource):
    @handle_request()
    def get(self):
        schema = ReviewListSchema()
        reviews = ReviewList().get()
        return schema.dump(reviews.to_dict('reviews')), 200
