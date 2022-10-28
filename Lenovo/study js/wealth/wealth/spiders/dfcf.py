import scrapy
import json
import jsonpath,re
from wealth.items import WealthItem
import datetime
import hashlib


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
                        for t, h in zip(title, href):
                            plate_coding = re.findall('.+(BK\d+)', h)
                            if plate_coding:
                                dates = datetime.datetime.now()
                                todays = re.sub('\s.+', '', str(dates))
                                # print(t, plate_coding)
                                every_plate_url = 'http://49.push2.eastmoney.com/api/qt/clist/get?&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=b:{}+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152,f45&_=1652938670435'.format(plate_coding[0])
                                # print('板块:',t,'url:',every_plate_url)
                                item = WealthItem()
                                item['plate'] = t
                                item['list_key'] = plate_coding[0]
                                item['todays'] = todays
                                yield scrapy.Request(url=every_plate_url, callback=self.get_every_plate_url,meta={'item':item},dont_filter=True)



    def get_every_plate_url(self, response):
        # print('====',response.body_as_unicode())
        '''处理页面json'''
        list_page_response = response.text
        list_page_response = re.sub('jQuery.+?\(', '', list_page_response)
        list_page_response = re.sub('\);', '', list_page_response)
        stock_list = json.loads(list_page_response)
        '''获取每个板块的总页数'''
        totals = jsonpath.jsonpath(stock_list, '$..total')
        total = int(totals[0])/20
        total = re.sub('\.0$','',str(total))
        if '.' in total:
            numb = re.sub('\.\d+','',total)
            numb = 1+int(numb)
        else:
            numb = int(total)

        for i in range(numb):
            item = response.meta['item']
            list_page_url = re.sub('pn=\d+', 'pn={}'.format(i+1),response.url)
            # print('详情页url',list_page_url)
            yield scrapy.Request(url=list_page_url, callback=self.parse_list_page, meta={'item': item},dont_filter=True)

    def cheaker_date(self,c):
        res = re.findall('\d{0,5}\-?[\.\d]+', str(c))
        if res:
            return c
        else:
            return 0.0



    def parse_list_page(self,response):
        '''处理页面json'''
        list_page_response = response.text
        list_page_response = re.sub('jQuery.+?\(', '', list_page_response)
        list_page_response = re.sub('\);', '', list_page_response)
        stock_list = json.loads(list_page_response)
        '''获取数据'''
        name = jsonpath.jsonpath(stock_list, '$..diff..f14')
        price = jsonpath.jsonpath(stock_list, '$..diff..f2')
        code = jsonpath.jsonpath(stock_list, '$..diff..f12')
        price_limit = jsonpath.jsonpath(stock_list, '$..diff..f3')
        trading_turnover = jsonpath.jsonpath(stock_list, '$..diff..f4')
        trading_volume = jsonpath.jsonpath(stock_list, '$..diff..f5')
        ampl = jsonpath.jsonpath(stock_list, '$..diff..f7')
        max_price = jsonpath.jsonpath(stock_list, '$..diff..f15')
        mini_price = jsonpath.jsonpath(stock_list, '$..diff..f16')
        yesterday_price = jsonpath.jsonpath(stock_list, '$..diff..f17')
        quantity_ratio = jsonpath.jsonpath(stock_list, '$..diff..f10')
        turnover_rate = jsonpath.jsonpath(stock_list, '$..diff..f8')
        PE = jsonpath.jsonpath(stock_list, '$..diff..f9')
        PB = jsonpath.jsonpath(stock_list, '$..diff..f23')

        for name,price,code,price_limit,trading_turnover,trading_volume,ampl,max_price,mini_price,yesterday_price,quantity_ratio,turnover_rate,PE, PB \
                in zip(name,price,code,price_limit,trading_turnover,trading_volume,ampl,max_price,mini_price,yesterday_price,quantity_ratio,turnover_rate,PE, PB):
            item = response.meta['item']
            item['name']=name
            item['price']=self.cheaker_date(price)
            item['code']=code
            item['price_limit']=self.cheaker_date(price_limit)
            item['trading_turnover']=self.cheaker_date(trading_turnover)
            item['trading_volume']=self.cheaker_date(trading_volume)
            item['ampl']=self.cheaker_date(ampl)
            item['max_price']=self.cheaker_date(max_price)
            item['mini_price']=self.cheaker_date(mini_price)
            item['yesterday_price']=self.cheaker_date(yesterday_price)
            item['quantity_ratio']=self.cheaker_date(quantity_ratio)
            item['turnover_rate']=self.cheaker_date(turnover_rate)
            item['PE']=self.cheaker_date(PE)
            item['PB']=self.cheaker_date(PB)
            check_md5 = item['code']+item['todays']
            item['md5'] = hashlib.md5(check_md5.encode(encoding='utf-8')).hexdigest()
            yield item

