from werkzeug.security import safe_str_cmp
from models.user import UserModel

#users = [
#    User(1, "ken", "asdas")
#]

#username_mapping = { u.username: u for u in users}
#    "ken": {
#        "id":1,
#        "username":"ken",
#        "password":"asdas"
#    }


#userid_mapping = { u.id: u for u in users }
#    1: {
#        "id":1,
#        "username": "ken",
#        "passowrd": "asd"
#    }
#}

def authenticate(username, password):
#    user = username_mapping.get(username, None)
    user = UserModel.find_by_username(username)
    #if user and user.passowrd == passowrd: #esto no puede funcionar aveces en todas la versiones de python por eso importamos a werkzeug
    #    return user
    if user and safe_str_cmp(user.password, password): # es lo mismo que lo que comentamos solo que esto si va a funcionar con toda las versiones de python
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
    #return userid_mapping.get(user_id, None)