from flask import Flask, render_template, url_for, request, session, redirect, flash
import pymysql
from config import Config
import hashlib
from functools import wraps
#import FinanceDataReader as fdr

app = Flask(__name__)
app.config.from_object(Config)

# 로그인 여부를 검사하는 데코레이터
#특정 라우트에 로그인 하지 않으면 접근 차단
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login_id' not in session:
            flash('로그인이 필요한 서비스 입니다.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



def get_db():
    return pymysql.connect(
         host=app.config['DB_HOST']
        ,user=app.config['DB_USER']
        ,password=app.config['DB_PASSWORD']
        ,db=app.config['DB_NAME']
        ,charset='utf8mb4'
        ,cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    market = "KRX"
    results = [] #검색결과
    keyword = "" #검색어
    watchlist = set() #관심종목
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        market = request.form.get('market', 'KRX')
        df = fdr.StockListing(market)
        if 'Symbol' in df.columns:
            df = df.rename(columns={'Symbol':'Code'})
        if 'Market' not in df.columns:
            df['Market'] = market
        if 'Name' in df.columns and 'Code' in df.columns:
            mask =  df['Name'].str.contains(keyword, case=False, na=False)|\
                    df['Code'].str.contains(keyword, case=False, na=False)

            filtered = df[mask]
            results = filtered.to_dict(orient='records')
            if not results:
                flash('검색결과가 없습니다.', 'info')
        else:
            flash(f'Market {market} data structure not supported yet', 'warning')


    return render_template('index.html',
        results=results, keyword=keyword,selected_market=market
      , watchlist_tickers=watchlist )

@app.route('/add", methods=['POST'])
@login_required
def add_to_watchlist():
    ticker = request.form['ticker']
    print(ticker)
    #관심종목 stocks 테이블에 저장.
    # 저장 후 관심종목 화면으로 이동
    return redirect(url_for('watchlist'))
@app.route('/watchlist')
@login_required
def watchlist():
    my_list = []
    return render_template('watchlist.html', my_list=my_list)

    def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

@app.route("/login", methods=['POST','GET'])
def login():
    if request.method =='POST':
        username = request.form['username']
        password = hash_pw(request.form['password'])
        print(username + "/" + password)
        conn = None
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute("SELECT user_id, login_id, user_nm FROM users WHERE login_id =%s AND user_pw =%s"
                               , (username,password))
                user = cursor.fetchone()
                if user:
                    session['login_id'] = user['user_id']
                    session['user_nm'] = user['user_nm']
                    flash(f"{user['user_nm']}님 환영합니다.", 'success')
                    return redirect(url_for('index'))
                else:
                    flash('아이디 또는 비밀번호가 올바르지 않습니다.','error')
        except Exception as e:
            print(str(e))
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    flash('로그아웃 되었습니다.', 'success')
    return redirect(url_for('login'))


@app.route('/register',methods=['POST','GET'])
def register():
    if request.method =='POST':
        login_id = request.form['loginid']
        user_pw = hash_pw(request.form['password'])
        user_nm = request.form['username']
        conn = None
        try:
            conn = get_db()
            with conn.cursor() as cursor:
                cursor.execute("SELECT user_id FROM users WHERE login_id = %s ",(login_id,))
                if cursor.fetchone():
                    flash("이미 존재하는 아이디입니다.!!", 'error')
                    return redirect(url_for('register'))
                cursor.execute("""INSERT INTO users (login_id, user_pw, user_nm)
                                  VALUES (%s, %s, %s) """,(login_id, user_pw, user_nm))
                conn.commit()
                flash("회원가입이 완료되었습니다! 로그인해주세요.",'success')
                return redirect(url_for('login'))
        except Exception as e:
            print(str(e))
        finally:
            conn.close()



    return render_template('register.html')





if __name__ == '__main__':
    app.run(debug=True)