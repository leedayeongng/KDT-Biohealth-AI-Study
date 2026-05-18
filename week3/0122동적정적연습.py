from selenium import webdriver    #beautiful 로 안보일때 selenium (동적보는)
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup   # 동적정적 이게 편해서 여것만사용해도댐 주로 정적볼때
url = "https://m.sports.naver.com/kfootball/article/311/0001966455"
import requests

res = requests.get(url) #요청    정적 html 전체가 출력 요거세문장@! 이단게에서 기사내용보이면정적
soup = BeautifulSoup(res.text, "html.parser")  #정적
print(soup.prettify())  #요거를 출력     # 정적은 페이지에 글자가 있다  #정적
# driver = webdriver.Chrome()  동
# driver.implicitly_wait(3)  동
# driver.get(url)  동
# time.sleep(1)  덩
# input_search = driver.find_element(By.ID, 'input_keyword')
# input_search.send_keys('축구')
# driver.find_element(By.CSS_SELECTOR, 'button.btn_search').click()
# time.sleep(2)
# driver.find_element(By.XPATH,
#                             '/html/body/div/div[2]/header/nav[1]/div/ul/li[4]/a/span').click()
# time.sleep(2)
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# driver.quit()
# lis = soup.select('.prod_list li')
# for li in lis:
#     print(li)
#     print("=" * 100)