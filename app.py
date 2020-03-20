from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from db import db

from resources.user import UserRegister, UserLanguage, UserRole, UserServiceType, UserLogin
from resources.userinfo import UserInfo, UserInfoMine
from resources.provide import AllProvide, MyProvide, ProvideByService, ProvideByLanguage, UpdateProvide, ProvideByServiceAndLanguage
from resources.request import AllRequest, RequestByLanguage, RequestByService, RequestByServiceAndLanguage, RequestDeleteAndUpdate, RequestItem, MyRequest, PostRequest
from resources.comment import Comments, PostComment, CommentItem, CheckComment
from resources.admin import AdminLanguage, AdminRole, AdminServiceType, AdminUser

app = Flask(__name__)
CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0603018liu@localhost:3306/servicebooking'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0603018liu@servicebookingrds.c2g4pj5ev9gn.us-east-2.rds' \
                                        '.amazonaws.com:3306/servicebooking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'henrySecretToken'
db.init_app(app)
api = Api(app)


@app.before_first_request
def create_tables():
    print('test git again from 1')
    db.create_all()


# User Resource
api.add_resource(UserLogin, '/api/users/login')
api.add_resource(UserRegister, '/api/users/register')
api.add_resource(UserLanguage, '/api/users/language')
api.add_resource(UserRole, '/api/users/role')
api.add_resource(UserServiceType, '/api/users/serviceType')

# UserInfo Resource
api.add_resource(UserInfo, '/api/userinfo')
api.add_resource(UserInfoMine, '/api/userinfo/me')

# Provide Resource
api.add_resource(AllProvide, '/api/provider')
api.add_resource(ProvideByService, '/api/provider/name/<string:serviceName>')
api.add_resource(ProvideByLanguage, '/api/provider/language/<string:languageName>')
api.add_resource(ProvideByServiceAndLanguage, '/api/provider/<string:serviceName>/<string:languageName>')
api.add_resource(MyProvide, '/api/provider/me')
api.add_resource(UpdateProvide, '/api/provider/update')

# Request Resource
api.add_resource(AllRequest, '/api/request/All')
api.add_resource(MyRequest, '/api/request/me')
api.add_resource(RequestByService, '/api/request/name/<string:serviceName>')
api.add_resource(RequestByLanguage, '/api/request/language/<string:languageName>')
api.add_resource(RequestItem, '/api/request/list/<string:RequestId>')
api.add_resource(RequestByServiceAndLanguage, '/api/request/<string:serviceName>/<string:languageName>')
api.add_resource(RequestDeleteAndUpdate, '/api/request/id/<string:RequestId>')
api.add_resource(PostRequest, '/api/request')

# Comment Resource
api.add_resource(PostComment, '/api/comment/post/<string:RequestOrderId>')
api.add_resource(Comments, '/api/comment/get/<string:RequestOrderId>')
api.add_resource(CommentItem, '/api/comment/id/<string:CommentId>')
api.add_resource(CheckComment, '/api/comment/check/<string:RequestOrderId>')

# Admin Resource
api.add_resource(AdminUser, '/api/admin/user')
api.add_resource(AdminRole, '/api/admin/role')
api.add_resource(AdminLanguage, '/api/admin/language')
api.add_resource(AdminServiceType, '/api/admin/serviceType')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
