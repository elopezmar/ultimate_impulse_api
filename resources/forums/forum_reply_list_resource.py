from flask_restful import Resource

from models.forums.forum import Forum
from models.forums.forum_topic import ForumTopic
from models.forums.forum_reply_list import ForumReplyList
from schemas.forums.forum_reply_list_schema import ForumReplyListSchema
from resources.utils import handle_errors


class ForumReplyListResource(Resource):
    @handle_errors()
    def get(self, forum_id: str, topic_id: str):
        schema = ForumReplyListSchema()
        forum = Forum(forum_id)
        topic = ForumTopic(forum, topic_id)
        replies = ForumReplyList(topic).get()
        return schema.dump(replies.to_dict()), 200
