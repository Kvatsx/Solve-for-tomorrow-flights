const fetch = require("node-fetch");

async function getFlights(org, dept, deptDt, arrDt) {

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
        "referrer": "https://flight.easemytrip.com/FlightList/Index?srch=DEL-Delhi-India|BOM-Mumbai-India|07/07/2020&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lng=&",
        "referrerPolicy": "no-referrer-when-downgrade",
        "body": "{\"org\":\""+ org + "\",\"dept\":\"" + dept +"\",\"adt\":\"1\",\"chd\":\"0\",\"inf\":\"0\",\"deptDT\":\""+ deptDt + "\",\"arrDT\":" + arrDt +",\"isDomestic\":\"true\",\"isOneway\":true,\"airline\":\"undefined\",\"Cabin\":\"0\",\"currCode\":\"INR\",\"appType\":1,\"isSingleView\":false,\"ResType\":1,\"CouponCode\":\"\",\"IpAddress\":\"\",\"userid\":\"\",\"UUID\":\"\"}",
        "method": "POST",
        "mode": "cors"
    })
    response.status     //=> number 100–599
    response.statusText //=> String
    console.log(response.status + " " + response.statusText)

    let data = await response.json()
    return data;
}

// function main() {
    // var result;
    getFlights("DEL", "BOM", "2020-07-07", null).then(data => {
        console.log(data);
        // result = data;
    });
    // return result
// }

// console.log(main());
