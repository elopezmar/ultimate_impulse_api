from flask_restful import Resource

from models.irs.ir import IR
from models.irs.ir_sample_list import IRSampleList
from schemas.irs.ir_sample_list_schema import IRSampleListSchema
from resources.utils import handle_request


class IRSampleListResource(Resource):
    @handle_request()
    def get(self, ir_id: str):
        schema = IRSampleListSchema()
        samples = IRSampleList(IR(ir_id)).get()
        return schema.dump(samples.to_dict('samples')), 200
            