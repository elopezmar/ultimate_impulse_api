from flask import Blueprint
from flask_restful import Api

from resources.irs.ir_resource import IRResource
from resources.irs.ir_list_resource import IRListResource
from resources.irs.ir_sample_resource import IRSampleResource
from resources.irs.ir_sample_list_resource import IRSampleListResource
from resources.irs.ir_file_resource import IRFileResource
from resources.irs.ir_file_list_resource import IRFileListResource
from resources.irs.ir_review_resource import IRReviewResource
from resources.irs.ir_review_list_resource import IRReviewListResource
from resources.irs.ir_purchase_resource import IRPurchaseListResource

ir_blueprint = Blueprint('ìr', __name__)
api = Api(ir_blueprint)

api.add_resource(IRResource, '/ir')
api.add_resource(IRListResource, '/irs')
api.add_resource(IRSampleResource, '/ir/<string:ir_id>/sample')
api.add_resource(IRSampleListResource, '/ir/<string:ir_id>/samples')
api.add_resource(IRFileResource, '/ir/<string:ir_id>/file')
api.add_resource(IRFileListResource, '/ir/<string:ir_id>/files')
api.add_resource(IRReviewResource, '/ir/<string:ir_id>/review')
api.add_resource(IRReviewListResource, '/ir/<string:ir_id>/reviews')
api.add_resource(IRPurchaseListResource, '/ir/<string:ir_id>/purchases')
