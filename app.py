import streamlit as st
import time
import pandas as pd
import requests
import math
from datetime import datetime
from decimal import Decimal, getcontext

# ตั้งความแม่นยำทศนิยมไว้ที่ 50 ตำแหน่ง
getcontext().prec = 50

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="เทเลสโคปิกกำลังสาม", layout="wide")

# --- Sidebar ---
with st.sidebar:
    try:
        st.image("image-removebg-preview.png", width=200) 
    except:
        st.write("โรงเรียนบัวใหญ่")
    st.markdown("---")
    st.write("ระบบคำนวณเชิงประสิทธิภาพสูง")

st.title("⚡ Telescoping Cubic จากคณิตศาสตร์บริสุทธิ์สู่อัลกอริทึมการประมวลผลความเร็วสูง")

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyC87oA6lqQaxWUfo8y5OtImplEP2552O1C-Tj2zTctw1cyeMC1Tm7F7M2Ag9FkN3lR/exec"

def save_to_sheets(source, entry_time):
    params = {'source': source, 'time': entry_time}
    try:
        requests.post(WEB_APP_URL, data=params)
    except:
        pass

# --- ระบบล็อกอิน ---
if 'user_info' not in st.session_state:
    with st.form("user_form"):
        source = st.text_input("ระบุโรงเรียน/หน่วยงาน")
        submit = st.form_submit_button("เข้าสู่ระบบ")
        if submit and source:
            t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_to_sheets(source, t)
            st.session_state.user_info = {"source": source, "time": t}
            st.rerun()
    st.stop()
