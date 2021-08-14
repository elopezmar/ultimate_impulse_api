from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models.exceptions import BusinessError
from models.irs.ir import IR
from models.irs.ir_file_list import IRFileList
from schemas.irs.ir_file_list_schema import IRFileListSchema
from resources.utils import get_requestor


class IRFileListResource(Resource):
    @jwt_required(optional=True)
    def get(self, ir_id: str):
        try:
            requestor = get_requestor()
            schema = IRFileListSchema()
            files = IRFileList(IR(ir_id).get(requestor)).get(requestor)
            return schema.dump(files.to_dict()), 200
        except BusinessError as err:
            return err.message
            