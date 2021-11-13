from marshmallow import Schema, fields

from schemas.reviews.review_comment_schema import ReviewCommentSchema
from schemas.reviews.review_section_schema import ReviewSectionSchema
from schemas.owners.owner_schema import OwnerSchema


class ReviewSchema(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    published_at = fields.DateTime(dump_only=True)
    pic_url = fields.Url(required=True)
    owner = fields.Nested(OwnerSchema(), dump_only=True)
    content = fields.List(fields.Nested(ReviewSectionSchema()))
    comments = fields.List(fields.Nested(ReviewCommentSchema(), dump_only=True))
    tags = fields.List(fields.Str())
