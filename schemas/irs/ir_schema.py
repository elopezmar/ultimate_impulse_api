from marshmallow import Schema, fields

from schemas.users.user_schema import UserSchema
from schemas.irs.ir_file_schema import IRFileSchema
from schemas.irs.ir_review_schema import IRReviewSchema
from schemas.irs.ir_sample_schema import IRSampleSchema


class IRSchema(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    published_at = fields.DateTime(dump_only=True)
    owner = fields.Nested(
        UserSchema(only=(
            'id', 
            'username', 
            'profile.country', 
            'profile.social_media'
        )), dump_only=True
    )
    pics_urls = fields.List(fields.Url())
    premium = fields.Boolean(missing=False)
    samples = fields.List(fields.Nested(IRSampleSchema()))
    files = fields.List(fields.Nested(IRFileSchema()))
    reviews = fields.List(fields.Nested(IRReviewSchema()), dump_only=True)
    stats = fields.Dict(
        reviews = fields.Integer(dump_only=True),
        rating = fields.Float(dump_only=True)
    ) 
    tags = fields.List(fields.String, missing=[])
