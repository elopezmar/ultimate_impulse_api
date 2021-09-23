from marshmallow import Schema, fields

from schemas.forums.forum_schema import ForumSchema


class ForumListSchema(Schema):
    forums = fields.List(fields.Nested(ForumSchema()))
