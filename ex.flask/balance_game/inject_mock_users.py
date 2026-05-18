import os
import sqlite3
from config import DATABASE

def inject_test_data():
    if not os.path.exists(DATABASE):
        print("Error: DB 파일이 존재하지 않습니다. 먼저 서버를 구동(app.py)해서 DB를 초기화해주세요.")
        return
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    users_data = [
        ('펭수', 1, [1, 1, 1, 1, 1]), # 전부 A
        ('동수', 1, [2, 2, 2, 2, 2]), # 전부 B
        ('길동', 1, [1, 2, 1, 2, 1])  # A B A B A
    ]
    for name, user_group, answers in users_data:
        try:
            cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
            uid = cursor.lastrowid
            
            for qid, ans in enumerate(answers, start=1):
                cursor.execute('INSERT INTO responses (user_id, question_id, answer) VALUES (?, ?, ?)', (uid, qid, ans))
                
            print(f"[OK] 테스트 친구 데이터 추가 완료: {name}")
        except sqlite3.IntegrityError:
             print(f"[Skip] 이미 존재하는 친구입니다: {name}")

    conn.commit()
    conn.close()
    print("가상 친구 3명의 데이터가 DB에 정상 입력되었습니다!")

if __name__ == '__main__':
    inject_test_data()
