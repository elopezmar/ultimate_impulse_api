from flask_restful import Resource

from models.irs.ir_list import IRList
from schemas.irs.ir_list_schema import IRListSchema
from resources.utils import handle_errors


class IRListResource(Resource):
    @handle_errors()
    def get(self):
        schema = IRListSchema()

        irs = IRList().get()
        return schema.dump(irs.to_dict('irs')), 200
