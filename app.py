import streamlit as st
import time
import pandas as pd
import requests
import math
from datetime import datetime
from decimal import Decimal, getcontext

# ตั้งค่าความละเอียด
getcontext().prec = 50

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

# --- ระบบล็อกอิน ---
if 'user_info' not in st.session_state:
    with st.form("user_form"):
        source = st.text_input("ระบุโรงเรียน/หน่วยงาน")
        submit = st.form_submit_button("เข้าสู่ระบบ")
        if submit and source:
            st.session_state.user_info = {"source": source}
            st.rerun()
    st.stop() # หยุดทำงานจนกว่าจะล็อกอิน

# --- หน้าคำนวณหลัก (จะแสดงต่อเมื่อล็อกอินแล้ว) ---
st.subheader("ส่วนคำนวณ")
a = st.number_input("ใส่ค่า a:", value=1)
k_input = st.text_input("ใส่ค่า k (คั่นด้วยคอมม่า):", value="10, 100, 1000, 10000")

# [ฟังก์ชัน brute_force และ high_speed คงเดิมไว้ที่นี่]
# [ส่วนปุ่มเปรียบเทียบ คงเดิมไว้ที่นี่]
