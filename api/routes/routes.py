from flask import Blueprint, jsonify, request
from flask_cors import CORS

from api.database import mongo
import json


mod = Blueprint('main', __name__)
CORS(mod)

@mod.route('/', methods=['GET'])
def index():
    # insertData()
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
