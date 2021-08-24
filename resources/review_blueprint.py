from flask import Blueprint
from flask_restful import Api

from resources.reviews.review_resource import ReviewResource
from resources.reviews.review_list_resource import ReviewListResource
from resources.reviews.review_comment_resource import ReviewCommentResource
from resources.reviews.review_comment_list_resource import ReviewCommentListResource

review_blueprint = Blueprint('review', __name__)
api = Api(review_blueprint)

api.add_resource(ReviewResource, '/review')
api.add_resource(ReviewListResource, '/reviews')
api.add_resource(ReviewCommentResource, '/review/<string:review_id>/comment')
api.add_resource(ReviewCommentListResource, '/review/<string:review_id>/comments')
