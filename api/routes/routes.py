from flask import Blueprint, jsonify, request
from flask_cors import CORS

from api.database import mongo

mod = Blueprint('main', __name__)
CORS(mod)

@mod.route('/', methods=['GET'])
def index():
    user_collection = mongo.db.discount
    # post = {"_id": 0, "name": "mmt"}
    # user_collection.insert(post)
    pilot = user_collection.find_one({"name": "mmt"})
    return jsonify({'pilot': pilot}), 201
