from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.forums.forum import Forum
from schemas.forums.forum_schema import ForumSchema
from resources.utils import handle_request


class ForumResource(Resource):
    @jwt_required()
    @handle_request()
    def post(self):
        schema = ForumSchema(partial=('id',))
        data = schema.load(request.get_json())
        forum = Forum().from_dict(data)
        forum.set()
        return schema.dump(forum.to_dict()), 201

    @handle_request()
    def get(self):
        schema = ForumSchema()
        forum = Forum(request.args['id']).get(
            topics=request.args.get('topics', '').lower() == 'true'
        )
        return schema.dump(forum.to_dict()), 200

    @jwt_required()
    @handle_request()
    def put(self):
        schema = ForumSchema(partial=('title', 'description'))
        data = schema.load(request.get_json())
        forum = Forum().from_dict(data)
        forum.update()
        return {'message': 'Forum updated.'}, 200

    @jwt_required()
    @handle_request()
    def delete(self):
        schema = ForumSchema(
            partial=('title', 'description'),
            only=('id',)
        )
        data = schema.load(request.get_json())
        forum = Forum().from_dict(data)
        forum.delete()
        return {'message': 'Forum deleted.'}, 200
