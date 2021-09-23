from marshmallow import Schema, fields

from schemas.users.user_schema import UserSchema


class ForumReplySchema(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    published_at = fields.DateTime(dump_only=True)
    owner = fields.Nested(UserSchema.owner_data(), dump_only=True)
