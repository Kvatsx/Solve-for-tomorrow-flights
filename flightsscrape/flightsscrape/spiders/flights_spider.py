import scrapy

class FlightsSpider(scrapy.Spider):
    name = "easemytrip"

    start_urls = [
        'https://flight.easemytrip.com/FlightList/Index?srch=DEL-Delhi-India|BOM-Mumbai-India|07/07/2020&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lng=&'
        # 'https://www.expedia.co.in/Flights-Search?flight-type=on&mode=search&trip=roundtrip&leg1=from%3ADelhi+%28DEL-Indira+Gandhi+Intl.%29%2Cto%3AGoa+%28GOI-Dabolim%29%2Cdeparture%3A01%2F07%2F2020TANYT&options=cabinclass%3Aeconomy&leg2=from%3AGoa+%28GOI-Dabolim%29%2Cto%3ADelhi+%28DEL-Indira+Gandhi+Intl.%29%2Cdeparture%3A02%2F07%2F2020TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY&fromDate=01%2F07%2F2020&toDate=02%2F07%2F2020&d1=2020-07-01&d2=2020-07-02'
    ]

    def parse(self, response):
        # filename = 'expedia-temp.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # print("Response", response.xpath('//*[@id="flightModuleList"]//li[@data-test-id]'))
        for item in response.xpath('//*[@id="ResultDiv"]/div/div/div[3]'):
            yield {
                'flightName': item.xpath('//*[@id="ResultDiv"]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/div/div[2]/span[1]').get(),
                # 'date': post.css('.post-header a::text')[1].get(),
                # 'author': post.css('.post-header a::text')[2].get()
            }
            print("item", item)
        # next_page = response.css('a.next-posts-link::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
# //*[@id="flight-module-2020-07-01t11:40:00+05:30-coach-del-goi-6e-367_2020-07-02t15:30:00+05:30-coach-goi-del-6e-637_"]