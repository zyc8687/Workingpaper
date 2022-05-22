import scrapy
import json
import jsonpath,re
from wealth.items import WealthItem


class DfcfSpider(scrapy.Spider):
    name = 'dfcf'
    # allowed_domains = ['quote.eastmoney.com']
    start_urls = ['http://quote.eastmoney.com/center/api/sidemenu.json']

    def parse(self, response):
        one_plate_list = json.loads(response.text)
        for one_plate in one_plate_list:
            if '沪深京板块' in one_plate['title']:
                for two_plate in one_plate['next']:
                    if '行业板块' in two_plate['title']:
                        title = jsonpath.jsonpath(two_plate, '$..title')
                        href = jsonpath.jsonpath(two_plate, '$..href')
                        href = href[0:4]
                        for t, h in zip(title, href):
                            plate_coding = re.findall('.+(BK\d+)', h)
                            if plate_coding:
                                print(t, plate_coding)
                                list_page_href = 'http://49.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112409060092406792142_1652939226224&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=b:{}+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152,f45&_=1652938670435'.format(plate_coding[0])
                                # print(list_page_href)
                                item = WealthItem()
                                item['plate'] = t
                                item['list_key'] = plate_coding
                                yield scrapy.Request(url=list_page_href, callback=self.parse_list_page)


    def parse_list_page(self, response):
        print(response.text)
        # list_page_response = response.text
        # list_page_response = re.sub('jQuery.+?\(', '', list_page_response)
        # list_page_response = re.sub('\);', '', list_page_response)

        # stock_list = json.loads(list_page_response)
        # for stock_js in stock_list:
        # print('==========',type(response))
            # item = response.meta['item']
            # name = jsonpath.jsonpath(stock_list, '$..diff..f14')
            # price = jsonpath.jsonpath(stock_list, '$..diff..f2')
            # code = jsonpath.jsonpath(stock_list, '$..diff..f12')
            # price_limit = jsonpath.jsonpath(stock_list, '$..diff..f3')
            # trading_turnover = jsonpath.jsonpath(stock_list, '$..diff..f4')
            # trading_volume = jsonpath.jsonpath(stock_list, '$..diff..f5')
            # ampl = jsonpath.jsonpath(stock_list, '$..diff..f7')
            # max_price = jsonpath.jsonpath(stock_list, '$..diff..f15')
            # mini_price = jsonpath.jsonpath(stock_list, '$..diff..f16')
            # yesterday_price = jsonpath.jsonpath(stock_list, '$..diff..f17')
            # quantity_ratio = jsonpath.jsonpath(stock_list, '$..diff..f10')
            # turnover_rate = jsonpath.jsonpath(stock_list, '$..diff..f8')
            # PE = jsonpath.jsonpath(stock_list, '$..diff..f9')
            # PB = jsonpath.jsonpath(stock_list, '$..diff..f23')
            # for name,price,code ,price_limit,trading_turnover,trading_volume,ampl,max_price,mini_price,yesterday_price,quantity_ratio,turnover_rate,PE, PB \
            #         in zip(name,price,code ,price_limit,trading_turnover,trading_volume,ampl,max_price,mini_price,yesterday_price,quantity_ratio,turnover_rate,PE, PB):
            #     item['name']=name
            #     item['price']=price
            #     item['code']=code
            #     price_item['limit']=limit
            #     trading_item['turnover']=turnover
            #     trading_item['volume']=volume
            #     item['ampl']=ampl
            #     max_item['price']=price
            #     mini_item['price']=price
            #     yesterday_item['price']=price
            #     quantity_item['ratio']=ratio
            #     turnover_item['rate']=rate
            #     item['PE']=PE
            #     item['PB']=PB
            #     print(item)
