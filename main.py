from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from resources.donation_blueprint import donation_blueprint
from resources.file_blueprint import file_blueprint
from resources.forum_blueprint import forum_blueprint
from resources.ir_blueprint import ir_blueprint
from resources.purchase_blueprint import purchase_blueprint
from resources.review_blueprint import review_blueprint
from resources.user_blueprint import user_blueprint

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = '123456'

CORS(app)
jwt = JWTManager(app)

app.register_blueprint(donation_blueprint)
app.register_blueprint(file_blueprint)
app.register_blueprint(forum_blueprint)
app.register_blueprint(ir_blueprint)
app.register_blueprint(purchase_blueprint)
app.register_blueprint(review_blueprint)
app.register_blueprint(user_blueprint)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
