from flask_restful import Resource

from models.exceptions import BusinessError
from models.irs.ir import IR
from models.irs.ir_sample_list import IRSampleList
from schemas.irs.ir_sample_list_schema import IRSampleListSchema


class IRSampleListResource(Resource):
    def get(self, ir_id: str):
        try:
            schema = IRSampleListSchema()
            samples = IRSampleList(IR(ir_id)).get()
            return schema.dump(samples.to_dict()), 200
        except BusinessError as err:
            return err.message
            