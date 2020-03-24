from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve
import os
import time
from tqdm import tqdm

driver = webdriver.Chrome("./chromedriver.exe")

keyword = "김치찌개"

driver.get('https://www.pinterest.co.kr/')

time.sleep(1)

# 로그인 화면 처리
login = driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div[2]/div/div/div[3]/div[1]/div[1]/div[2]/div[1]/button')
login.click()
time.sleep(1)
driver.find_element_by_name('id').send_keys('dbslzld15@naver.com')
driver.find_element_by_name('password').send_keys('srt86241380@')
driver.find_element_by_name('password').send_keys(Keys.ENTER)
time.sleep(5)

# 검색 키워드 서치
search = driver.find_element_by_css_selector('input.SearchBoxInputExperimental')
search.send_keys(keyword)
search.send_keys(Keys.ENTER)

# 페이지 스크롤 다운
scrollTime = 10  # 밑으로 스크롤 횟수, 많이 할 수록 더 많은 이미지 저장
body = driver.find_element_by_css_selector('body')
for i in range(scrollTime):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

# 이미지 링크 수집
imgs = driver.find_elements_by_css_selector('img.hCL.kVc.L4E.MIw')
result = []
filenum = 0
for img in tqdm(imgs):
    if 'http' in img.get_attribute('src'):
        # print(img.get_attribute('src'))
        result.append(img.get_attribute('src'))
        filenum += 1

# driver.close()
print(filenum, "개 링크 수집 완료")

# 폴더 생성
if not os.path.isdir('./{}{}'.format("핀터레스트", keyword)):
    os.mkdir('./{}{}'.format("핀터레스트", keyword))

# 다운로드
for index, link in tqdm(enumerate(result)):
    filetype = '.jpg'
    urlretrieve(link, './{}{}/{}{}{}'.format("핀터레스트",keyword, keyword, index, filetype))
    time.sleep(1)

print("다운로드완료")