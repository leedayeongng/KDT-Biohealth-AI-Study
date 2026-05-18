import os

#하위 모든 디렉토리 탐색
root= 'c:\\dev'

def fn_search(root, file_nm):
    for root_path, dirs, files in os.walk(root):
        for file_name in files:
            if file_nm in file_name:
                print("=" * 100)
                print(file_name)
                user_input = input("이 파일이 맞나요?(y/n)")
                if user_input == "y":
                    print("파일을 찾았습니다.")
                    print(os.path.join(root, file_name))
                    return
print("파일을 찾을 수 없습니다 ...")
if __name__ == '__main__':
    while True:
        try :
            parts = input("시작경로, 찾는 파일명 입력(종료 q):".strip().split()
            if len(parts) == 1 and parts[0].lower() == 'q':
                print("종료")
                break
            root.filename = parts
            fn_search(root,file_name)
        except Exception as e:
            print(str(e))


    #files <-- 파일 중 사용자 입력 키워드가 포함되어있는지 체크!
    #있다면 사용자에게 묻기    1/21 연습문제!!!!!
