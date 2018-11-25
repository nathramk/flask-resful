#import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity, 
    fresh_jwt_required
    )
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help="this field cannot be left blank"
    )
    parser.add_argument('store_id',
        type = int,
        required = True,
        help="every item need a store id."
    )
    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {"message": "item not found"}, 404
    ## reciente    item = next(filter(lambda x: x['name']==name, items), None) #esto funciona igual que ..
    #    for item in items:

    #        if item['name']==name: # todo esto
    #            return item
    #    return {'item': None}, 404
    ## reciente    return {'item': item}, 200 if item else 404
    
    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
             return {'message': 'this item whit name {} already exist'.format(name)},400
        #if next(filter(lambda x: x['name']==name, items), None):
        #    return {'message': 'this item whit name {} already exist'.format(name)},400
        #request_data=request.get_json()
        request_data = Item.parser.parse_args()
        #item = {'name':name, 'price': request_data['price']}
        item = ItemModel(name, **request_data) # **request_data es igual a decir request_data['price'], request_data['store_id']
        #items.append(item)
        try:
            #ItemModel.insert(item)
            #item.insert()
            item.save_to_db()
        except:
            return {"message":"error ocurred insterting the item"}, 500
        

        return item.json(), 201

    
    @jwt_required
    def delete(self, name):
        #item = ItemModel.find_by_name(name)
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message':'Admin privilegie required.'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()
        #query = "DELETE FROM items WHERE name=?"
        #cursor.execute(query,(name,))
        #connection.commit()
        #connection.close()
        #-------------------------------------
        #global items
        #items = list(filter(lambda x: x['name']!=name, items))
            return {'message': 'Item deteled'}
        return {'messsage': 'Item not found'}, 404
    def put(self, name):
       
        
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        #update_item = {'name':name, 'price': data['price']}
        #update_item = ItemModel(name, data['price'])
        #data = request.get_json()
        #item = next(filter(lambda x: x['name'] == name, items), None)s
        if item is None:
            item = ItemModel(name, **data)
            #item = {'name': name, 'price':data['price']}
            #try:
                #ItemModel.insert(update_item)
                #update_item.insert()
                
            #except:
            #    return {"message": "An error ocurred inserting the item"}, 500
        else:
            item.price = data['price']
            #try:
                #ItemModel.update(update_item)
                #update_item.update()
            #except:
            #    return {"message": "An error ocurred updating the item"}, 500
            #item.update(data)
        item.save_to_db()
        return item.json()
    
    

class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [x.json() for x in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {'items': [item['name'] for item in items], 'message':'mode data available if you log in.'}, 200
        #return {'items': list(map(lambda x: x.json, ItemModel.query.all()))} #es otra manera de retornar una lista de items o siquieres usas el de listas por compresion.

        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "SELECT * FROM items"
        #result = cursor.execute(query)
        #items = []
        #for row in result:
        #    items.append({"id": row[0],"name":row[1], "price":row[2]})
        #---connection.commit() se ejecuta solo cuando vas a insertar  
        #connection.close()

        #return items