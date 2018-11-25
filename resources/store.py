from flask_restful import Resource
from models.store import StoreModel
from flask_jwt import jwt_required

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "store not found"}, 404
    def post(self, name):
        storefind = StoreModel.find_by_name(name)
        if storefind:
            return {"message": "the store whit name '{}' already exist.".format(name)}, 400
        store = StoreModel(name) 
        try:
            store.save_to_db()
        except:
            return {"message":"An error ocurred creating a store."}, 500
        
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            delete = StoreModel(store)
            delete.delete_from_db()
            return {"message":"store deleted"}
        else:
            return {"message": "the storer with name '{}' not found".format(name)}, 404    


class StoreList(Resource):
    def get(self):
        return {"Stores": [store.json() for store in StoreModel.find_all()]}