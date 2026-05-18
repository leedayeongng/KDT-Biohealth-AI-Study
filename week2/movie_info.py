import requests

# 개인 API키 입니다. 실습에만 사용하세요!
API_KEY = "7f7314005c9a1bb8ee535cedbd043a27"
# 영화인 목록조회
CODE_URL = "http://kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json"
# 영화인 상세정보조회
INFO_URL = "http://kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json"
# 일간박스오피스
INFO_DAILY = "http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"

def search_people(keyword):
    """
    인물 이름으로 KOBIS 인물 목록 조회
    :param keyword: 검색이름
    :return: 영화인 목록
    """
    params = {
        "key": API_KEY
        ,"peopleNm" : keyword
    }
    res = requests.get(CODE_URL, params=params)
    data = res.json()
    return data['peopleListResult']['peopleList']
actor_arr = search_people("하정우")
for v in actor_arr:
    print(v)
    #people Cd를 입력받아 상세정보를 조회하시오(함수)
    #peoplecd로 인물상세정보조회
    #return:people info(dict)

def get_people_info(people_cd):
    params = {
        "key": API_KEY,
        "peopleCd" : people_cd

    }
    res = requests.get(INFO_URL, params=params)
    data = res.json()
    return data['peopleInfoResult']['peopleInfo']


for v in actor_arr:
    print(v)

    people_cd = v['peopleCd']
    info = get_people_info(people_cd)

    print(info['peopleNm'],info['filmos'])

    #일별박스오피스조회
    #yyyymmdd 기준일별박스오피스조회
    #return : daily boxofficelist(list)
    def daily_boxoffice(target_dt):
        """
        :param target_dt: = yyyyMMdd 기준
        :return: dailyBoxOfficeList
        """
        params ={
            "key": API_KEY
            ,"targetDt": target_dt
        }
        res=requests.get(INFO_DAILY, params=params)
        data = res.json()
        print(data)
    daily_boxoffice("20260118")

