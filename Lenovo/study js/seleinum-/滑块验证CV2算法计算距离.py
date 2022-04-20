import re,random
from matplotlib import pyplot as plt
import cv2
import numpy as np
'''https://www.bilibili.com/video/BV1kT4y1L7e5?from=search&seid=15290919513795561525&spm_id_from=333.337.0.0'''
''' jupyter 运行查看步骤结果 '''


# color_img = cv2.imread('img.jpg')#打开图片
# # color_img   #矩阵显示
# # plt.imshow(color_img)  #显示图片
#
# gray = cv2.cvtColor(color_img,cv2.COLOR_RGB2GRAY)  #把彩色图片转换灰度图
# ret , gray = cv2.threshold(gray,190,255,cv2.THRESH_BINARY)#阈值分割二值化  230灰度下线 255灰度上限 去除杂质
# gray = cv2.Laplacian(gray,cv2.CV_16S,ksize=3)#拉普拉斯算法 边缘加强
# gray = cv2.convertScaleAbs(gray) #原图和处理后的边界合并
# gray = np.array(gray,dtype='float')
#
# plt.imshow(gray,cmap='gray')
#
# ''' 缺口图片↓ '''
# exp = cv2.imread('gap_img.jpg',cv2.IMREAD_GRAYSCALE)#制作拼图过滤器
# exp = cv2.Laplacian(exp, -1 , ksize=3)#拉普拉斯提取边框
# ret ,exp = cv2.threshold(exp,240,255,cv2.THRESH_BINARY)#阈值分割去杂质
# exp = np.array(exp,dtype=float)
# plt.imshow(exp,cmap='gray')
#
#
# output = cv2.filter2D(gray,-1,exp)#卷积操作 将拼图滤波（过滤出特点）进行全图运算
# output = (output-output.min())/(output.max()-output.min())*255  #特征图归一化，将图归于0-255的范围
# plt.imshow(output,cmap='gray')
#
#
# ''' output[:,:60]是图片宽60的地方切割'''
# index = np.unravel_index(output[:,:60].argmax(),output[:,:60,].shape)
# i = index[0]#纵坐标
# print(index)
#
# # plt.imshow(output,cmap='gray')
# # output[i,60:].argsort()[-10:][::-1]+60


def Get_Img_Index(img1,img2):
    color_img = cv2.imread(img1)
    gray = cv2.cvtColor(color_img, cv2.COLOR_RGB2GRAY)  # 把彩色图片转换灰度图
    ret, gray = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)  # 阈值分割二值化  230灰度下线 255灰度上限 去除杂质  需要调整第二个值
    gray = cv2.Laplacian(gray, cv2.CV_16S, ksize=3)  # 拉普拉斯算法 边缘加强
    gray = cv2.convertScaleAbs(gray)  # 原图和处理后的边界合并
    gray = np.array(gray, dtype='float')
    print(gray.size)


    gap_img = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
    # 制作拼图过滤器
    gap = cv2.Laplacian(gap_img, -1, ksize=3)
    # 拉普拉斯提取边框   不同类型图片需要调整第二个值
    ret, gap = cv2.threshold(gap, 240, 255, cv2.THRESH_BINARY)
    # 阈值分割去杂质
    gap = np.array(gap, dtype=float)

    output = cv2.filter2D(gray, -1, gap)  # 卷积操作 将拼图滤波（过滤出特点）进行全图运算
    output = (output - output.min()) / (output.max() - output.min()) * 255  # 特征图归一化，将图归于0-255的范围

    index = np.unravel_index(output[:, :680].argmax(), output[:, :680].shape)
    # i = index[0]  # 纵坐标
    print(index)


img1 = 'img.jpg'
img2 = 'gap_img.jpg'
Get_Img_Index(img1,img2)


