# pip install streamlit
import streamlit as st

# python만으로 웹 구현 가능
st.set_page_config(page_title='streamlit CRUD')
st.title("FastAPI SPA 비교")
st.markdown("""
    ### FastAPI는 프론트엔드를 만들어야 하지만 Streamlit은 파이썬 코드만 필요함. 
    """)
st.divider()
# 메모리 데이터베이스 상태관리
if "my_db" not in st.session_state:
    st.session_state.my_db = []
    # 1.create(추가 폼)
st.subheader("새 아이템 추가")
with st.form("add_form", clear_on_submit=True):
    new_name = st.text_input("아이템 이름", placeholder="예: 마우스")
    new_price = st.number_input("가격 :", min_value=0, step=1000)
    #제출 버튼
    submitted = st.form_submit_button("아이템 추가")
    if submitted:
        if new_name.strip() == "":
            st.warning("이름을 입력해 주세요!")
        else:
            # 상태에 저장
            new_id = len(st.session_state.my_db) + 1
            st.session_state.my_db.append({"id":new_id, "name":new_name, "price":new_price})
            st.success(f"'{new_name}' 추가 완료!")
            st.rerun() #추가 후 새로고침
st.divider()

# 2. Read & Delete
st.subheader("등록된 아이템 목록")
if len(st.session_state.my_db) == 0:
    st.info("아직 등록된 아이템이 없습니다.")
else :
    for item in st.session_state.my_db.copy():
        # columns 레이아웃 쉽게 구현
        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            st.write(f'**ID: #{item["id"]}')
        with col2:
            st.write(f'{item["name"]}-{item["price"]}')
        with col3:
            # 삭제 버튼
            if st.button("삭제 -", key=f'del_{item["id"]}'):
                st.session_state.my_db.remove(item)
                st.rerun()

# web에서 이 창을 열어야 할 때 pycharm-terminal에서
# (ai_env) PS C:\dev\workspace_python\ex_streamlit> streamlit run streamlit_item_260325.py

# cd ex_streamlit
# streamlit run 0325_streamlit_item.py