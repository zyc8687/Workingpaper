from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver import ActionChains
import time


web = Chrome()

web.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')

#要定位的标签在iframe标签之中 需要先定位到iframe页面
web.switch_to.frame('iframeResult')
webIframe = web.find_element(By.ID,'draggable')

#拖动动作
action = ActionChains(web)
action.click_and_hold(webIframe)

for i in range(5):
    #横着移动17个像素 对应的是X与Y的关系  .perfrom()执行的意思
    action.move_by_offset(50,0).perform()
    sleep(0.3)

#释放拖拽动作
action.release()
print(webIframe)

web.quit()