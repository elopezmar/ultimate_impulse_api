from marshmallow import Schema, fields

from schemas.forums.forum_topic_schema import ForumTopicSchema


class ForumTopicListSchema(Schema):
    topics = fields.List(fields.Nested(ForumTopicSchema()))
