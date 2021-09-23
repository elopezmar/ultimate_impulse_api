from marshmallow import Schema, fields

from schemas.forums.forum_topic_schema import ForumTopicSchema
from schemas.users.user_schema import UserSchema


class ForumSchema(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    published_at = fields.DateTime(dump_only=True)
    owner = fields.Nested(UserSchema.owner_data(), dump_only=True)
    stats = fields.Dict(
        topics = fields.Integer(dump_only=True),
        replies = fields.Integer(dump_only=True)
    )
    topics = fields.List(fields.Nested(ForumTopicSchema()), dump_only=True)
    
