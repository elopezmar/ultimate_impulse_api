from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.reviews.review import Review
from schemas.reviews.review_schema import ReviewSchema
from resources.utils import get_requestor, handle_errors


class ReviewResource(Resource):
    @jwt_required()
    @handle_errors()
    def post(self):
        schema = ReviewSchema(partial=('id',))
        data = schema.load(request.get_json())
        review = Review().from_dict(data)
        review.set(get_requestor())
        return schema.dump(review.to_dict()), 201

    @handle_errors()
    def get(self):
        schema = ReviewSchema()
        review = Review(id=request.args['id']).get(
            content=request.args.get('content', '').lower() == 'true',
            comments=request.args.get('comments', '').lower() == 'true'
        )
        return schema.dump(review.to_dict()), 200

    @jwt_required()
    @handle_errors()
    def put(self):
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

    @jwt_required()
    @handle_errors()
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
        review = Review().from_dict(data)
        review.delete(get_requestor())
        return {'message': 'Review deleted.'}, 200
