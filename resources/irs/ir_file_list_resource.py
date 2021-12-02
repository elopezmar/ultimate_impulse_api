from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models.irs.ir import IR
from models.irs.ir_file_list import IRFileList
from schemas.irs.ir_file_list_schema import IRFileListSchema
from resources.utils import handle_request


class IRFileListResource(Resource):
    @jwt_required(optional=True)
    @handle_request()
    def get(self, ir_id: str):
        schema = IRFileListSchema()
        files = IRFileList(IR(ir_id).get()).get()
        return schema.dump(files.to_dict('files')), 200
            