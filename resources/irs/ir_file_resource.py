from flask_jwt_extended import jwt_required
from flask_restful import Resource, request
from marshmallow import ValidationError

from models.exceptions import BusinessError
from models.irs.ir import IR
from models.irs.ir_file import IRFile
from schemas.irs.ir_file_schema import IRFileSchema
from resources.utils import get_requestor


class IRFileResource(Resource):
    @jwt_required()
    def post(self, ir_id: str):
        try:
            requestor = get_requestor()
            schema = IRFileSchema(partial=('id',))
            
            file = IRFile(
                ir=IR(ir_id).get(requestor)
            ).from_dict(
                data=schema.load(request.get_json())
            )

            file.set(requestor)
            return schema.dump(file.to_dict()), 201
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    @jwt_required(optional=True)
    def get(self, ir_id: str):
        try:
            requestor = get_requestor()
            schema = IRFileSchema()

            file = IRFile(
                ir=IR(ir_id).get(requestor), 
                id=request.args['id']
            ).get(requestor)
            
            return schema.dump(file.to_dict()), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message

    @jwt_required()
    def put(self, ir_id: str):
        try:
            requestor = get_requestor()
            schema = IRFileSchema(partial=('title', 'file_url'))
            
            file = IRFile(
                ir=IR(ir_id).get(requestor)
            ).from_dict(
                data=schema.load(request.get_json())
            )
            
            file.update(requestor)
            return {'message': 'File updated.'}, 200
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message

    @jwt_required()
    def delete(self, ir_id: str):
        try:
            requestor = get_requestor()
            schema = IRFileSchema(partial=('title', 'file_url'), only=('id',))
            
            file = IRFile(
                ir=IR(ir_id).get(requestor)
            ).from_dict(
                data=schema.load(request.get_json())
            )
            
            file.delete(requestor)
            return {'message': 'File deleted.'}, 200
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message
