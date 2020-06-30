const fetch = require("node-fetch");
const MongoClient = require('mongodb').MongoClient
const DB=require('./config.json').DB
const fs = require('fs');
const app=require('express')();

let flightcollection=null;

async function getFlights(req_data) {

    let response = await fetch("https://flightservice.easemytrip.com/EmtAppService/AirAvail_Lights/AirSearchLightFromCloud", {
        "headers": {
          "accept": "application/json, text/plain, */*",
          "accept-language": "en-US,en;q=0.9",
          "access-control-allow-headers": "X-Requested-With",
          "access-control-allow-orgin": "*",
          "access-control-max-age": "1728000",
          "content-type": "application/json",
          "sec-fetch-dest": "empty",
          "sec-fetch-mode": "cors",
          "sec-fetch-site": "same-site"
      },
      "referrer": "https://flight.easemytrip.com/FlightList/Index?srch=DEL-Delhi-India|BOM-Mumbai-India|07/07/2020&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lng=&CouponCode=",
      "referrerPolicy": "no-referrer-when-downgrade",
      "body": "{\"org\":\"DEL\",\"dept\":\"HYD\",\"adt\":\"1\",\"chd\":\"0\",\"inf\":\"0\",\"deptDT\":\"2020-07-07\",\"arrDT\":null,\"isDomestic\":\"true\",\"isOneway\":true,\"airline\":\"undefined\",\"Cabin\":\"0\",\"currCode\":\"INR\",\"appType\":1,\"isSingleView\":false,\"ResType\":1,\"CouponCode\":\"\",\"IpAddress\":\"\",\"userid\":\"\",\"UUID\":\"\"}",
      "method": "POST",
      "mode": "cors",
      "credentials": "omit"
  });
    console.log(response.status + " " + response.statusText)

    let data = await response.json()

    return data;
}

function showRelevantInfo(data) {
    // console.log(data);

    var locationDetails = data.A;
    var flightNames = data.C;
    var locationAndCountryMap = data.Cnty;
    var flightList = {};
    var index = 0;
    flightList['from'] = data.SQ[0].org;
    flightList['to'] = data.SQ[0].dept;
    flightList['departureData'] = data.SQ[0].deptDT;
    flightList['returnDate'] =  data.SQ[0].arrDT;
    flightList['traveller'] = {
        adult: data.adt,
        child: data.chd,
        infant: data.inf
    }
    flightList['cashCurrency'] = data.CC;
    flightList['offers'] = data.OFR;
    docs=[]

    for (flight in data.j[0].s) {
        var obj = {};
        obj['flightName'] = flightNames[data.dctFltDtl[data.j[0].s[flight].b[0].FL[0]].AC];
        obj['departureDate']= data.SQ[0].deptDT
        obj['arrivalDate']= data.SQ[0].arrDT
        obj['depart'] = data.dctFltDtl[data.j[0].s[flight].b[0].FL[0]].DTM;
        obj['duration'] = data.j[0].s[flight].b[0].JyTm;
        obj['arrive'] = data.dctFltDtl[data.j[0].s[flight].b[0].FL.length-1].ATM;
        obj['previousPrice'] = data.j[0].s[flight].TF;
        obj['finalPrice'] = data.j[0].s[flight].TTDIS;
        obj['couponCode'] = data.j[0].s[flight].CC;
        obj['couponName'] = data.j[0].s[flight].CpNt;
        obj['Meal'] = data.j[0].s[flight].Rmk;
        obj['Stops'] = data.dctFltDtl[data.j[0].s[flight].b[0].FL[0]].STP;

        docs.push(obj);
    }

    console.log(docs);
    console.log(docs.length)

    
    return docs;
}





app.get('/getFlights',function(req,res){
    MongoClient.connect(DB.URI, function(err,db){
    if(err)
        throw err;

    flightcollection=db.db('test').collection('easemytrip_node');
    getFlights(req.query).then(function(data){
        let docs= showRelevantInfo(data);
        flightcollection.insertMany(docs).then(result=>{
            console.log("Saved to DB!");
            res.send("Result saved in DB!");
        }).catch(err=>{
            res.send(err);
        });
    })
    })  
})

app.get('/',function(req,res){
    res.send('Hey there!')
})

app.listen(2345, ()=>{
    console.log('Connected to node server');
    
})

//JSON request parameter format
// {
//     "origin": "DEL",
//     "destination":"BOM",
//     "departureDate":"2020-07-07",
//     "arrivalDate": null,
//     "adults":"1",
//     "children":"0",
//     "infants":"0",
//     "isDomestic":"true",
//     "isOneway":"true",
//     "airline":"undefined",
//     "cabin":"0",
//     "currencyCode":"INR",
// }
