from flask_restful import Resource

from models.irs.ir import IR
from models.irs.ir_review_list import IRReviewList
from schemas.irs.ir_review_list_schema import IRReviewListSchema
from resources.utils import handle_request


class IRReviewListResource(Resource):
    @handle_request()
    def get(self, ir_id: str):
        schema = IRReviewListSchema()
        reviews = IRReviewList(IR(ir_id)).get()
        return schema.dump(reviews.to_dict('reviews')), 200
            