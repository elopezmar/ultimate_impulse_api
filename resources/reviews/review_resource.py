from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.reviews.review import Review
from schemas.reviews.review_schema import ReviewSchema
from resources.utils import handle_request, get_bool_arg


class ReviewResource(Resource):
    @jwt_required()
    @handle_request()
    def post(self):
        schema = ReviewSchema(partial=('id',))
        data = schema.load(request.get_json())
        review = Review().from_dict(data)
        review.set()
        return schema.dump(review.to_dict()), 201

    @handle_request()
    def get(self):
        schema = ReviewSchema()
        review = Review(id=request.args['id']).get(
            content=get_bool_arg('content'),
            comments=get_bool_arg('comments')
        )
        return schema.dump(review.to_dict()), 200

    @jwt_required()
    @handle_request()
    def put(self):
        schema = ReviewSchema(
            partial=(
                'title',
                'description',
                'pic_url'
            )
        )
        data = schema.load(request.get_json())
        review = Review(id=data['id']).get()
        review.from_dict(data)
        review.update()
        return {'message': 'Review updated.'}, 200

    @jwt_required()
    @handle_request()
    def delete(self):
        schema = ReviewSchema(
            partial=(
                'title',
                'description',
                'pic_url'
            ),
            only=('id',)
        )
        data = schema.load(request.get_json())
        review = Review(id=data['id']).get()
        review.delete()
        return {'message': 'Review deleted.'}, 200
