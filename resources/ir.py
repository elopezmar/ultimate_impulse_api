from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from resources.common.base import CollectionResource, DocumentResource

from gcp.storage import Storage

from schemas.ir import (
    IRFileSchema, 
    IRFilesSchema, 
    IRReviewsSchema, 
    IRSampleSchema, 
    IRSamplesSchema, 
    IRSchema, 
    IRReviewSchema,
    IRsSchema
)
from schemas.common.exceptions import BusinessError
from schemas.common.security import Roles, Methods


class IRSample(DocumentResource):
    def __init__(self, *args, **kwargs):
        super().__init__(IRSampleSchema(), *args, **kwargs)
        self.security.remove_privilege(Roles.USER, Methods.POST)
        self.security.remove_privilege(Roles.USER, Methods.PUT)
        self.security.remove_privilege(Roles.USER, Methods.DELETE)

    @jwt_required()
    def post(self, ir_id):
        try:
            self.load_request_data()
            self.schema.partial = ('id',)
            sample = self.schema.load(self.json)
            temp_file_url = sample['file_url']
            target_file_url = self.storage.get_target_file_url(temp_file_url)
            sample['file_url'] = target_file_url
            sample = self.schema.set_owner(sample)
            sample = self.schema.set_document(sample, (ir_id,))
            self.storage.replace_file(temp_file_url, target_file_url, make_public=True)
            return self.schema.dump(sample), 201
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    def get(self, ir_id):
        try:
            self.load_request_data()
            sample = {'id': self.args['id']}
            sample = self.schema.get_document(sample, (ir_id,))
            return self.schema.dump(sample), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message

    
class IRFile(DocumentResource):
    def __init__(self, *args, **kwargs):
        super().__init__(IRFileSchema(), *args, **kwargs)
        self.security.remove_privilege(Roles.USER, Methods.POST)
        self.security.remove_privilege(Roles.USER, Methods.PUT)
        self.security.remove_privilege(Roles.USER, Methods.DELETE)

    @jwt_required()
    def post(self, ir_id):
        try:
            self.load_request_data()
            self.schema.partial = ('id',)

            file = self.schema.load(self.json)
            
            ir = IRSchema().get_document({'id': ir_id})
            make_public = not ir.get('premium', False)
            temp_file_url = file['file_url']
            target_file_url = self.storage.get_target_file_url(temp_file_url)

            file['file_url'] = target_file_url
            file = self.schema.set_owner(file)
            file = self.schema.set_document(file, (ir_id,))
            
            self.storage.replace_file(temp_file_url, target_file_url, make_public)
            
            return self.schema.dump(file), 201
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    def get(self, ir_id):
        try:
            self.load_request_data()
            ir = {'id': ir_id}
            ir = IRSchema().get_document(ir)
            file = {'id': self.args['id']}
            file = self.schema.get_document(file, (ir_id,))
            file = self.schema.manage_file(file, ir)
            return self.schema.dump(file), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message


class IRReview(DocumentResource):
    def __init__(self, *args, **kwargs):
        super().__init__(IRReviewSchema(), *args, **kwargs)

    @jwt_required()
    def post(self, ir_id):
        try:
            #TODO: Solo una review por usuario

            self.load_request_data()
            self.schema.partial = ('id',)

            review = self.schema.load(self.json)
            review = self.schema.set_owner(review)
            review = self.schema.set_document(review, (ir_id,))

            IRSchema().update_stats(ir_id)

            return self.schema.dump(review), 201
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    def get(self, ir_id):
        try:
            self.load_request_data()
            review = {'id': self.args['id']}
            review = self.schema.get_document(review, (ir_id,))
            return self.schema.dump(review), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message


