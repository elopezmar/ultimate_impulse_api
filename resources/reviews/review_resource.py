from flask_jwt_extended import jwt_required
from flask_restful import Resource, request
from marshmallow import ValidationError, schema

from models.reviews.review import Review
from models.exceptions import BusinessError
from schemas.reviews.review_schema import ReviewSchema
from resources.utils import get_requestor

class ReviewResource(Resource):
    @jwt_required()
    def post(self):
        try:
            schema = ReviewSchema(partial=('id',))
            data = schema.load(request.get_json())
            review = Review().from_dict(data)
            review.set(get_requestor())
            return schema.dump(review.to_dict()), 201
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    def get(self):
        try:
            schema = ReviewSchema()
            review = Review(id=request.args['id']).get(
                content=request.args.get('content', '').lower() == 'true',
                comments=request.args.get('comments', '').lower() == 'true'
            )
            return schema.dump(review.to_dict()), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message

    @jwt_required()
    def put(self):
        try:
            schema = ReviewSchema(
                partial=(
                    'title',
                    'description',
                    'pic_url'
                )
            )
            data = schema.load(request.get_json())
            review = Review().from_dict(data)
            review.update(get_requestor())
            return {'message': 'Review updated.'}, 200
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    @jwt_required()
    def delete(self):
        try:
            schema = ReviewSchema(
                partial=(
                    'title',
                    'description',
                    'pic_url'
                ),
                only=('id',)
            )
            data = schema.load(request.get_json())
            review = Review().from_dict(data)
            review.delete(get_requestor())
            return {'message': 'Review deleted.'}, 200
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message
