from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.forums.forum import Forum
from models.forums.forum_topic import ForumTopic
from schemas.forums.forum_topic_schema import ForumTopicSchema
from resources.utils import get_requestor, handle_errors


class ForumTopicResource(Resource):
    @jwt_required()
    @handle_errors()
    def post(self, forum_id: str):
        schema = ForumTopicSchema(partial=('id',))
        data = schema.load(request.get_json())
        forum = Forum(forum_id).get()
        topic = ForumTopic(forum).from_dict(data)
        topic.set(get_requestor())
        return schema.dump(topic.to_dict()), 201

    @handle_errors()
    def get(self, forum_id: str):
        schema = ForumTopicSchema()
        forum = Forum(forum_id)
        topic = ForumTopic(forum, request.args['id']).get(
            replies=request.args.get('replies', '').lower() == 'true'
        )
        return schema.dump(topic.to_dict()), 200

    @jwt_required()
    @handle_errors()
    def put(self, forum_id: str):
        schema = ForumTopicSchema(partial=('title', 'description'))
        data = schema.load(request.get_json())
        forum = Forum(forum_id)
        topic = ForumTopic(forum).from_dict(data)
        topic.update(get_requestor())
        return {'message': 'Topic updated.'}, 200

    @jwt_required()
    @handle_errors()
    def delete(self, forum_id: str):
        schema = ForumTopicSchema(
            partial=('title', 'description'),
            only=('id',)
        )
        data = schema.load(request.get_json())
        forum = Forum(forum_id)
        topic = ForumTopic(forum).from_dict(data)
        topic.delete(get_requestor())
        return {'message': 'Topic deleted.'}, 200
