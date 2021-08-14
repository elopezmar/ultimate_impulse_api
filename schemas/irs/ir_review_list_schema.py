from marshmallow import Schema, fields

from schemas.irs.ir_review_schema import IRReviewSchema

class IRReviewListSchema(Schema):
    reviews = fields.List(fields.Nested(IRReviewSchema()))
