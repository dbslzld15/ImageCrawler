from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve
import os
import time
from tqdm import tqdm

# 평균속도 1시간 2000개의 이미지 저장

driver = webdriver.Chrome("./chromedriver.exe")

keyword = "김치찌개"

driver.get('https://www.picuki.com/tag/' + keyword)

# 페이지 스크롤 다운
scrollTime = 5  # 밑으로 스크롤 횟수, 많이 할 수록 더 많은 이미지 저장
body = driver.find_element_by_css_selector('body')
for i in range(scrollTime):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

# 이미지 링크 수집
imgs = driver.find_elements_by_css_selector('img.post-image')
result = []
filenum = 0
for img in tqdm(imgs):
    if 'http' in img.get_attribute('src'):
        #  print(img.get_attribute('src'))
        result.append(img.get_attribute('src'))
        filenum += 1

driver.close()
print(filenum, "개 링크 수집 완료")

# 폴더 생성
if not os.path.isdir('./{}{}'.format("인스타그램", keyword)):
    os.mkdir('./{}{}'.format("인스타그램", keyword))

# 다운로드
for index, link in tqdm(enumerate(result)):
    filetype = '.jpg'
    urlretrieve(link, './{}{}/{}{}{}'.format("인스타그램", keyword, keyword, index, filetype))
    time.sleep(1)

print("다운로드완료")