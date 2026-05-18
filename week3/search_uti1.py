from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request as req
import os

from selenium.webdriver.common.devtools.v144.dom import discard_search_results


def get_img(query):
    all_cnt = 0
    del_cnt = 0
    result = []
    url = f'https://www.google.com/search?q={query}'
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.get(url)
    time.sleep(1)
    input("해결한 후 Enter...")
    driver.find_element(By.LINK_TEXT, '이미지').click()
    time.sleep(1)
    start_h = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(f'window.scrollTo(0, {start_h})')
        time.sleep(4)
        next_h = driver.execute_script("return document.body.scrollHeight")
        if start_h == next_h:
            break
        start_h = next_h
    imgs = driver.find_elements(By.TAG_NAME, 'img')
    img_set = set()
    for v in imgs:
        src = v.get_attribute('src')
        if src:
            img_set.add(src)
    driver.quit()
            #이미지 저장
    all_cnt = len(img_set)
    img_dir = os.path.join('./',query)
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    for i, v in enumerate(img_set):
        f = os.path.join(img_dir, str(i)+'.png')
        try:
            req.urlretrieve(v, f)
        except Exception as e:
            print(str(e))
        #파일삭제
        for filename in os.listdir(img_dir):
            file_path = os.path.join(img_dir, filename)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                if file_size < 1000:
                    os.remove(file_path)
                    del_cnt += 1
                else:
                    result.append(str(file_path))
    return result, all_cnt, del_cnt
if __name__ == '__main__':
    print(get_img('향유고래'))
