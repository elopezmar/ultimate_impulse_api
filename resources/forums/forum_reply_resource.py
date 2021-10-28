from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.forums.forum import Forum
from models.forums.forum_reply import ForumReply
from models.forums.forum_topic import ForumTopic
from schemas.forums.forum_reply_schema import ForumReplySchema
from resources.utils import get_requestor, handle_errors


class ForumReplyResource(Resource):
    def reply(self, forum_id: str, topic_id: str, reply_id: str=None) -> ForumReply:
        forum = Forum(forum_id).get()
        topic = ForumTopic(forum, topic_id).get()
        reply = ForumReply(topic, reply_id)
        return reply

    @jwt_required()
    @handle_errors()
    def post(self, forum_id: str, topic_id: str):
        schema = ForumReplySchema(partial=('id',))
        data = schema.load(request.get_json())
        reply = self.reply(forum_id, topic_id).from_dict(data)
        reply.set(get_requestor())
        return schema.dump(reply.to_dict()), 201

    @handle_errors()
    def get(self, forum_id: str, topic_id: str):
        schema = ForumReplySchema()
        reply = self.reply(forum_id, topic_id, request.args['id']).get()
        return schema.dump(reply.to_dict()), 200

    @jwt_required()
    @handle_errors()
    def put(self, forum_id: str, topic_id: str):
        schema = ForumReplySchema(partial=('title', 'description'))
        data = schema.load(request.get_json())
        reply = self.reply(forum_id, topic_id).from_dict(data)
        reply.update(get_requestor())
        return {'message': 'Reply updated.'}, 200

    @jwt_required()
    @handle_errors()
    def delete(self, forum_id: str, topic_id: str):
        schema = ForumReplySchema(
            partial=('title', 'description'),
            only=('id',)
        )
        data = schema.load(request.get_json())
        reply = self.reply(forum_id, topic_id).from_dict(data)
        reply.delete(get_requestor())
        return {'message': 'Reply deleted.'}, 200
