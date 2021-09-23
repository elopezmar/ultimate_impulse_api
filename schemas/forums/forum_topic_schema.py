from marshmallow import Schema, fields

from schemas.forums.forum_reply_schema import ForumReplySchema
from schemas.users.user_schema import UserSchema


class ForumTopicSchema(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    published_at = fields.DateTime(dump_only=True)
    owner = fields.Nested(UserSchema.owner_data(), dump_only=True)
    stats = fields.Dict(
        replies = fields.Integer(dump_only=True)
    )
    replies = fields.List(fields.Nested(ForumReplySchema()), dump_only=True)
