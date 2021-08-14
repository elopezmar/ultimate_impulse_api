from flask_restful import Resource

from models.exceptions import BusinessError
from models.irs.ir_list import IRList
from schemas.irs.ir_list_schema import IRListSchema


class IRListResource(Resource):
    def get(self):
        try:
            schema = IRListSchema()
            irs = IRList().get()
            return schema.dump(irs.to_dict()), 200
        except BusinessError as err:
            return err.message
