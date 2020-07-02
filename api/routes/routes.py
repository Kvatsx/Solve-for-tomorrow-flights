from flask import Blueprint, jsonify
from flask_cors import CORS

from api.database import mongo
import json, requests

# test link
# http://127.0.0.1:5000/api/easemytrip/from=DEL-Delhi-India&to=BOM-Mumbai-India&dd=2020-07-07&rd=null&tvlr=1-0-0&cl=0&isdm=true&isow=true&airline=undefined

mod = Blueprint('main', __name__)
CORS(mod)
# /easemytrip/from=<fr>&to=<to>&dd=<dd>&rd=<rd>&tvlr=<tvlr>&cl=<cl>
@mod.route('/easemytrip/from=<fr>&to=<to>&dd=<dd>&rd=<rd>&tvlr=<tvlr>&cl=<cl>&isdm=<isdm>&isow=<isow>&airline=<airline>', methods=['GET'])
def index(fr, to, dd, rd, tvlr, cl, isdm, isow, airline):
    if fr == "" or to == "" or dd == "" or len(tvlr) != 5 or cl == "":
        return jsonify({
            'status':404, 'message': "Incorrect api call",
            'exampleAPI': "/api/easemytrip/from=DEL-Delhi-India&to=BOM-Mumbai-India&dd=2020-07-07&rd=null&tvlr=1-0-0&cl=0&isdm=true&isow=true&airline=undefined"
        }), 404
    try :
        obj = {}
        obj["origin"] = fr.split('-')[0]
        obj["destination"] = to.split('-')[0]
        obj["adults"] = tvlr.split('-')[0]
        obj["children"] = tvlr.split('-')[1]
        obj["infants"] = tvlr.split('-')[2]
        obj["departureDate"] = dd
        obj["arrivalDate"] = rd
        obj["isDomestic"] = isdm
        obj["isOneway"] = isow
        obj["airline"] = airline
        obj['cabin'] = cl
        obj["currencyCode"] = "INR"
        obj = fetchFlights(obj)
        print(obj)
    except:
        return jsonify({
            'status':404, 'message': "Incorrect api call",
            'exampleAPI': "/api/easemytrip/from=DEL-Delhi-India&to=BOM-Mumbai-India&dd=30-07-2020&rd=null&tvlr=1-0-0&cl=0&isdm=true&isow=true&airline=undefined"
        }), 404

    return jsonify(obj), 200


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

def fetchFlights(obj):
    headers = {
        'authority': 'flightservice.easemytrip.com',
        'accept': 'application/json, text/plain, */*',
        'access-control-allow-orgin': '*',
        'access-control-allow-headers': 'X-Requested-With',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'access-control-max-age': '1728000',
        'content-type': 'application/json',
        'origin': 'https://flight.easemytrip.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://flight.easemytrip.com/FlightList/Index?srch=DEL-Delhi-India|BOM-Mumbai-India|10/07/2020&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lng=&',
        'accept-language': 'en-US,en;q=0.9',
    }

    data = '{"org":"'+ obj['origin'] +'","dept":"'+ obj['destination'] +'","adt":"'+ obj['adults'] +'","chd":"'+ obj['children'] +'","inf":"'+ obj['infants'] +'","deptDT":"'+ obj['departureDate'] +'","arrDT":"'+ obj['arrivalDate'] +'","isDomestic":"'+ obj['isDomestic'] +'","isOneway":'+ obj['isOneway'] +',"airline":"'+ obj['airline'] +'","Cabin":"'+ obj['cabin'] +'","currCode":"'+ obj['currencyCode'] +'","appType":1,"isSingleView":false,"ResType":1,"CouponCode":"","IpAddress":"","userid":"","UUID":""}'
    # data = '{"org":%s,"dept":{},"adt":{},"chd":{},"inf":{},"deptDT":{},"arrDT":{},"isDomestic":{},"isOneway":{},"airline":{},"Cabin":{},"currCode":{},"appType":1,"isSingleView":false,"ResType":1,"CouponCode":"","IpAddress":"","userid":"","UUID":""}'.format(obj['origin'], obj['destination'], obj['adults'], obj['children'], obj['infants'], obj['departureDate'], obj['arrivalDate'], obj['isDomestic'], obj['isOneway'], obj['airline'],  obj['cabin'], obj['currencyCode'])
    # print(data)

    response = requests.post('https://flightservice.easemytrip.com/EmtAppService/AirAvail_Lights/AirSearchLightFromCloud', headers=headers, data=data)
    # json.dump(response.json(), open("data.json", 'w'))
    print(data)
    return showRelevantInfo(response.json())

