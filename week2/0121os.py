import os
import json

folder = os.getcwd() #현재위치
print(folder)
file_list = os.listdir(folder)
print(file_list)
for file in file_list:
    file_path = os.path.join(folder, file)
    if os.path.isdir(file_path):
        print("폴더:", file_path)
        if file == "test1":    #경로 파일 test1만들었었는데 if~폴더삭제 입력하니 삭제됨
            os.rmdir(file_path)
            print("폴더 삭제")
    elif os.path.isfile(file_path):
        print("파일:", file_path)




data= {"name":"Nick", "age":30}
#파이썬 객체를 -> json 문자열로 '직렬화'
json_str = json.dumps(data)
#저장
with open('data.json','w', encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False) #한글깨짐방지
#읽기
with open('data.json','r', encoding="utf-8") as f:
    load_data = json.load(f)
print(load_data)
#파일 삭제
filepath = os.path.join(folder, "data.json")
                    #경로 결합, 윈도우에서는 불필요하나 리눅스환경에서는 필요할수있다.
os.remove(filepath)
print('삭제됨')

