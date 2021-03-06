from flask import Blueprint
from flask.app import Flask
from flask_restful import Api

from resources.reviews.review_resource import ReviewResource
from resources.reviews.review_list_resource import ReviewListResource
from resources.reviews.review_comment_resource import ReviewCommentResource
from resources.reviews.review_comment_list_resource import ReviewCommentListResource
from resources.reviews.review_tags_resource import ReviewTagListResource

review_blueprint = Blueprint('review', __name__)
api = Api(review_blueprint, errors=Flask.errorhandler)

api.add_resource(ReviewResource, '/review')
api.add_resource(ReviewListResource, '/reviews')
api.add_resource(ReviewCommentResource, '/review/<string:review_id>/comment')
api.add_resource(ReviewCommentListResource, '/review/<string:review_id>/comments')
api.add_resource(ReviewTagListResource, '/review/tags')
