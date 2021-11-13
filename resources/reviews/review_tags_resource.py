from flask_restful import Resource


class ReviewTagListResource(Resource):
    def get(self):
        return {
            'tags': [
                'news',
                'music_production',
                'review'
            ]
        }, 200
