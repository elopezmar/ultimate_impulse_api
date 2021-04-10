from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import User, UserLogin, UserVerify
from resources.ir import IR, IRReview
from resources.forum import Forum, Topic, Reply

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '123456'
jwt = JWTManager(app)

api = Api(app)

api.add_resource(User, '/user')
api.add_resource(UserLogin, '/user/login')
api.add_resource(UserVerify, '/user/verify')
api.add_resource(IR, '/ir')
api.add_resource(IRReview, '/ir/<string:ir_id>/review')
api.add_resource(Forum, '/forum')
api.add_resource(Topic, '/forum/<string:forum_id>/topic')
api.add_resource(Reply, '/forum/<string:forum_id>/topic/<string:topic_id>/reply')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)