from flask_restful import Resource

from models.exceptions import BusinessError
from models.irs.ir import IR
from models.irs.ir_review_list import IRReviewList
from schemas.irs.ir_review_list_schema import IRReviewListSchema


class IRReviewListResource(Resource):
    def get(self, ir_id: str):
        try:
            schema = IRReviewListSchema()
            reviews = IRReviewList(IR(ir_id)).get()
            return schema.dump(reviews.to_dict()), 200
        except BusinessError as err:
            return err.message
            