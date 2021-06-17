from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from resources.user import User, UserLogin, UserVerify, Users
from resources.ir import IR, IRSample, IRFile, IRReview, IRs, IRSamples, IRFiles, IRReviews
from resources.forum import Forum, Topic, Reply
from resources.file import File

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = '123456'

CORS(app)
jwt = JWTManager(app)
api = Api(app)

api.add_resource(User, '/user')
api.add_resource(Users, '/users')
api.add_resource(UserLogin, '/user/login')
api.add_resource(UserVerify, '/user/verify')
api.add_resource(IR, '/ir')
api.add_resource(IRSample, '/ir/<string:ir_id>/sample')
api.add_resource(IRFile, '/ir/<string:ir_id>/file')
api.add_resource(IRReview, '/ir/<string:ir_id>/review')
api.add_resource(IRs, '/irs')
api.add_resource(IRSamples, '/ir/<string:ir_id>/samples')
api.add_resource(IRFiles, '/ir/<string:ir_id>/files')
api.add_resource(IRReviews, '/ir/<string:ir_id>/reviews')
api.add_resource(Forum, '/forum')
api.add_resource(Topic, '/forum/<string:forum_id>/topic')
api.add_resource(Reply, '/forum/<string:forum_id>/topic/<string:topic_id>/reply')
api.add_resource(File, '/file')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)