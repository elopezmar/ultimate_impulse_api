from flask_jwt_extended import jwt_required
from flask_restful import Resource, request
from marshmallow import ValidationError

from models.exceptions import BusinessError
from models.irs.ir import IR
from schemas.irs.ir_schema import IRSchema
from resources.utils import get_requestor


class IRResource(Resource):
    @jwt_required()
    def post(self):
        try:
            schema = IRSchema(partial=('id', 'samples.id', 'files.id'))
            data = schema.load(request.get_json())
            ir = IR().from_dict(data)
            ir.set(get_requestor())
            return schema.dump(ir.to_dict()), 201
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    @jwt_required(optional=True)
    def get(self):
        try:
            schema = IRSchema()
            ir = IR(id=request.args['id']).get(
                requestor=get_requestor(),
                samples=request.args.get('samples', '').lower() == 'true',
                files=request.args.get('files', '').lower() == 'true',
                reviews=request.args.get('reviews', '').lower() == 'true'
            )
            return schema.dump(ir.to_dict()), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message

    @jwt_required()
    def put(self):
        try:
            schema = IRSchema(
                partial=(
                    'title', 
                    'samples.title',
                    'samples.file_url',
                    'files.title',
                    'files.file_url'
            ))
            data = schema.load(request.get_json())
            ir = IR().from_dict(data)
            ir.update(get_requestor())
            return {'message': 'IR updated.'}, 200
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    @jwt_required()
    def delete(self):
        try:
            schema = IRSchema(
                partial=(
                    'title', 
                    'samples.title',
                    'samples.file_url',
                    'files.title',
                    'files.file_url'
                ),
                only=('id',)
            )
            data = schema.load(request.get_json())
            ir = IR().from_dict(data)
            ir.delete(get_requestor())
            return {'message': 'IR deleted.'}, 200
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message
