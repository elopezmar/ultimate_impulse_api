from flask_restful import Resource

from models.reviews.review_list import ReviewList
from models.exceptions import BusinessError
from schemas.reviews.review_list_schema import ReviewListSchema

class ReviewListResource(Resource):
    def get(self):
        try:
            schema = ReviewListSchema()
            reviews = ReviewList().get()
            return schema.dump(reviews.to_dict()), 200
        except BusinessError as err:
            return err.message
