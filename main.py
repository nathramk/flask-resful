from flask import Flask, jsonify
from flask_restful import Resource, Api
#from flask_jwt import JWT
from flask_jwt_extended import JWTManager
#from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.items import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST
#from flask_sqlalchemy import SQLAlchemy
import os

#os.system("python create_tables.py")

app = Flask(__name__)
app.secret_key='ken'
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['JWT_BLACKLIST_ENABLED']=True
app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access', 'refresh']

@app.before_first_request
def create_tables():
    db.create_all()
#el archivo security.py no o necesitamos para el jwt-extended solo es valido para el jwt
#jwt = JWT(app, authenticate, identity) #/auth
jwt = JWTManager(app) #this not create /auth
#db = SQLAlchemy(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity ==1:
        return {'is_admin': True}
    else:
        return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'dexcription': 'The token has expired.',
        'error': 'token expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify({
        'desciption':'Signaure verification failed',
        'error':'invalid_token'
    }), 401
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401

#items = []


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/item')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin,'/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')



if __name__=='__main__':
    from db.db import db
    db.init_app(app)
    app.run(debug=True)