def showRelevantInfo(data):
    locationDetails = data['A']
    flightNames = data['C']
    locationAndCountryMap = data['Cnty']
    flightList = {}
    index = 0
    flightList['from'] = data['SQ'][0]['org']
    flightList['to'] = data['SQ'][0]['dept']
    flightList['departureData'] = data['SQ'][0]['deptDT']
    flightList['returnDate'] =  data['SQ'][0]['arrDT']
    flightList['traveller'] = {
        'adult': data['adt'],
        'child': data['chd'],
        'infant': data['inf']
    }
    flightList['cashCurrency'] = data['CC']
    flightList['offers'] = data['OFR']
    docs=[]

    for flight in range(len(data['j'][0]['s'])):
        obj = {}
        obj['flightName'] = flightNames[data['dctFltDtl'][str(data['j'][0]['s'][flight]['b'][0]['FL'][0])]['AC']]
        obj['from']=data['SQ'][0]['org']
        obj['to'] = data['SQ'][0]['dept']
        obj['departureDate']= data['SQ'][0]['deptDT']
        obj['arrivalDate']= data['SQ'][0]['arrDT']
        obj['depart'] = data['dctFltDtl'][str(data['j'][0]['s'][flight]['b'][0]['FL'][0])]['DTM']
        obj['duration'] = data['j'][0]['s'][flight]['b'][0]['JyTm']
        # obj['arrive'] = data.dctFltDtl[data.j[0].sflight.b[0].FL.length-1].ATM
        obj['previousPrice'] =  data['j'][0]['s'][flight]['TF']
        obj['finalPrice'] =  data['j'][0]['s'][flight]['TTDIS']
        obj['couponCode'] =  data['j'][0]['s'][flight]['CC']
        if obj['couponCode'] != "":
            obj['couponName'] =  data['j'][0]['s'][flight]['CpNt']
        obj['Meal'] =  data['j'][0]['s'][flight]['Rmk']
        obj['Stops'] = data['dctFltDtl'][str(data['j'][0]['s'][flight]['b'][0]['FL'][0])]['STP']
        docs.append(obj)

    flightList['flights'] = docs;
    return flightList

# def getDataFromNode(obj):
#     payload = "{\"origin\": \""+obj['origin']+"\",\"destination\":\""+obj['destination']+"\",\"departureDate\":\""+obj['departureDate']+"\",\"arrivalDate\": "+obj['arrivalDate']+",\"adults\":\""+obj['adults']+"\",\"children\":\""+obj['children']+"\",\"infants\":\""+obj['infants']+"\",\"isDomestic\":\""+obj['isDomestic']+"\",\"isOneway\":\""+obj['isOneway']+"\",\"airline\":\""+obj['airline']+"\",\"cabin\":\""+obj['cabin']+"\",\"currencyCode\":\""+obj['currencyCode']+"\"}"
#     headers = {
#         'Content-Type': 'application/json'
#     }
#     print(payload)
    # url = "https://flights-easemytrip.herokuapp.com/getFlights"
#   # url = "http://127.0.0.1:2345/getFlights"
#     response = requests.request("POST", url, data=payload, headers=headers) # https://flights-easemytrip.herokuapp.com/getFlights
#     return response.json()
# https://flight.easemytrip.com/FlightList/Index?srch=DEL-Delhi-India|BOM-Mumbai-India|30/07/2020&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lng=&