class IR(DocumentResource):
    def __init__(self, *args, **kwargs):
        super().__init__(IRSchema(), *args, **kwargs)
        self.security.remove_privilege(Roles.USER, Methods.POST)
        self.security.remove_privilege(Roles.USER, Methods.PUT)
        self.security.remove_privilege(Roles.USER, Methods.DELETE)

        self.sample_schema = IRSampleSchema()
        self.file_schema = IRFileSchema()
        self.review_schema = IRReviewSchema()

        self.sample_schema.security = self.security
        self.file_schema.security = self.security
        self.review_schema.security = self.security

        self.sample_storage = Storage(self.sample_schema.schema_id)
        self.file_storage = Storage(self.file_schema.schema_id)

    @jwt_required()
    def post(self):
        try:
            self.load_request_data()
            self.schema.partial = ('id', 'samples.id', 'files.id')

            ir = self.schema.load(self.json)

            files_to_replace = []

            ir['pics_url'] = ir.get('pics_urls', [])
            samples = ir.pop('samples', [])
            files = ir.pop('files', [])

            for x in range(len(ir['pics_url'])):
                temp_file_url = ir['pics_url'][x]
                target_file_url = self.storage.get_target_file_url(temp_file_url)
                files_to_replace.append((temp_file_url, target_file_url, True))
                ir['pics_urls'][x] = target_file_url

            for x in range(len(samples)):
                temp_file_url = samples[x]['file_url']
                target_file_url = self.sample_storage.get_target_file_url(temp_file_url)
                files_to_replace.append((temp_file_url, target_file_url, True))
                samples[x]['file_url'] = target_file_url
            
            for x in range(len(files)):
                temp_file_url = files[x]['file_url']
                target_file_url = self.file_storage.get_target_file_url(temp_file_url)
                files_to_replace.append((temp_file_url, target_file_url, not ir['premium']))
                files[x]['file_url'] = target_file_url

            ir = self.schema.set_owner(ir)
            ir = self.schema.set_document(ir)
            ir['samples'] = []
            ir['files'] = []
            
            for sample in samples:
                sample = self.sample_schema.set_owner(sample)
                ir['samples'].append(self.sample_schema.set_document(sample, (ir['id'],)))

            for file in files:
                file = self.file_schema.set_owner(file)
                ir['files'].append(self.file_schema.set_document(file, (ir['id'],)))
                
            for temp_file_url, target_file_url, make_public in files_to_replace:
                self.storage.replace_file(temp_file_url, target_file_url, make_public)

            return self.schema.dump(ir)
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    @jwt_required(optional=True)
    def get(self):
        try:
            self.load_request_data()

            ir_samples_schema = IRSamplesSchema()
            ir_files_schema = IRFilesSchema()
            ir_reviews_schema = IRReviewsSchema()

            ir_files_schema.security = self.security
            
            ir = {'id': self.args['id']}
            ir = self.schema.get_document(ir)

            if self.args.get('samples', '').lower() == 'true':
                ir.update(ir_samples_schema.get_documents((ir['id'],)))
            if self.args.get('files', '').lower() == 'true':
                files = ir_files_schema.get_documents((ir['id'],))
                files = ir_files_schema.manage_files(files, ir)
                ir.update(files)
            if self.args.get('reviews', '').lower() == 'true':
                ir.update(ir_reviews_schema.get_documents((ir['id'],)))

            return self.schema.dump(ir), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message


class IRSamples(CollectionResource):
    def __init__(self, *args, **kwargs):
        super().__init__(IRSamplesSchema(), *args, **kwargs)

    def get(self, ir_id):
        try:
            self.load_request_data()
            samples = self.schema.get_documents((ir_id,))
            return self.schema.dump(samples), 200
        except BusinessError as err:
            return err.message


class IRFiles(CollectionResource):
    def __init__(self, *args, **kwargs):
        super().__init__(IRFilesSchema(), *args, **kwargs)

    @jwt_required(optional=True)
    def get(self, ir_id):
        try:
            self.load_request_data()
            ir = {'id': ir_id}
            ir = IRSchema().get_document(ir)
            files = self.schema.get_documents((ir_id,))
            files = self.schema.manage_files(files, ir)
            return self.schema.dump(files), 200
        except BusinessError as err:
            return err.message


class IRReviews(CollectionResource):
    def __init__(self, *args, **kwargs):
        super().__init__(IRReviewsSchema(), *args, **kwargs)

    def get(self, ir_id):
        try:
            self.load_request_data()
            reviews = self.schema.get_documents((ir_id,))
            return self.schema.dump(reviews), 200
        except BusinessError as err:
            return err.message


class IRs(CollectionResource):
    def __init__(self, *args, **kwargs):
        super().__init__(IRsSchema(), *args, **kwargs)

    def get(self):
        try:
            self.load_request_data()
            irs = self.schema.get_documents()
            return self.schema.dump(irs), 200
        except BusinessError as err:
            return err.message

