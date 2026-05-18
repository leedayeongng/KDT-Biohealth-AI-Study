#pip install bs4
from bs4 import BeautifulSoup
import re




html_doc ='''
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>크롤링 연습 페이지</title>
</head>
<body>
  <h1>📰 오늘의 뉴스</h1>
  <ul id="news-list">
    <li class="headline"><a href="https://news.example.com/article1">AI가 바꿀 미래 사회</a></li>
    <li class="headline"><a href="https://news.example.com/article2">2025년 인기 프로그래밍 언어</a></li>
    <li class="headline"><a href="https://news.example.com/article3">기후 변화, 현실이 되다</a></li>
  </ul>

  <h2>📚 인기 책</h2>
  <div class="book-list">
    <div class="book">
      <p class="title">파이썬으로 시작하는 데이터 과학</p>
      <p class="price">₩25,000</p>
    </div>
    <div class="book">
      <p class="title">생활코딩 HTML+CSS</p>
      <p class="price">₩18,000</p>
    </div>
    <div class="book">
      <p class="title">AI 시대의 생존 전략</p>
      <p class="price">₩22,000</p>
    </div>
  </div>
</body>
</html>


'''

soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.prettify()) #구조화되게 출력
a_arr = soup.find_all('a')
for a in a_arr:
    print(a['href'])
    print(a.text)
# id
print(soup.find('ul,{"id":"news-list"}'))
#class
print(soup.find('li', {'class':'headline'}))
#select or select_one
news = soup.select_one('#news-list')
print(news)
headlines = soup.select_one('.headline')
print(headlines)

en = soup.find_all('a', string=re.compile('[a-zA-A]'))
print(en)