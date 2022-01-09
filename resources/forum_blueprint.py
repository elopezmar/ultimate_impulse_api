from flask import Blueprint
from flask.app import Flask
from flask_restful import Api

from resources.forums.forum_resource import ForumResource
from resources.forums.forum_list_resource import ForumListResource
from resources.forums.forum_topic_resource import ForumTopicResource
from resources.forums.forum_topic_list_resource import ForumTopicListResource
from resources.forums.forum_reply_resource import ForumReplyResource
from resources.forums.forum_reply_list_resource import ForumReplyListResource

forum_blueprint = Blueprint('forum', __name__)
api = Api(forum_blueprint, errors=Flask.errorhandler)

api.add_resource(ForumResource, '/forum')
api.add_resource(ForumListResource, '/forums')
api.add_resource(ForumTopicResource, '/forum/<string:forum_id>/topic')
api.add_resource(ForumTopicListResource, '/forum/<string:forum_id>/topics')
api.add_resource(ForumReplyResource, '/forum/<string:forum_id>/topic/<string:topic_id>/reply')
api.add_resource(ForumReplyListResource, '/forum/<string:forum_id>/topic/<string:topic_id>/replies')
