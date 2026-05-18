import streamlit as st
st.set_page_config(layout="wide")
with open('mimic_ckd_analysis_report.md', encoding='utf-8') as f:
    md = f.read()
st.markdown(md)