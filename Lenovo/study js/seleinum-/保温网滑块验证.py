import re
import webbrowser
import requests
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from io import BytesIO
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
import time
import random


''' 下载缺口图片和完整图片 '''
def get_image(driver,div_class,name):
    bg_imgs = driver.find_elements_by_class_name(div_class)
    img_url=''
    location_list = []
    ''' 获取52个图片的xy位置 '''
    for img in bg_imgs:
        img_url = re.findall(r'.+url\("([^"]+)"\);.+',img.get_attribute('style'))[0]
        location={}
        location['x'] = re.findall(r'.+background-position: (.*?)px (.*?)px;',img.get_attribute('style'))[0][0]
        location['y'] = re.findall(r'.+background-position: (.*?)px (.*?)px;',img.get_attribute('style'))[0][1]
        # print('>>>',img_url,location['x'],location['y'])
        location_list.append(location)


    print('img_url》》',img_url)
    response = requests.get(img_url).content
    image_content = BytesIO(response)
    # image.show()
    image = get_merge_image(image_content,location_list,name)
    image.save('{}.jpg'.format(name))
    return image


def get_merge_image(image_content,location_list,name):
    '''拼接图片'''
    print('进入拼接图片函数')
    image = Image.open(image_content)
    image_list_tp = []
    image_list_down = []
    for location in location_list:
        print('====',location)
        if int(location['y']) == -58:
            image_list_tp.append(image.crop((abs(int(location['x'])),58,abs(int(location['x']))+10,116)))
        if int(location['y']) == 0:
            image_list_down.append(image.crop((abs(int(location['x'])),0,abs(int(location['x']))+10,58)))

    new_image = Image.new('RGB',(260,116))
    positon_x = 0
    for image in image_list_tp:
        new_image.paste(image,(positon_x,0))
        positon_x += 10

    positon_x = 0
    for image in image_list_down:
        new_image.paste(image, (positon_x, 58))
        positon_x += 10

    # new_image.show()
    return new_image


'''对比图像找到缺口位置'''
def get_diff_location(image1,image2):
    for x in range(1,259):   #边为26   26*10-1
        for y in range(1,115):   #58*2-1
            #判断成立  表示两张图的像素点不一样
            if is_similar(image1,image2,x,y) == False:
                return x


'''对比图像找到缺口位置'''
def is_similar(image1,image2,x,y):
    pixel1 = image1.getpixel((x,y))
    pixel2 = image2.getpixel((x,y)) #元祖

    for i in range(0,3):
        if (abs(pixel1[i] - pixel2[i]) >= 50):
            return False
    return True


    ''' 模拟人拖动 先加速后减速 '''
def get_track(driver,move_dist):
    actions = webdriver.ActionChains(driver)
    actions.click_and_hold(elem)   #click_and_hold长按元素
    actions.pause(0.4)
    actions.move_by_offset(move_dist - 3, 0)  #move_by_offset以当前点为原点移动
    actions.pause(0.2)
    actions.move_by_offset(+3, 0)
    actions.pause(0.1)
    actions.move_by_offset(+5, 0)
    actions.pause(0.3)
    actions.move_by_offset(-7, 0)
    actions.pause(0.6)
    '''松开按钮'''
    actions.release()
    ''' 结束动作  调用perform 才会执行'''
    actions.perform()


def main(driver,elem):
    image1 = get_image(driver, 'gt_cut_fullbg_slice', 'fullbgbg')
    image2 = get_image(driver, 'gt_cut_bg_slice', 'bg')
    dist = get_diff_location(image1, image2)
    get_track(driver=driver,move_dist=dist)



def get_home_li(driver):
    lis = driver.find_elements_by_xpath("//*[@class='im0l_v16']/ul/li//p//a")
    for li in lis:
        print(li.txt)



if __name__ == '__main__':
    driver = webdriver.Chrome()

    driver.maximize_window()

    driver.get('http://www.cnbaowen.net/api/geetest/')

    try:
        count = 5
        wait = WebDriverWait(driver, 10)
        elem = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'gt_slider_knob')))
        while count > 0:
            main(driver,elem)
            time.sleep(5)
            # try:
            driver.find_element_by_xpath("//input[@name='submit']").click()
            print(driver.title)
            if '保温材料网'in driver.title:
                print('成功进入首页')
                get_home_li(driver)
            else:
                count -= 1
                time.sleep(1)
    finally:
        driver.quit()