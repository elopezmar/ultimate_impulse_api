from marshmallow import Schema, fields

from schemas.reviews.review_schema import ReviewSchema


class ReviewListSchema(Schema):
    reviews = fields.List(fields.Nested(ReviewSchema()))
