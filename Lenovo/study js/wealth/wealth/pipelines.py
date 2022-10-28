# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class WealthPipeline:
    def open_spider(self, spider):
        self.conn = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            password='111111',
            db='ces_demo',
            charset='utf8',
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'insert into ces_demo.dfcf(name,price,code,price_limit,trading_turnover,trading_volume,ampl,max_price,mini_price,yesterday_price,quantity_ratio,turnover_rate,PE,PB,plate,list_key,todays,md5) ' \
              'values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'

        self.query_sql = """SELECT * FROM ces_demo.dfcf WHERE md5='{}'"""
        self.cursor.execute(self.query_sql.format(item['md5']))

        ret = self.cursor.fetchone()
        if ret:
            print('kzz数据重复:{}'.format(item['name']))
        else:
            self.cursor.execute(
                sql % (
                    item['name'],
                    item['price'],
                    item['code'],
                    item['price_limit'],
                    item['trading_turnover'],
                    item['trading_volume'],
                    item['ampl'],
                    item['max_price'],
                    item['mini_price'],
                    item['yesterday_price'],
                    item['quantity_ratio'],
                    item['turnover_rate'],
                    item['PE'],
                    item['PB'],
                    item['plate'],
                    item['list_key'],
                    item['todays'],
                    item['md5'],

                )

            )
            self.conn.commit()  # 提交
            print('数据插入成功')
        return item

        # ''' 数据库字段和item字段名称一样自动生成 '''
        # keys = item.keys()
        # values = list(item.values())
        # sql = "insert into ces_demo.baowen({})values({})".format(
        #     ','.join(keys),
        #     ','.join(['%s']*len(values))
        # )
        # self.cursor.execute(sql,values)
        # self.conn.commit()
        # return item

    def close_spider(self, spider):
        self.cursor.close()  # 关闭游标
        self.conn.close()  # 关闭数据库
