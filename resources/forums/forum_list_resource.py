from flask_restful import Resource

from models.forums.forum_list import ForumList
from schemas.forums.forum_list_schema import ForumListSchema
from resources.utils import handle_errors


class ForumListResource(Resource):
    @handle_errors()
    def get(self):
        schema = ForumListSchema()
        forums = ForumList().get()
        return schema.dump(forums.to_dict()), 200
