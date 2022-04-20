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
from time import sleep
import random
import cv2
import numpy as np



def Parse_Img():
    'checkContent_index'

def Main(driver,wait,img1,img2):
    search_button = wait.until(EC.element_to_be_clickable((By.ID, 'checkBtn')))
    input_search = driver.find_element_by_id('checkContent_index')
    input_search.send_keys('晋城市民政局')
    sleep(1.4)
    search_button.click()
    sleep(3)

    while True:
        ''' 验证码刷新第四次会出现重试提示 '''
        for i in range(1):
            if i == 3:
                print('超过重试错误，刷新页面')
                driver.refersh()
            else:
                #滑块
                slider_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'geetest_slider_button')))
                #图片
                img = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'geetest_canvas_bg')))
                img_location = img.location
                size = img.size
                # print('img_location',img_location)
                # print('size',size)
                '''
                553 195 260 160
                左  图片位置的左   553
                高  图片位置的高    195
                右  图片位置的x+图片的宽   553+226
                下  图片位置的y加图片的高   195+160
                得到页面图片的位置  和图片的大小 得到了图片在页面的位置  在进行截图  得到验证码图片
                '''
                print(img_location['x'],img_location['y'],size['width'],size['height'])
                left = img_location['x']
                top = img_location['y']
                right = img_location['x']+size['width']
                buttom = img_location['y']+size['height']
                driver.get_screenshot_as_file('full.png')
                img = Image.open('full.png')
                img = img.crop((left,top,right,buttom))
                img.save(img1)

                move_index = Get_Img_Index(img1,img2,size['height'])
                sleep(2)
                actions = webdriver.ActionChains(driver)

                actions.click_and_hold(slider_button)
                ''' 停顿0。2秒 '''
                actions.pause(1)
                actions.move_by_offset(move_index + 7, 0)
                actions.pause(1.5)
                actions.move_by_offset(-5, 0)
                actions.pause(1)

                '''松开按钮'''
                actions.release()
                ''' 结束动作 '''
                actions.perform()
                sleep(2)







def Get_Img_Index(img1,img2,img_height):
    color_img = cv2.imread(img1)
    gray = cv2.cvtColor(color_img, cv2.COLOR_RGB2GRAY)  # 把彩色图片转换灰度图
    ret, gray = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)  # 阈值分割二值化  230灰度下线 255灰度上限 去除杂质
    gray = cv2.Laplacian(gray, cv2.CV_16S, ksize=3)  # 拉普拉斯算法 边缘加强
    gray = cv2.convertScaleAbs(gray)  # 原图和处理后的边界合并
    gray = np.array(gray, dtype='float')


    gap_img = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
    # 制作拼图过滤器
    gap = cv2.Laplacian(gap_img, -1, ksize=3)
    # 拉普拉斯提取边框
    ret, gap = cv2.threshold(gap, 50, 255, cv2.THRESH_BINARY)
    # 阈值分割去杂质
    gap = np.array(gap, dtype=float)

    output = cv2.filter2D(gray, -1, gap)  # 卷积操作 将拼图滤波（过滤出特点）进行全图运算
    output = (output - output.min()) / (output.max() - output.min()) * 255  # 特征图归一化，将图归于0-255的范围

    index = np.unravel_index(output[:, :img_height].argmax(), output[:, :img_height].shape)
    i = index[0]  # index是纵坐标和横坐标      i得到纵坐标
    # print(index)
    index_list = output[i, 60:].argsort()[-6:][::-1] + 60  # 通过纵坐标 找到水平方向最大值  由此得出第二块拼图坐标 及需移动的纵坐标 吧前7名最大的数找出来
    print(index_list)
    move_index = np.mean(index_list)
    move_index = move_index
    print('移动距离是',move_index)
    return move_index





if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    ''' 让浏览器不识别被控制 '''
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get('https://www.cods.org.cn/')
    wait = WebDriverWait(driver, 10)
    Main(driver,wait,'yzm.png','yzmqk.png')
    sleep(1)
    # elem = wait.until(EC.element_to_be_clickable((By.ID, 'checkContent_index')))

