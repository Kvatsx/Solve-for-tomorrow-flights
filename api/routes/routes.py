from flask import Blueprint, jsonify, request
from flask_cors import CORS

from api.database import mongo
import json


mod = Blueprint('main', __name__)
CORS(mod)
# /easemytrip/from=<fr>&to=<to>&dd=<dd>&rd=<rd>&tvlr=<tvlr>&cl=<cl>
@mod.route('/easemytrip/from=<fr>&to=<to>&dd=<dd>&rd=<rd>&tvlr=<tvlr>&cl=<cl>', methods=['GET'])
# def index(fr, to, dd):
def index(fr, to, dd, rd, tvlr, cl):
    obj = {}
    if fr == "" or to == "" or dd == "" or len(tvlr) != 5 or cl == "":
        return jsonify({
            'status':404, 'message': "Incorrect api call",
            'exampleAPI': "/easemytrip/from=DEL-Delhi-India&to=BOM-Mumbai-India&dd=30-07-2020&rd=null&tvlr=1-0-0&cl=0"
        }), 404
    try :
        obj["from"] = [fr, fr.split('-')[0]]
        obj["to"] = [to, to.split('-')[0]]
        obj["dd"] = dd.replace('-', '/')
        obj["rd"] = rd.replace('-', '/')
        obj["tvlr"] = {"v": tvlr, "adt": tvlr.split('-')[0], "chd": tvlr.split('-')[1], "inf": tvlr.split('-')[2]}
        obj["cl"] = cl
        print(obj)
        # TODO: Send this json object to App.js
    except:
        return jsonify({
            'status':404, 'message': "Incorrect api call",
            'exampleAPI': "/easemytrip/from=DEL-Delhi-India&to=BOM-Mumbai-India&dd=30-07-2020&rd=null&tvlr=1-0-0&cl=0"
        }), 404
        
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
# https://flight.easemytrip.com/FlightList/Index?srch=DEL-Delhi-India|BOM-Mumbai-India|30/07/2020&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lng=&