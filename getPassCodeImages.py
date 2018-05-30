#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 00:59:17 2018

@author: shanghungshih
"""

import os
import re
import time
from selenium import webdriver
from PIL import Image

if os.path.exists(os.path.join(os.getcwd(), 'passCodeImages')) is False:
    os.makedirs(os.path.join(os.getcwd(), 'passCodeImages'))

# passCodeCoordinates.txt => column=[id, left, top, right, bottom]
record = open(os.path.join(os.getcwd(),'passCodeImages', 'passCodeCoordinates.txt'), 'a')

def generatePassCode(x=1):
    print('id\tleft\ttop\tright\tbottom')
    start = 0
    end = x
    if os.popen('ls %s' %(os.path.join(os.getcwd(), 'passCodeImages'))).read() != '' and os.popen('ls %s' %(os.path.join(os.getcwd(), 'passCodeImages'))).read() != 'passCodeCoordinates.txt\n':
        tmp = os.popen('ls %s' %(os.path.join(os.getcwd(), 'passCodeImages'))).read().replace('passCodeCoordinates.txt\n', '')
        start = int(re.split('[0]+', re.findall('[0-9]+', tmp.split('\n')[-2])[0])[1])+1
        end = int(re.split('[0]+', re.findall('[0-9]+', tmp.split('\n')[-2])[0])[1])+1+x
    for i in range(start, end):
        driver = webdriver.Firefox()
        driver.get('https://irs.thsrc.com.tw/IMINT/?student=university')

        driver.save_screenshot('screen.png')

        element = driver.find_element_by_id('BookingS1Form_homeCaptcha_passCode')
        #print(element.location)
        #print(element.size)

        left = element.location['x']
        right = element.location['x'] + element.size['width']
        top = element.location['y']
        bottom = element.location['y'] + element.size['height']
        #print(left, top, int(right), int(bottom))

        img = Image.open('screen.png')
        img = img.crop((left*2+1, top*2, int(right)*2, int(bottom)*2))
        #img = img.crop((1277, 1010, 1560, 1120))
        #img.show()
        filename = os.path.join(os.getcwd(), 'passCodeImages', ('passCode_%0.4d.png' %(i)))
        img.save(filename, 'png')
        driver.quit()
        record.writelines('%0.4d\t%s\t%s\t%s\t%s\n' %(i, left*2+1, top*2, int(right)*2, int(bottom)*2))
        print('%0.4d\t%s\t%s\t%s\t%s\n' %(i, left*2+1, top*2, int(right)*2, int(bottom)*2), sep='', end='')
        time.sleep(1)
    record.close()

generatePassCode(eval(input('請輸入欲爬取的台灣高鐵驗證碼圖片張數：')))