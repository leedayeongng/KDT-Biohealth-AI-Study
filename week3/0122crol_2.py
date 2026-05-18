import requests
from bs4 import BeautifulSoup
import csv
import time


def fn_get_bbs(page):
    time.sleep(0.2)
    url = f'https://www.paxnet.co.kr/tbbs/list?tbbsType=L&id=N10841&page={page}'
    res= requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'html.parser')
        # print(soup.prettify())
        ul = soup.select_one('#comm-list')
        lis = ul.select('li')
        data_rows = []
        # for li in lis:
        #     print(li)
        for idx, li in enumerate(lis):
            if idx != 0:
                seq = li.select_one('.type')
                # print(li)
                if seq:
                    seq_num = seq['data-seq']
                    title= li.select_one('.title .best-title').text.strip()
                    data_rows.append([seq_num, title])
        with open('paxnet.csv', 'a', encoding='utf-8', newline='') as f:
            write = csv.writer(f, delimiter='|')
            write.writerow(data_rows)
if __name__ == '__main__':
        for p in range(1,101):
            fn_get_bbs(p)

