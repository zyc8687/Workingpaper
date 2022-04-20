from time import sleep
''' seleinum 隐形等待的包'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium import webdriver
import os,cv2
import numpy as np
''' 键盘输入包 '''
from selenium.webdriver.common.keys import Keys
import cv2
from urllib import request

class jd_spider():
    def __init__(self):
        self.url = 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F%3Fopenbpab%3Dwritecookie%26uabt%3D92_33_39%26cu%3Dtrue%26utm_source%3Dbaidu-pinzhuan%26utm_medium%3Dcpc%26utm_campaign%3Dt_288551095_baidupinzhuan%26utm_term%3D0f3d30c8dba7459bb52f2eb5eba8ac7d_0_dc062e67e6324ea793c4ba870ed1f02c'
        options = webdriver.ChromeOptions()
        ''' 让浏览器不识别被控制 '''
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)  # 设置隐形等待时间

    def login(self,img_name1,img_name2):
        self.driver.get(self.url)
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'qrcode-img')))
        self.driver.find_element_by_class_name('login-tab-r').click()
        sleep(1.5)
        input_use = self.driver.find_element_by_id('loginname')
        input_use.send_keys('18803348687', Keys.ENTER)

        sleep(1.5)
        input_pwd = self.driver.find_element_by_id('nloginpwd')
        # 输入文字回车键搜索
        input_pwd.send_keys('223978', Keys.ENTER)
        sleep(1.5)
        self.wait.until(ec.presence_of_element_located((By.ID,'loginsubmit'))).click()
        tp_img = self.wait.until(ec.element_to_be_clickable((By.XPATH,"//div[@class='JDJRV-bigimg']/img"))).get_attribute('src')
        hk_img = self.wait.until(ec.element_to_be_clickable((By.XPATH,"//div[@class='JDJRV-smallimg']/img"))).get_attribute('src')

        request.urlretrieve(tp_img, img_name1)
        request.urlretrieve(hk_img, img_name2)
        index = self.Get_Img_Index(img1=img_name1,img2=img_name2)
        sleep(1.5)
        self.Move_Block(index,self.driver)


    def Move_Block(self,index,driver):
        distance = int(index)-50
        print('移动距离', distance)
        actions = webdriver.ActionChains(driver)
        slider = driver.find_element_by_class_name('JDJRV-slide-btn')

        actions.click_and_hold(slider)
        ''' 停顿0。2秒 '''
        actions.pause(0.2)
        actions.move_by_offset(distance + 7, 0)
        actions.pause(0.5)
        actions.move_by_offset(-4, 0)
        actions.pause(0.3)

        '''松开按钮'''
        actions.release()
        ''' 结束动作 '''
        actions.perform()
        sleep(2)




    def Get_Img_Index(self,img1,img2):
        color_img = cv2.imread(img1)
        gray = cv2.cvtColor(color_img, cv2.COLOR_RGB2GRAY)  # 把彩色图片转换灰度图
        ret, gray = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)  # 阈值分割二值化  230灰度下线 255灰度上限 去除杂质
        gray = cv2.Laplacian(gray, cv2.CV_16S, ksize=3)  # 拉普拉斯算法 边缘加强
        gray = cv2.convertScaleAbs(gray)  # 原图和处理后的边界合并
        gray = np.array(gray, dtype='float')


        gap_img = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
        # 制作拼图过滤器
        gap = cv2.Laplacian(gap_img, -1, ksize=3)
        # 拉普拉斯提取边框
        ret, gap = cv2.threshold(gap, 240, 255, cv2.THRESH_BINARY)
        # 阈值分割去杂质
        gap = np.array(gap, dtype=float)

        output = cv2.filter2D(gray, -1, gap)  # 卷积操作 将拼图滤波（过滤出特点）进行全图运算
        output = (output - output.min()) / (output.max() - output.min()) * 255  # 特征图归一化，将图归于0-255的范围

        index = np.unravel_index(output[:, :350].argmax(), output[:, :350].shape)

        '''误差'''
        if index[1] < 85 or index[1] > 220:
            color_img = cv2.imread(img1)
            gray = cv2.cvtColor(color_img, cv2.COLOR_RGB2GRAY)  # 把彩色图片转换灰度图
            et, gray = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)  # 阈值分割二值化  230灰度下线 255灰度上限 去除杂质
            gray = cv2.Laplacian(gray, cv2.CV_16S, ksize=3)  # 拉普拉斯算法 边缘加强
            gray = cv2.convertScaleAbs(gray)  # 原图和处理后的边界合并
            gray = np.array(gray, dtype='float')

            gap_img = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
            # 制作拼图过滤器
            gap = cv2.Laplacian(gap_img, -1, ksize=3)
            # 拉普拉斯提取边框
            ret, gap = cv2.threshold(gap, 240, 255, cv2.THRESH_BINARY)
            # 阈值分割去杂质
            gap = np.array(gap, dtype=float)

            output = cv2.filter2D(gray, -1, gap)  # 卷积操作 将拼图滤波（过滤出特点）进行全图运算
            output = (output - output.min()) / (output.max() - output.min()) * 255  # 特征图归一化，将图归于0-255的范围

            index = np.unravel_index(output[:, :350].argmax(), output[:, :350].shape)
            print('第二次结果',index)
            return index[1]


        else:
            print(index)
            return index[1]




if __name__ == '__main__':
    jd = jd_spider()
    jd.login('jd_tp.png','jd_hk.png')