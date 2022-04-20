import re

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver import ActionChains

from time import sleep
''' seleinum 隐形等待的包'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium import webdriver
import random
''' 键盘输入包 '''
from selenium.webdriver.common.keys import Keys
class TaoBao_crwl:
    #初始化对象
    def __init__(self):
        url  = 'https://login.taobao.com/member/login.jhtml'
        self.url=url
        options = webdriver.ChromeOptions()
        ''' 让浏览器不识别被控制 '''
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser,10) #设置隐形等待时间

    #登录淘宝
    def Login(self):
        #打开网页
        self.browser.get(self.url)
        #等待密码输入框加载
        self.wait.until(ec.presence_of_element_located((By.ID,"fm-login-id")))
        #使用支付宝扫码登录
        self.browser.find_element_by_class_name('alipay-login').click()
        sleep(7)

        nick_name = self.wait.until(ec.presence_of_element_located((By.XPATH,'//*[@id="J_SiteNavLogin"]/div[1]/div/a'))).text
        print(nick_name)
        self.browser.find_element_by_xpath('//*[@id="J_SiteNavHome"]/div/a/span').click()

        input_search = self.wait.until(ec.presence_of_element_located((By.ID,"q")))

        # 清除输入框上的文字
        input_search.clear()

        # input_search.send_keys('联想手机')
        # self.browser.find_element_by_class_name('btn-search tb-bg').click()
        #输入文字回车键搜索
        input_search.send_keys('联想手机',Keys.ENTER)


    #获取列表页页数
    def Get_List_Pages(self):
        pages = self.browser.find_element(By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > div.total").text
        page = re.findall('[^\d]*(\d+)[^\d]*',pages)
        return page[0]


    def Get_Commodity(self,page_number):
        # for pages in range(1,int(page_number)):
        for pages in range(1,3):
            commodity_item = self.browser.find_elements_by_class_name('J_MouserOnverReq')
            for commoditys in commodity_item:
                price = commoditys.find_element_by_class_name('price').text
                name = commoditys.find_element_by_class_name('shop').text
                address = commoditys.find_element_by_class_name('location').text
                print('价格：%s，是掌柜%s的，由%s发货'%(price,name,address))
            #列表页面设置随机滑动次数
            num = random.randint(1,4)
            self.Swip_Down(num)

            #翻页
            next_url = 'https://s.taobao.com/search?q=联想手机&s='+str(44*pages)
            print('现在爬取的是第%s页，%s'%(pages,next_url))
            self.browser.get(next_url)



    #模拟人滚动滑轮
    def Swip_Down(self,second):
        for i in range(second):
            randsum = random.randint(50,200)
            ruadslep = random.randint(0,1)
            #js滑动滑轮
            js = 'var q=document.documentElement.scrollTop='+str(214+randsum*i)
            self.browser.execute_script(js)
            sleep(0.5)
            js = 'var q=document.documentElement.scrollTop=' + str(721+randsum * i)
            self.browser.execute_script(js)
            sleep(0.9)
            js = 'var q=document.documentElement.scrollTop=' + str(1024+randsum*i)
            self.browser.execute_script(js)
            sleep(1.5)
            js = 'var q=document.documentElement.scrollTop=' + str(2634+randsum*i)
            self.browser.execute_script(js)
            sleep(1.5)

            #使滑轮滑到底部
            js = 'var q=document.documentElement.scrollTop=100000'
            self.browser.execute_script(js)
            sleep(ruadslep)



if __name__ == '__main__':
    a = TaoBao_crwl()
    a.Login()
    page_number = a.Get_List_Pages()
    print(page_number)
    a.Get_Commodity(page_number)
