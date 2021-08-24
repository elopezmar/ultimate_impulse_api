from datetime import datetime

from marshmallow import Schema, fields

from schemas.users.user_schema import UserSchema

class ReviewCommentSchema(Schema):
    id = fields.Str(required=True)
    description = fields.Str(required=True)
    created_at = fields.DateTime(missing=datetime.now())
    owner = fields.Nested(UserSchema.owner_data(), dump_only=True)
    