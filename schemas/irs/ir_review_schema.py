from datetime import datetime

from marshmallow import Schema, fields, validate

from schemas.users.user_schema import UserSchema


class IRReviewSchema(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    rating = fields.Float(required=True, validate=validate.Range(min=0, max=5))
    likes = fields.Integer(dump_only=True)
    created_at = fields.DateTime(missing=datetime.now())
    owner = fields.Nested(
        UserSchema(only=(
            'id', 
            'username', 
            'profile.country', 
            'profile.social_media'
        )), dump_only=True
    )
