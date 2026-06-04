import streamlit as st
import time
import pandas as pd
import requests
from datetime import datetime

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="เทเลสโคปิกกำลังสาม", layout="wide")

# --- Sidebar ---
with st.sidebar:
    # ตรวจสอบชื่อไฟล์รูปให้ตรงกับที่อัปขึ้น GitHub
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

# --- ส่วนคำนวณ ---
a = st.number_input("ใส่ค่า a:", value=1)
k_input = st.text_input("ใส่ค่า k (คั่นด้วยคอมม่า):", value="10, 100, 1000, 10000")
st.warning("⚠️ คำเตือน: แนะนำอย่าใส่ค่า k เกิน 10 ล้าน เนื่องจากอาจทำให้ระบบโหลดช้าครับ")

def brute_force(a, k):
    res = 1.0
    for n in range(a + 1, k + 1):
        res *= ((n + 1)**3 + a**3) / (n**3 - a**3)
    return res

def high_speed(a, k):
    return (k + a + 1) / (2 * a + 1)

# --- ปุ่มรันเปรียบเทียบ ---
if st.button("เปรียบเทียบความเร็ว"):
    try:
        k_values = [int(x.strip()) for x in k_input.split(",")]
        results = []
        for k in k_values:
            iterations = max(0, k - a)
            
            # วัดเวลา BF
            start = time.time()
            val_bf = brute_force(a, k)
            time_bf = time.time() - start
            
            # วัดเวลา HS
            start = time.time()
            val_hs = high_speed(a, k)
            time_hs = time.time() - start
            
            # เช็คความถูกต้องด้วยทศนิยม 4 ตำแหน่ง
            is_correct = "✅ ถูกต้อง" if round(val_bf, 4) == round(val_hs, 4) else "❌ ไม่ถูกต้อง"
            speed_ratio = time_bf / time_hs if time_hs > 0 else 0
            
            results.append({
                "k": k,
                "รอบการคำนวณ (BF)": iterations,
                "BF Time(s)": f"{time_bf:.6f}",
                "HS Time(s)": f"{time_hs:.6f}",
                "อัตราส่วนความเร็ว": f"{speed_ratio:.1f} เท่า",
                "ผลลัพธ์ (BF)": f"{val_bf:.4f}",
                "ผลลัพธ์ (HS)": f"{val_hs:.4
