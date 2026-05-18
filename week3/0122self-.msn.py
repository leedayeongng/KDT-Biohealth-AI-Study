#pip install selenium
#pip install chromedriver_autoinstaller

from selenium.webdriver.ie.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
chromedriver_autoinstaller.install() #크롬드라이버 설치
url ="https://www.msn.com/ko-kr"
driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get(url)
import time
time.sleep(2)
body = driver.find_element(By.TAG_NAME,'body') #스크롤 대상
page = 1
while page < 100:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1) #load 기다림
    page +=1

driver.quit()