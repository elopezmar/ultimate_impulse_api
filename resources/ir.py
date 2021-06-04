from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from resources.common.base import BaseResource

from gcp.storage import Storage

from schemas.ir import (
    IRFileSchema, 
    IRFilesSchema, 
    IRReviewsSchema, 
    IRSampleSchema, 
    IRSamplesSchema, 
    IRSchema, 
    IRReviewSchema
)
from schemas.common.exceptions import BusinessError
from schemas.common.security import Roles, Methods


class IRSample(BaseResource):
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

    
class IRFile(BaseResource):
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
            make_public = True# TODO: Verificar si el IR es premium
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
            file = {'id': self.args['id']}
            file = self.schema.get_document(file, (ir_id,))
            return self.schema.dump(file), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message


class IRReview(BaseResource):
    def __init__(self, *args, **kwargs):
        super().__init__(IRReviewSchema(), *args, **kwargs)

    @jwt_required()
    def post(self, ir_id):
        try:
            self.load_request_data()
            self.schema.partial = ('id',)
            review = self.schema.load(self.json)
            review = self.schema.set_owner(review)
            review = self.schema.set_document(review, (ir_id,))
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


class IR(BaseResource):
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

    def get(self):
        try:
            self.load_request_data()
            
            ir = {'id': self.args['id']}
            ir = self.schema.get_document(ir)

            if self.args.get('samples', '').lower() == 'true':
                ir.update(IRSamplesSchema().get_documents((ir['id'],)))
            if self.args.get('files', '').lower() == 'true':
                ir.update(IRFilesSchema().get_documents((ir['id'],)))
            if self.args.get('reviews', '').lower() == 'true':
                ir.update(IRReviewsSchema().get_documents((ir['id'],)))

            return self.schema.dump(ir), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message
