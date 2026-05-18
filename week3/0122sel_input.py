from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
url = "https://www.hanatour.com/package/international"
driver = webdriver.Chrome() #동
driver.implicitly_wait(3) #동
driver.get(url) #동
time.sleep(1) #동
input_search = driver.find_element(By.ID, 'input_keyword')
input_search.send_keys('하와이')
driver.find_element(By.CSS_SELECTOR, 'button.btn_search').click()
time.sleep(2)
driver.find_element(By.XPATH,
                    '/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/ul/li[2]/a').click()

time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser') #여기까지 동
driver.quit()
lis = soup.select('.prod_list li')
for li in lis:
    print(li)
    print("=" * 100)

    # 원하는데이터가 수집안되면 동적, 되면 정적

