from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

web = Chrome(r"C:\Users\BZ\Downloads\chromedriver_win32\chromedriver.exe")

web.get('https://www.lagou.com/')


#选择输入框 输入文字
# el = web.find_element(By.XPATH,'//*[@id="kw"]').send_keys('爬虫')
#点击搜索框
web.find_element(By.XPATH,'//*[@id="changeCityBox"]/p[1]/a').click()

time.sleep(1)

#选择输入框  输入文字 点击回车键
sercah = web.find_element(By.XPATH,'//*[@id="search_input"]').send_keys('爬虫',Keys.ENTER)

time.sleep(1)

web.find_element(By.XPATH,'//*[@id="jobList"]/div[1]/div[1]/div[1]/div[1]/div[1]').click()
#进入到详情页面提取
#切换到窗口  -1最后一个窗口
web.switch_to.window(web.window_handles[-1])
href = web.find_element(By.XPATH,'//*[@id="job_detail"]/dd[2]/div').text
print(href)
#关闭窗口
web.close()

web.switch_to.window((web.window_handles[0]))

