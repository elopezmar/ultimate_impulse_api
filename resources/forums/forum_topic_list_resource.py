from flask_restful import Resource

from models.forums.forum import Forum
from models.forums.forum_topic_list import ForumTopicList
from schemas.forums.forum_topic_list_schema import ForumTopicListSchema
from resources.utils import handle_request


class ForumTopicListResource(Resource):
    @handle_request()
    def get(self, forum_id: str):
        schema = ForumTopicListSchema()
        forum = Forum(forum_id)
        topics = ForumTopicList(forum).get()
        return schema.dump(topics.to_dict('topics')), 200
