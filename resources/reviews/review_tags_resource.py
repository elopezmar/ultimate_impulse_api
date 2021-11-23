from flask_restful import Resource


class ReviewTagListResource(Resource):
    def get(self):
        return {
            'tags': [
                'NEWS',
                'MUSIC PRODUCTION',
                'REVIEW'
            ]
        }, 200
