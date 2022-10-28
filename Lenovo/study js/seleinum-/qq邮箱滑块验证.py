import urllib.request

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver import ActionChains

from time import sleep
''' seleinum 隐形等待的包'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium import webdriver
import os,cv2
import numpy as np



# ''' 固定值拖动滑块 '''
# def main(driver):
#     driver.get('https://mail.qq.com/')
#
#     sleep(1)
#     '''切换到qq登录的iferam窗口'''
#     driver.switch_to.frame('login_frame')
#
#     sleep(0.3)
#     driver.find_element_by_id('u').send_keys('1239965374')
#     sleep(0.9)
#     driver.find_element_by_id('p').send_keys('zyc2239785088')
#     sleep(0.9)
#     '''程序等待五秒 如果加载出来就执行后面的点击 没有执行出来就报错'''
#     WebDriverWait(driver,5).until(ec.element_to_be_clickable((By.ID,'login_button')))
#     driver.find_element_by_id('login_button').click()
#     sleep(1)
#
#     '''切换到滑块窗口'''
#     driver.switch_to.frame("tcaptcha_iframe")
#     '''拖动滑块'''
#     while True:
#         sleep(0.5)
#         slider = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.CLASS_NAME,'tc-drag-thumb')))
#         ''' 拖动距离 网站缺口位置一样 取均值175 '''
#         distance = 175
#         actions = webdriver.ActionChains(driver)
#
#
#         actions.click_and_hold(slider)
#         ''' 停顿0。2秒 '''
#         actions.pause(0.2)
#         actions.move_by_offset(distance+5, 0)
#         actions.pause(0.2)
#         actions.move_by_offset(-10, 0)
#         actions.pause(0.6)
#
#         '''松开按钮'''
#         actions.release()
#         ''' 结束动作 '''
#         actions.perform()
#         sleep(2)
#         try:
#             shuaxin = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.ID, 'e_reload')))
#             driver.find_element_by_id('e_reload').click()
#         except:
#             break


''' 计算距离拖动滑块 '''
def Count_Sliding(driver,img1,img2):
    driver.get('https://mail.qq.com/')
    sleep(0.3)
    '''切换到qq登录的iferam窗口'''
    driver.switch_to.frame('login_frame')
    # WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.ID, 'switcher_plogin')))
    driver.find_element_by_id('switcher_plogin').click()


    sleep(0.3)
    driver.find_element_by_id('u').send_keys('1239965374')
    sleep(0.9)
    driver.find_element_by_id('p').send_keys('zyc2239785088')
    sleep(0.9)
    '''程序等待五秒 如果加载出来就执行后面的点击 没有执行出来就报错'''
    WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.ID, 'login_button')))
    driver.find_element_by_id('login_button').click()
    sleep(1)

    '''切换到滑块窗口'''
    driver.switch_to.frame("tcaptcha_iframe")

    # #遍历文件夹
    # path = os.listdir('picture')
    # #按照图片名字排序
    # path.sort(reverse=False)
    img = driver.find_element_by_id('slideBg').get_attribute('src')
    gap_img = driver.find_element_by_id('slideBlock').get_attribute('src')
    urllib.request.urlretrieve(img,img1)
    urllib.request.urlretrieve(gap_img,img2)


    while True:
        sleep(0.5)
        slider = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.CLASS_NAME,'tc-drag-thumb')))
        distance = int(Get_Img_Index(img1,img2)*0.41)-50
        print('移动距离',distance)
        actions = webdriver.ActionChains(driver)


        actions.click_and_hold(slider)
        ''' 停顿0。2秒 '''
        actions.pause(0.2)
        actions.move_by_offset(distance+7, 0)
        actions.pause(0.5)
        actions.move_by_offset(-5, 0)
        actions.pause(0.3)

        '''松开按钮'''
        actions.release()
        ''' 结束动作 '''
        actions.perform()
        sleep(2)
        try:
            shuaxin = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.ID, 'e_reload')))
            driver.find_element_by_id('e_reload').click()
        except:
            break


def Get_Img_Index(img1,img2):
    color_img = cv2.imread(img1)
    gray = cv2.cvtColor(color_img, cv2.COLOR_RGB2GRAY)  # 把彩色图片转换灰度图
    ret, gray = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)  # 阈值分割二值化  230灰度下线 255灰度上限 去除杂质
    gray = cv2.Laplacian(gray, cv2.CV_16S, ksize=3)  # 拉普拉斯算法 边缘加强
    gray = cv2.convertScaleAbs(gray)  # 原图和处理后的边界合并
    gray = np.array(gray, dtype='float')
    print('图片大小为',gray.size)

    gap_img = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
    # 制作拼图过滤器
    gap = cv2.Laplacian(gap_img, -1, ksize=3)
    # 拉普拉斯提取边框
    ret, gap = cv2.threshold(gap, 240, 255, cv2.THRESH_BINARY)
    # 阈值分割去杂质
    gap = np.array(gap, dtype=float)

    output = cv2.filter2D(gray, -1, gap)  # 卷积操作 将拼图滤波（过滤出特点）进行全图运算
    output = (output - output.min()) / (output.max() - output.min()) * 255  # 特征图归一化，将图归于0-255的范围

    index = np.unravel_index(output[:, :680].argmax(), output[:, :680].shape)
    # i = index[0]  # 纵坐标
    print(index)
    return index[1]







if __name__ == '__main__':
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = Chrome(options=option)
    waits = WebDriverWait(driver, 10)  # 设置隐形等待时间
    # main(driver) #固定值拖动
    img1 = 'img.jpg'
    img2 = 'gap_img.jpg'
    Count_Sliding(driver,img1,img2)