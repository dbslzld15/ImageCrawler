import errno
import sys, os
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib, urllib.request
import requests
import random
import time
from selenium.webdriver.common.keys import Keys

# # 이 크롤러는 .image 폴더에 이미지 생성 # #

# initial set

folder = ".image/"
url = "https://www.google.com/search"
webDriver = "./chromedriver.exe"
searchItem = "김치찌개"   # 키워드 설정
size = 1000 # 원하는 갯수이지만 크롤링 중 결과 더보기를 수동으로 눌러줘야 더 크롤링 가능

params ={
   "q":searchItem
   ,"tbm":"isch"
   ,"sa":"1"
   ,"source":"lnms&tbm=isch"
}

url = url+"?"+urllib.parse.urlencode(params)
browser = webdriver.Chrome(webDriver)
time.sleep(0.5)
browser.get(url)
html = browser.page_source
time.sleep(0.5)

### get number of image for a page

soup_temp = BeautifulSoup(html,'html.parser')
img4page = len(soup_temp.findAll("img"))

### page down

elem = browser.find_element_by_tag_name("body")
imgCnt =0
while imgCnt < size*10:
    elem.send_keys(Keys.PAGE_DOWN)
    rnd = random.random()
    print(imgCnt)
    time.sleep(rnd)
    imgCnt+=img4page

html = browser.page_source
soup = BeautifulSoup(html,'html.parser')
img = soup.findAll("img")

browser.find_elements_by_tag_name('img')

fileNum=0
srcURL=[]

for line in img:
   if str(line).find('data-src') != -1 and str(line).find('http')<100:
      print(fileNum, " : ", line['data-src'])
      srcURL.append(line['data-src'])
      fileNum+=1

### make folder and save picture in that directory

saveDir = folder+searchItem

try:
    if not(os.path.isdir(saveDir)):
        os.makedirs(os.path.join(saveDir))
except OSError as e:
    if e.errno != errno.EEXIST:
        print("Failed to create directory!!!!!")
        raise

for i,src in zip(range(fileNum),srcURL):
    urllib.request.urlretrieve(src, saveDir+"/"+str(i)+".jpg")
    print(i,"saved")