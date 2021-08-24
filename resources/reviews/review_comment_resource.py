from flask_jwt_extended import jwt_required
from flask_restful import Resource, request
from marshmallow import ValidationError

from models.reviews.review import Review
from models.reviews.review_comment import ReviewComment
from models.exceptions import BusinessError
from schemas.reviews.review_comment_schema import ReviewCommentSchema
from resources.utils import get_requestor

class ReviewCommentResource(Resource):
    @jwt_required()
    def post(self, review_id: str):
        try:
            schema = ReviewCommentSchema(partial=('id',))
            
            review = ReviewComment(
                review=Review(id=review_id).get()
            ).from_dict(
                data=schema.load(request.get_json())
            ).set(get_requestor())

            return schema.dump(review.to_dict()), 201
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    def get(self, review_id: str):
        try:
            schema = ReviewCommentSchema()

            review = ReviewComment(
                review=Review(id=review_id).get(),
                id=request.args['id']
            ).get()

            return schema.dump(review.to_dict()), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message

    @jwt_required()
    def put(self, review_id: str):
        try:
            schema = ReviewCommentSchema(
                partial=('description',)
            )

            ReviewComment(
                review=Review(id=review_id).get()
            ).from_dict(
                data=schema.load(request.get_json())
            ).update(get_requestor())

            return {'message': 'Comment updated.'}, 200
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    @jwt_required()
    def delete(self, review_id: str):
        try:
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
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message
