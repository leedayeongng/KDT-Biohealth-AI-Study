import requests
from bs4 import BeautifulSoup
import os
import re
import urllib.request as req

url = 'https://www.moviechart.co.kr/rank/realtime/index/image'
img_path ="./img"
if not os.path.exists(img_path):
    os.makedirs(img_path)
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
imgs = soup.select('.movieBox-list .movieBox-item img')
for i, img in enumerate(imgs):
    src_value = img['src']
    title = img['alt'].replace(":","_") #window 파일명 규칙 콜론:안됨
    arr = src_value.split('=')
    img_url = arr[-1]
    ext = os.path.splitext(img_url)[1]                  #파일명 확장자
    file_nm = os.path.join(img_path, title + ext)           #폴더경로에 저장을 위해
    req.urlretrieve(img_url, file_nm)                   #(이미지실제결로,저장경로)


