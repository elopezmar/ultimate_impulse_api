import uuid
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from marshmallow import Schema, fields

from firestore import db, doc_to_dict, docs_to_dict

from schemas.user import UserSchema
from schemas.exceptions import BusinessError


class __BaseSchema(Schema):
    IRS = 'irs'
    SAMPLES = 'samples'
    FILES = 'files'
    REVIEWS = 'reviews'

    id = fields.Str(dump_only=True)
    title = fields.Str()
    description = fields.Str()


class IRSampleSchema(__BaseSchema):
    sample_url = fields.Str()

    @classmethod
    def get_document_path(cls, ir_id, sample_id):
        return f'{cls.IRS}/{ir_id}/{cls.SAMPLES}/{sample_id}'

    def create(self, ir_id, sample, dump=True):
        sample_id = uuid.uuid1().hex
        db.document(self.get_document_path(ir_id, sample_id)).set(sample)
        sample['id'] = sample_id
        return self.dump(sample) if dump else sample

    def read(self, ir_id, sample_id, dump=True):
        doc = db.document(self.get_document_path(ir_id, sample_id)).get()
        sample = doc_to_dict(doc)
        if sample:
            return self.dump(sample) if dump else sample
        raise BusinessError('Sample not found.', 404)


class IRFileSchema(__BaseSchema):
    file_url = fields.Str()
    # settings = fields.List(fields.Str())

    @classmethod
    def get_document_path(cls, ir_id, file_id):
        return f'{cls.IRS}/{ir_id}/{cls.FILES}/{file_id}'

    def create(self, ir_id, file, dump=True):
        file_id = uuid.uuid1().hex
        db.document(self.get_document_path(ir_id, file_id)).set(file)
        file['id'] = file_id
        return self.dump(file) if dump else file

    def read(self, ir_id, file_id, dump=True):
        doc = db.document(self.get_document_path(ir_id, file_id)).get()
        file = doc_to_dict(doc)
        if file:
            return self.dump(file) if dump else file
        raise BusinessError('File not found.', 404)


class IRReviewSchema(__BaseSchema):
    USER_FIELDS = ('id', 'username', 'profile.country', 'profile.social_media')

    created_at = fields.DateTime(missing=datetime.now())
    user = fields.Nested(UserSchema(
        only=USER_FIELDS
    ))
    rating = fields.Float()
    likes = fields.Integer()

    @classmethod
    def get_user(cls):
        user_id = get_jwt_identity()
        user_schema = UserSchema(only=cls.USER_FIELDS)
        owner = user_schema.read(user_id=user_id)
        return user_schema.load(owner, partial=True)

    @classmethod
    def get_document_path(cls, ir_id, review_id):
        return f'{cls.IRS}/{ir_id}/{cls.REVIEWS}/{review_id}'

    def create(self, ir_id, review, dump=True):
        review_id = uuid.uuid1().hex
        review['user'] = self.get_user()
        db.document(self.get_document_path(ir_id, review_id)).set(review)
        review['id'] = review_id
        return self.dump(review) if dump else review

    def read(self, ir_id, review_id, dump=True):
        doc = db.document(self.get_document_path(ir_id, review_id)).get()
        review = doc_to_dict(doc)
        if review:
            return self.dump(review) if dump else review
        raise BusinessError('Review not found.', 404)


class IRSampleListSchema(__BaseSchema):
    samples = fields.List(fields.Nested(IRSampleSchema()))

    @classmethod
    def get_collection_path(cls, ir_id):
        return f'{cls.IRS}/{ir_id}/{cls.SAMPLES}'

    def read(self, ir_id, dump=True):
        docs = db.collection(self.get_collection_path(ir_id)).stream()
        samples = docs_to_dict(self.SAMPLES, docs)
        return self.dump(samples) if dump else samples


class IRFileListSchema(__BaseSchema):
    files = fields.List(fields.Nested(IRFileSchema()))

    @classmethod
    def get_collection_path(cls, ir_id):
        return f'{cls.IRS}/{ir_id}/{cls.FILES}'

    def read(self, ir_id, dump=True):
        docs = db.collection(self.get_collection_path(ir_id)).stream()
        files = docs_to_dict(self.FILES, docs)
        return self.dump(files) if dump else files


class IRReviewListSchema(__BaseSchema):
    reviews = fields.List(fields.Nested(IRReviewSchema()))

    @classmethod
    def get_collection_path(cls, ir_id):
        return f'{cls.IRS}/{ir_id}/{cls.REVIEWS}'

    def read(self, ir_id, dump=True):
        docs = db.collection(self.get_collection_path(ir_id)).stream()
        reviews = docs_to_dict(self.REVIEWS, docs)
        return self.dump(reviews) if dump else reviews


class IRSchema(__BaseSchema):
    published_at = fields.DateTime(missing=datetime.now())
    maker = fields.Str() # TODO Definirlo como un usuario
    pics_urls = fields.List(fields.Str())
    rating = fields.Float()
    samples = fields.List(fields.Nested(IRSampleSchema()))
    files = fields.List(fields.Nested(IRFileSchema()))
    reviews = fields.List(fields.Nested(IRReviewSchema()))

    @classmethod
    def get_document_path(cls, ir_id):
        return f'{cls.IRS}/{ir_id}'

    def create(self, ir, dump=True):
        ir_id = uuid.uuid1().hex
        samples = ir.pop('samples', None)
        files = ir.pop('files', None)
        db.document(self.get_document_path(ir_id)).set(ir)
        ir['id'] = ir_id
        if samples:
            ir['samples'] = []
            for sample in samples:
                ir['samples'].append(IRSampleSchema().create(ir_id, sample, dump=False))
        if files:
            ir['files'] = []
            for file in files:
                ir['files'].append(IRFileSchema().create(ir_id, file, dump=False))
        return self.dump(ir) if dump else ir

    def read(self, ir_id, samples=False, files=False, reviews=False, dump=True):
        doc = db.document(self.get_document_path(ir_id)).get()
        ir = doc_to_dict(doc)
        if ir:
            if samples:
                ir.update(IRSampleListSchema().read(ir['id'], dump=False))
            if files:
                ir.update(IRFileListSchema().read(ir['id'], dump=False))
            if reviews:
                ir.update(IRReviewListSchema().read(ir['id'], dump=False))
            return self.dump(ir) if dump else ir
        raise BusinessError('IR not found.', 404)










