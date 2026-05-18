import sqlite3
from flask import g
from config import DATABASE, INITIAL_QUESTIONS

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                code TEXT UNIQUE,
                option_a TEXT,
                option_b TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                user_id INTEGER,
                question_id INTEGER,
                answer INTEGER,
                PRIMARY KEY (user_id, question_id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (question_id) REFERENCES questions (id)
            )
        ''')
        
        # 초기 질문 데이터 세팅 (DB가 비어있을 때만)
        cursor.execute('SELECT COUNT(*) FROM questions')
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.executemany('''
                INSERT INTO questions (category, code, option_a, option_b)
                VALUES (?, ?, ?, ?)
            ''', INITIAL_QUESTIONS)
        
        db.commit()

def init_app(app):
    app.teardown_appcontext(close_connection)

def get_user_by_name(name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
    return cursor.fetchone()

def create_user(name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
    db.commit()
    return cursor.lastrowid

def get_total_question_count():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM questions')
    row = cursor.fetchone()
    return row[0] if row else 0

def get_user_response_count(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM responses WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    return row[0] if row else 0

def get_all_questions():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM questions ORDER BY id ASC')
    return cursor.fetchall()

def clear_user_responses(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM responses WHERE user_id = ?', (user_id,))
    db.commit()

def save_user_responses(user_id, responses_list):
    db = get_db()
    cursor = db.cursor()
    for q_id, ans in responses_list:
        cursor.execute('INSERT INTO responses (user_id, question_id, answer) VALUES (?, ?, ?)', (user_id, q_id, ans))
    db.commit()

def get_user_answers(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT answer FROM responses WHERE user_id = ? ORDER BY question_id ASC', (user_id,))
    return [row['answer'] for row in cursor.fetchall()]

def get_other_users(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE id != ?', (user_id,))
    return cursor.fetchall()
