import uuid
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from marshmallow import Schema, fields, validate
from google.api_core.exceptions import NotFound

from firestore import firestore, db, doc_to_dict

from schemas.user import UserSchema
from schemas.exceptions import BusinessError


class __BaseSchema(Schema):
    FORUMS = 'forums'
    TOPICS = 'topics'
    REPLIES = 'replies'
    OWNER_FIELDS = ('id', 'username') #, 'profile.country', 'profile.social_media')

    # TODO Validar los campos requeridos y valores minimos
    id = fields.Str(required=True, validate=validate.Length(equal=32))
    title = fields.Str(required=True, validate=validate.Length(min=5))
    description = fields.Str(required=True, validate=validate.Length(min=10))
    created_at = fields.DateTime(missing=datetime.now())
    owner = fields.Nested(UserSchema(
        only=OWNER_FIELDS
    ))

    @classmethod
    def get_collection_path(cls, forum_id=None, topic_id=None):
        path = cls.FORUMS
        if forum_id:
            path = f'/{forum_id}/{cls.TOPICS}'
            if topic_id:
                path = f'/{topic_id}/{cls.REPLIES}'
        return path

    @classmethod
    def get_document_path(cls, forum_id, topic_id=None, reply_id=None):
        path = f'{cls.FORUMS}/{forum_id}'
        if topic_id:
            path = f'{path}/{cls.TOPICS}/{topic_id}'
            if reply_id:
                path = f'{path}/{cls.REPLIES}/{reply_id}'                
        return path

    @classmethod
    def get_owner(cls):
        owner_id = get_jwt_identity()
        user_schema = UserSchema(only=cls.OWNER_FIELDS)
        owner = user_schema.read(user_id=owner_id)
        # TODO Verificar los permisos que podran crear elementos del foro
        return user_schema.load(owner, partial=True)


class ReplySchema(__BaseSchema, Schema):
    def create(self, forum_id, topic_id, reply):
        TopicSchema.increment_stats(forum_id, topic_id, num_of_replies=1)
        ForumSchema.increment_stats(forum_id, num_of_replies=1)
        reply_id = uuid.uuid1().hex
        reply['owner'] = self.get_owner()
        db.document(self.get_document_path(forum_id, topic_id, reply_id)).set(reply)
        reply['id'] = reply_id
        return self.dump(reply)

    def read(self, forum_id, topic_id, reply_id, dump=True):
        doc = db.document(self.get_document_path(forum_id, topic_id, reply_id)).get()
        reply = doc_to_dict(doc)
        if reply:
            return self.dump(reply) if dump else reply
        raise BusinessError('Reply not found.', 404)


class TopicSchema(__BaseSchema):
    stats = fields.Dict(
        replies=fields.Integer,
        views=fields.Integer
    )

    @classmethod
    def increment_stats(cls, forum_id, topic_id, num_of_replies=0, num_of_views=0):
        try:
            forum_ref = db.document(cls.get_document_path(forum_id, topic_id))
            forum_ref.update({
                'stats.replies': firestore.Increment(num_of_replies),
                'stats.views': firestore.Increment(num_of_views)
            })
        except NotFound:
            raise BusinessError('Topic not found.', 404)

    def create(self, forum_id, topic):
        ForumSchema.increment_stats(forum_id, num_of_topics=1)
        topic_id = uuid.uuid1().hex
        topic['owner'] = self.get_owner()
        db.document(self.get_document_path(forum_id, topic_id)).set(topic)
        topic['id'] = topic_id
        return self.dump(topic)

    def read(self, forum_id, topic_id, dump=True):
        doc = db.document(self.get_document_path(forum_id, topic_id)).get()
        topic = doc_to_dict(doc)
        if topic:
            return self.dump(topic) if dump else topic
        raise BusinessError('Topic not found.', 404)


class ForumSchema(__BaseSchema):
    stats = fields.Dict(
        topics=fields.Integer(),
        replies=fields.Integer()
    )

    @classmethod
    def increment_stats(cls, forum_id, num_of_topics=0, num_of_replies=0):
        try:
            forum_ref = db.document(cls.get_document_path(forum_id))
            forum_ref.update({
                'stats.topics': firestore.Increment(num_of_topics),
                'stats.replies': firestore.Increment(num_of_replies)
            })
        except NotFound:
            raise BusinessError('Forum not found.', 404)
    
    def create(self, forum):
        forum_id = uuid.uuid1().hex
        forum['owner'] = self.get_owner()
        db.document(self.get_document_path(forum_id)).set(forum)
        forum['id'] = forum_id
        return self.dump(forum)

    def read(self, forum_id, dump=True):
        doc = db.document(self.get_document_path(forum_id)).get()
        forum = doc_to_dict(doc)
        if forum:
            return self.dump(forum) if dump else forum
        raise BusinessError('Forum not found.', 404)

    
