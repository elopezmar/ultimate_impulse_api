from flask_restful import Resource, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from schemas.forum import ReplySchema, TopicSchema, ForumSchema, BusinessError

class Reply(Resource):
    reply_schema = ReplySchema()

    @jwt_required()
    def post(self, forum_id, topic_id):
        try:
            json_data = request.get_json()
            reply = self.reply_schema.load(json_data, partial=('id',))
            return self.reply_schema.create(forum_id, topic_id, reply), 201
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    def get(self, forum_id, topic_id):
        try:
            args = request.args
            reply_id = args['id']
            return self.reply_schema.read(forum_id, topic_id, reply_id), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message


class Topic(Resource):
    topic_schema = TopicSchema()

    @jwt_required()
    def post(self, forum_id):
        try:
            json_data = request.get_json()
            topic = self.topic_schema.load(json_data, partial=('id',))
            return self.topic_schema.create(forum_id, topic), 201
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    def get(self, forum_id):
        try:
            args = request.args
            topic_id = args['id']
            return self.topic_schema.read(forum_id, topic_id), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message
    

class Forum(Resource):
    forum_schema = ForumSchema()

    @jwt_required()    
    def post(self):
        json_data = request.get_json()

        try:
            forum = self.forum_schema.load(json_data, partial=('id',))
            return self.forum_schema.create(forum), 201
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message
        
    def get(self):
        try:
            args = request.args
            forum_id = args['id']
            return self.forum_schema.read(forum_id), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message
