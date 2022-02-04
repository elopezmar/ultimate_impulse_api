from flask_restful import Resource

from models.irs.ir_list import IRList
from models.reviews.review_list import ReviewList
from schemas.irs.ir_schema import IRSchema
from schemas.reviews.review_schema import ReviewSchema
from resources.utils import handle_request


class HomeResource(Resource):
    @handle_request()
    def get(self):
        ir_schema = IRSchema(many=True)
        review_schema = ReviewSchema(many=True)
        irs = IRList().get(
            order_by=[('published_at', 'desc')],
            limit=5
        )
        #TODO: Necesita incide en firestore
        news = ReviewList().get(
            filters=[('tags', 'array_contains', 'NEWS')],
            order_by=[('published_at', 'desc')],
            limit=5
        )
        music_production = ReviewList().get(
            filters=[('tags', 'array_contains', 'MUSIC PRODUCTION')],
            order_by=[('published_at', 'desc')],
            limit=5
        )
        reviews = ReviewList().get(
            filters=[('tags', 'array_contains', 'REVIEW')],
            order_by=[('published_at', 'desc')],
            limit=5
        )
        return {
            # TODO: Enviar fondo de la sección
            'home': {
                'irs': ir_schema.dump(irs.to_list()),
                'news': review_schema.dump(news.to_list()),
                'music_production': review_schema.dump(music_production.to_list()),
                'reviews': review_schema.dump(reviews.to_list())
            }
        }, 200