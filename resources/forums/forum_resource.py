from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.forums.forum import Forum
from schemas.forums.forum_schema import ForumSchema
from resources.utils import get_requestor, handle_errors


class ForumResource(Resource):
    @jwt_required()
    @handle_errors()
    def post(self):
        schema = ForumSchema(partial=('id',))
        data = schema.load(request.get_json())
        forum = Forum().from_dict(data)
        forum.set(get_requestor())
        return schema.dump(forum.to_dict()), 201

    @handle_errors()
    def get(self):
        schema = ForumSchema()
        forum = Forum(request.args['id']).get(
            topics=request.args.get('topics', '').lower() == 'true'
        )
        return schema.dump(forum.to_dict()), 200

    @jwt_required()
    @handle_errors()
    def put(self):
        schema = ForumSchema(partial=('title', 'description'))
        data = schema.load(request.get_json())
        forum = Forum().from_dict(data)
        forum.update(get_requestor())
        return {'message': 'Forum updated.'}, 200

    @jwt_required()
    @handle_errors()
    def delete(self):
        schema = ForumSchema(
            partial=('title', 'description'),
            only=('id',)
        )
        data = schema.load(request.get_json())
        forum = Forum().from_dict(data)
        forum.delete(get_requestor())
        return {'message': 'Forum deleted.'}, 200
