from flask_restful import Resource

from models.forums.forum_list import ForumList
from schemas.forums.forum_list_schema import ForumListSchema
from resources.utils import handle_request


class ForumListResource(Resource):
    @handle_request()
    def get(self):
        schema = ForumListSchema()
        forums = ForumList().get()
        return schema.dump(forums.to_dict('forums')), 200
