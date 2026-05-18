from flask import Flask, render_template, request, session, redirect, url_for
from config import SECRET_KEY
import database

from game_logic import find_best_and_worst_match

app = Flask(__name__)
app.secret_key = SECRET_KEY

database.init_app(app)

@app.before_request
def startup_checks():
    database.init_db(app)

@app.route('/')
def index():
    session.clear() # 처음 접속하면 세션(로그인 상태) 초기화
    error = request.args.get('error')
    return render_template('index.html', error=error)

@app.route('/start', methods=['POST'])
def start():
    name = request.form.get('username')
    
    if not name:
        return redirect(url_for('index', error="이름을 입력해주세요."))
    
    # 1. 유저 확인 또는 새로 등록
    user = database.get_user_by_name(name)
    
    if user:
        user_id = user['id']
        # 2. 이미 모든 질문에 답했는지 확인
        total_q_count = database.get_total_question_count()
        answered_count = database.get_user_response_count(user_id)
        has_responses = (answered_count >= total_q_count and total_q_count > 0)
    else:
        user_id = database.create_user(name)
        has_responses = False
    
    # 세션에 내 정보 저장
    session['user_id'] = user_id
    session['username'] = name
    
    if has_responses:
        return redirect(url_for('result')) # 이미 응답했으면 결과창으로 직행
    else:
        return redirect(url_for('game'))   # 처음이면 게임창으로 이동

@app.route('/game')
def game():
    if 'user_id' not in session:
        return redirect(url_for('index'))
        
    # 모든 질문 가져오기 (고정 목록)
    questions = database.get_all_questions()
    question_list = [dict(q) for q in questions]
    session['current_questions'] = [q['id'] for q in question_list]
    
    return render_template('game.html', questions=question_list)

@app.route('/submit', methods=['POST'])
def submit():
    if 'user_id' not in session or 'current_questions' not in session:
        return redirect(url_for('index'))
    user_id = session['user_id']
    submitted_questions = session['current_questions']
    # 이전 응답이 있다면 지우고 덮어쓰기
    database.clear_user_responses(user_id)
    # 내 응답 DB에 저장 (학생 실습은 여기서 안함, 웹 동작을 위해 뼈대에서 처리)
    responses_list = []
    for q_id in submitted_questions:
        ans = request.form.get(f'q_{q_id}')
        if ans is not None:
             responses_list.append((q_id, int(ans)))
             
    database.save_user_responses(user_id, responses_list)
    return redirect(url_for('result'))

@app.route('/result')
def result():
    if 'user_id' not in session:
        return redirect(url_for('index'))  
    current_user_id = session['user_id']
    current_user_name = session['username']

    # --- 데이터 준비 (학생들에게 넘겨줄 파이썬 자료형 만들기) ---
    # 1. 나의 응답 리스트 (예: [1, 2, 1, 1, 2])
    my_answers = database.get_user_answers(current_user_id)
    
    # 2. 모든 사람들의 정보와 응답 딕셔너리 리스트
    # 예: [{'name': '동수', 'answers': [1, 2, 2, 1, 1]}, {'name': '민지', 'answers': [1, 1, 1, 2, 2]}, ...]
    other_users = database.get_other_users(current_user_id)
    
    all_responses = []
    for u in other_users:
        uid = u['id']
        uname = u['name']
        f_answers = database.get_user_answers(uid)
        
        # 질문을 끝까지 안 푼 친구는 제외
        if len(f_answers) == len(my_answers):
            all_responses.append({
                'name': uname,
                'answers': f_answers
            })
    
    if not all_responses:
        return render_template('result.html', not_enough_users=True, user=session)
    # 작성한 'game_logic.py' 로직 실행!
    try:
        top_match, bottom_match = find_best_and_worst_match(current_user_name, my_answers, all_responses)
    except Exception as e:
        # 코드를 완성하지 않아 에러가 나면 띄워줄 임시 안내창
        return f"<h1>앗! game_logic.py 코드에 오류가 있거나 빈칸이 덜 채워졌습니다!</h1><p>에러 메시지: {e}</p>"

    return render_template('result.html', top=top_match, bottom=bottom_match, user=session)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
