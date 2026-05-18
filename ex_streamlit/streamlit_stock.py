import streamlit as st
import FinanceDataReader as fdr
from datetime import datetime,timedelta
import pandas as pd
import plotly.graph_objs as go

#페이지 설정
st.set_page_config(page_title="Stock Analysis", layout="wide")
st.title("실시간 주식 시장 분석 대시보드")
st.markdown("국내외 주식 데이터를 시각화합니다.")

#사이드 바
st.sidebar.header('설정')
#1.종목 선택
stock_dict ={
    "삼성전자":"005930",
    "현대차":"005380",
    "Tesla":"TSLA",
    "NVIDIA":"NVDA",

}
target_stock = st.sidebar.selectbox("대상 종목 선택", list(stock_dict.keys()))
symbol = stock_dict[target_stock]
#기간 선택
col1, col2 = st.sidebar.columns(2)
with col1:
    st_date = st.date_input("시작일",datetime.now() - timedelta(days=365))
with col2:
    en_date = st.date_input("종료일", datetime.now())
    #추가지표선택
show_ma5 = st.sidebar.checkbox("5일 이동평균선", value=True)
show_ma20 = st.sidebar.checkbox("20일 이동평균선",value=True)
show_ma60 = st.sidebar.checkbox("60일 이동평균선", value=False)
show_volume = st.sidebar.checkbox("거래량 표시",value=True)

#데이터 로드
def get_stock_data(symbol, start,end):
    df = fdr.DataReader(symbol, start=start, end=end)
    return df
try:
    with st.spinner("데이터를 불러오고 있습니다..."):
        df = get_stock_data(symbol, st_date, en_date)
    if df.empty:
        st.error("데이터가 없습니다. 기간을 확인해주세요.")
    else:
        #지표계산
        df['MA5'] = df['Close'].rolling(window=5).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA60'] = df['Close'].rolling(window=60).mean()
        #캔들스틱 차크생성
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'],close=df['Close']
            ,name='Price'
        ))
        #차트에 이동평균선 추가
        if show_ma5:
            fig.add_trace(go.Scatter(x=df.index, y=df['MA5']
                                     , name='MA5', line=dict(color='orange',width=1)))
        if show_ma20:
            fig.add_trace(go.Scatter(x=df.index, y=df['MA20']
                                     , name='MA20', line=dict(color='blue',width=1)))
        if show_ma60:
            fig.add_trace(go.Scatter(x=df.index, y=df['MA60']
                                     , name='MA60', line=dict(color='red', width=1)))
        st.plotly_chart(fig, use_container_width=True)
        #하단 정보입력
        st.markdown("---")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        last_price = df['Close'].iloc[-1]
        prev_price = df['Close'].iloc[-2]
        change = last_price - prev_price
        pct_change = (change / prev_price) * 100
        m_col1.metric("현재가",f'{last_price:,}',f'{change:+,} ({pct_change:.2f}%)')
        m_col2.metric('고가(기간 내)', f'{df["High"].max():}')
        m_col3.metric('저가(기간 내',f'{df["Low"].min():}')
        m_col4.metric('거래량',f'{df["Volume"].iloc[-1]:,}')
        if show_volume:
            st.subheader('거래량')
            st.bar_chart(df['Volume'])
        if st.checkbox('전체 데이터 테이블 보기'):
            st.dataframe(df)


except Exception as e:
    print(str(e))

    ## cd ex_streamlit
# streamlit run 0325_streamlit_item.py