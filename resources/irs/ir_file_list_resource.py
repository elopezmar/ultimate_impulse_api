from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models.irs.ir import IR
from models.irs.ir_file_list import IRFileList
from schemas.irs.ir_file_list_schema import IRFileListSchema
from resources.utils import get_requestor, handle_errors


class IRFileListResource(Resource):
    @jwt_required(optional=True)
    @handle_errors()
    def get(self, ir_id: str):
        requestor = get_requestor()
        schema = IRFileListSchema()
        files = IRFileList(IR(ir_id).get(requestor)).get(requestor)
        return schema.dump(files.to_dict('files')), 200
            