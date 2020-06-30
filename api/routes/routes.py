from flask import Blueprint, jsonify, request
from flask_cors import CORS

from api.database import mongo
import json


mod = Blueprint('main', __name__)
CORS(mod)

@mod.route('/', methods=['GET'])
def index():
    # insertData()
    print(fetchData(fromPlace='DEL', toPlace='BOM'))
    user_collection = mongo.db.discount
    data = user_collection['easemytrip'].find()
    data = list(data)
    del data[0]['_id']
    return jsonify(data[0]), 201


# test function to load data in mongodb
def insertData():
    # update path of data.json before using this function
    f = open('./easemytrip/data.json')
    data = json.load(f)
    user_collection = mongo.db.discount
    user_collection['easemytrip'].drop()
    user_collection['easemytrip'].insert(data)

"""
data_dict: Dictionary structure storing the mangodb query output
        Important Keys:  'from', 'to', 'departureData', 'returnDate', 
                        'traveller', 'cashCurrency', 'offers'
"""
def fetchData(fromPlace, toPlace):
    user_collection = mongo.db.discount
    data = user_collection['easemytrip'].find()
    for record in data:
        data_dict = record
        print(data_dict.keys())
        if (data_dict['from'] == fromPlace and data_dict['to'] == toPlace):
            return json.dumps(data_dict, default=str)
        else:
            return None