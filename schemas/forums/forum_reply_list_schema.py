from marshmallow import Schema, fields

from schemas.forums.forum_reply_schema import ForumReplySchema


class ForumReplyListSchema(Schema):
    replies = fields.List(fields.Nested(ForumReplySchema()))
