import scrapy
import re
import openpyxl as op
import copy
from urllib import parse




class GppSpider(scrapy.Spider):
    name = 'gpp'
    allowed_domains = ['www.3gpp.org']
    # start_urls = [
    #         'https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_116-e/Inbox/Drafts',
    #               ]
    start_urls = ['https://www.3gpp.org/ftp/tsg_ran/WG2_RL2/TSGR2_119bis-e/Inbox/Drafts']

    '''count leader'''
    # def parse(self, response):
    #     links = response.xpath('//tbody//td//a/@href').getall()
    #     item = {}
    #     for link in links:
    #         link = parse.unquote(link)
    #
    #         topic = re.sub('.+\/','',link)
    #         save_topic = re.sub('[^a-zA-Z]\(.+','',link)
    #         save_topic = re.sub('.+Drafts/','',save_topic)
    #         save_topic = re.sub('.+]/','',save_topic)
    #         save_topic = re.sub('.+]/','',save_topic)
    #         if '(' in topic:
    #             topic= re.sub('[^a-zA-Z\)]+$','',topic)
    #             gs_names = re.findall('\(([^\)]+)\)?$',topic)
    #             gs_name = gs_names[0]
    #         else:
    #             backups=topic
    #             topic = re.sub('\s.+', '', topic)
    #             gs_names = re.findall('.+(\d{3})\]',topic)
    #             if len(gs_names)>0:
    #                 gs_name = gs_names[0]
    #             else:
    #                 gs_name=backups
    #         print(gs_name,'>>',topic)
    #         item['topic'] = save_topic
    #         item['name'] = gs_name
    #         # print(item)
    #         yield item





    ''' 统计公司名字 '''
    def parse(self, response):
        links = response.xpath('//tbody//td//a/@href').getall()
        for link in links:
            # link = parse.unquote(link)
            '''判断列表页是否为.doc结尾'''
            detail_link = re.findall('.+[\s\-\_]{1}(.+)\.[docxrazip]{3,4}',link)
            if detail_link[0:2]:
                pass
            else:

                yield scrapy.Request(link, callback=self.get_document)
        # link = 'https://www.3gpp.org/ftp/tsg_ran/WG3_Iu/TSGR3_117bis-e/Inbox/Drafts/CB%20%23%2010_R17MBS2_F1E1'
        # yield scrapy.Request(link, callback=self.get_document)





    def get_document(self, response):
        item = {}
        urls = response.xpath('//tbody//tr/td/a/@href').getall()
        doc_time = response.xpath('//tbody//tr/td[3]//text()').getall()
        re_doc = re.compile('.+[\s\-\_]{1}(.+)\.[docxrazip]{3,4}', re.I)
        re_time = re.compile('[^\d]+(\d{4}\/\d{2}\/\d{2}).*')
        for url,time in zip(urls,doc_time):
            # urls = parse.unquote(url)
            # docurl = urls.replace('%', '-')
            # docurl = docurl.replace('(', '/')
            # docurl = docurl.replace(')', '')
            name = re_doc.findall(url)
            time = re_time.findall(time)
            if len(name) > 0:
                # '''判断是否计数文件'''
                '''显示路径'''
                # _document = re.compile('https.+\.[a-z]{3,15}$', re.I)
                # doument = _document.findall(url)
                # doument = parse.unquote(doument[0])
                # item['paths'] = doument

                CompanyName = re.sub("\d+", '', name[0], re.I)
                item['name'] = CompanyName
                item['time'] = time
                yield item
                # print(item)


            else:
                '''嵌套文件处理'''
                _document = re.compile('https.+\.[a-z]{3,15}$', re.I)
                doument = _document.findall(url)
                if len(doument) > 0:
                    pass
                else:
                    yield scrapy.Request(url, callback=self.get_document)
                    yield item




    ''' 一次会分TOPIC '''
    # def parse(self, response):
    #     links = response.xpath('//tbody//td//a/@href').getall()
    #     item = {}
    #     for link in links:
    #         catalog = re.sub('.+\/','',link)
    #         docurl = catalog.replace('%20', ' ')
    #         docurl = docurl.replace('%5B', '[')
    #         docurl = docurl.replace('%2B', '+')
    #         docurl = docurl.replace('%5D', ']')
    #         docurl = docurl.replace('%23', '#')
    #         docurl = docurl.replace('%26', '&')
    #         docurl = docurl.replace('%2C', ',')
    #         docurl = docurl.replace('%24', '$')
    #         docurl = docurl.replace('%3D', '=')
    #         # catalog = re.sub('\s.+','',docurl)
    #         # catalogs = re.findall('.+(\d{3})\].+',docurl)
    #
    #
    #         # catalogss = catalog if len(catalogs) == 0 else catalogs[0]
    #         # catalogss = re.sub('\[','',catalogss)
    #         # catalogss = re.sub('\]','',catalogss)
    #
    #         item["subject"] = docurl
    #
    #         yield scrapy.Request(link, callback=self.get_document,meta={'item': copy.deepcopy(item)})
    #
    # def get_document(self, response):
    #     item = response.meta['item']
    #     urls = response.xpath('//tbody//tr/td/a/@href').getall()
    #     _document = re.compile('https.+\.[xlsdoczipraft]{3,4}', re.I)
    #
    #
    #     wendang = re.compile('\/[^\/]+\.[xlsdoczipraft]{3,4}', re.I)
    #     # wendang = re.compile('.+[\s\-\_]{1}(.+)\.[docxzip]{3,4}', re.I)
    #     for url in urls:
    #
    #         doument = _document.findall(url)
    #
    #         if len(doument) > 0:
    #             docurl = url.replace('%20', ' ')
    #             docurl = docurl.replace('%5B', '[')
    #             docurl = docurl.replace('%2B', '+')
    #             docurl = docurl.replace('%5D', ']')
    #             docurl = docurl.replace('%23', '#')
    #             docurl = docurl.replace('%26', '&')
    #             docurl = docurl.replace('%2C', ',')
    #             docurl = docurl.replace('%24', '$')
    #             docurl = docurl.replace('%3D', '=')
    #             name = wendang.findall(docurl)
    #             docl = name[0]
    #             company_list = re.findall('.+[^a-zA-Z0-9]{1}(.+)\.[xlsdocziepraft]{3,4}', docl, re.I)
    #
    #             item['path']=docl
    #             item['name'] = company_list[0]
    #             # print('=====',docl,company_list[0])
    #             # print('=====',url)
    #             yield item
    #
    #         else:
    #
    #             yield scrapy.Request(url, callback=self.get_document,meta={'item': copy.deepcopy(item)})
    #             yield item
