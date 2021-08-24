from marshmallow import Schema, fields

from schemas.reviews.review_comment_schema import ReviewCommentSchema

class ReviewCommentListSchema(Schema):
    comments = fields.List(fields.Nested(ReviewCommentSchema()))
    