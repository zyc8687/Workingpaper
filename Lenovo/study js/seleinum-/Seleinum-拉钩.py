from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

web = Chrome()

web.get('https://www.lagou.com/')


#选择输入框 输入文字
# el = web.find_element(By.XPATH,'//*[@id="kw"]').send_keys('爬虫')
#点击搜索框
web.find_element(By.XPATH,'//*[@id="changeCityBox"]/p[1]/a').click()

time.sleep(1)

#选择输入框  输入文字 点击回车键
sercah = web.find_element(By.XPATH,'//*[@id="search_input"]').send_keys('爬虫',Keys.ENTER)

time.sleep(1)

elements = web.find_elements(By.XPATH,"//div[@class='list__YibNq']/div")
for element in elements:
    name = element.find_element(By.XPATH,".//div[@class='company-name__2-SjF']//a").text
    position = element.find_element(By.XPATH,".//div[@class='p-top__1F7CL']//a").text
    pay = element.find_element(By.XPATH,".//div[@class='p-bom__JlNur']").text
    print(position,'====',name,'===',pay)



