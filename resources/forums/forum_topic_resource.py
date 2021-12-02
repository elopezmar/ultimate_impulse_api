from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.forums.forum import Forum
from models.forums.forum_topic import ForumTopic
from schemas.forums.forum_topic_schema import ForumTopicSchema
from resources.utils import handle_request


class ForumTopicResource(Resource):
    def topic(self, forum_id: str, topic_id: str=None) -> ForumTopic:
        forum = Forum(forum_id).get()
        topic = ForumTopic(forum, topic_id)
        return topic

    @jwt_required()
    @handle_request()
    def post(self, forum_id: str):
        schema = ForumTopicSchema(partial=('id',))
        data = schema.load(request.get_json())
        topic = self.topic(forum_id).from_dict(data)
        topic.set()
        return schema.dump(topic.to_dict()), 201

    @handle_request()
    def get(self, forum_id: str):
        schema = ForumTopicSchema()
        topic = self.topic(forum_id, request.args['id']).get(
            replies=request.args.get('replies', '').lower() == 'true'
        )
        return schema.dump(topic.to_dict()), 200

    @jwt_required()
    @handle_request()
    def put(self, forum_id: str):
        schema = ForumTopicSchema(partial=('title', 'description'))
        data = schema.load(request.get_json())
        topic = self.topic(forum_id).from_dict(data)
        topic.update()
        return {'message': 'Topic updated.'}, 200

    @jwt_required()
    @handle_request()
    def delete(self, forum_id: str):
        schema = ForumTopicSchema(
            partial=('title', 'description'),
            only=('id',)
        )
        data = schema.load(request.get_json())
        topic = self.topic(forum_id).from_dict(data)
        topic.delete()
        return {'message': 'Topic deleted.'}, 200
