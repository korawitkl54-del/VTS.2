import streamlit as st
import time
import pandas as pd
import requests
import math
from datetime import datetime
from decimal import Decimal, getcontext

# ตั้งค่าความละเอียดทศนิยม
getcontext().prec = 50

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="เทเลสโคปิกกำลังสาม", layout="wide")

# --- Web App URL ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyC87oA6lqQaxWUfo8y5OtImplEP2552O1C-Tj2zTctw1cyeMC1Tm7F7M2Ag9FkN3lR/exec"

def save_to_sheets(source, entry_time):
    params = {'source': source, 'time': entry_time}
    try:
        requests.post(WEB_APP_URL, data=params)
    except:
        pass

# --- Sidebar ---
with st.sidebar:
    try:
        st.image("image-removebg-preview.png", width=200)
    except:
        st.write("โรงเรียนบัวใหญ่")
    st.markdown("---")
    st.write("ระบบคำนวณเชิงประสิทธิภาพสูง")

# --- ระบบล็อกอิน ---
if 'user_info' not in st.session_state:
    st.title("เข้าสู่ระบบ")
    with st.form("user_form"):
        source = st.text_input("ระบุโรงเรียน/หน่วยงาน")
        submit = st.form_submit_button("เข้าสู่ระบบ")
        if submit and source:
            t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_to_sheets(source, t)
            st.session_state.user_info = {"source": source}
            st.rerun()
    st.stop()

# --- หน้าหลัก ---
st.title("⚡ เทเลสโคปิกกำลังสาม Telescoping Cubic จากคณิตศาสตร์บริสุทธิ์สู่อัลกอริทึมการประมวลผลความเร็วสูง")

def brute_force(a, k):
    res = Decimal(1.0)
    a_dec = Decimal(a)
    for n in range(int(a) + 1, int(k) + 1):
        n_dec = Decimal(n)
        res *= ((n_dec + 1)**3 + a_dec**3) / (n_dec**3 - a_dec**3)
    return res

def high_speed(a, k):
    a_dec = Decimal(a)
    k_dec = Decimal(k)
    n_val = int(k_dec + a_dec + 1)
    r_val = int(2 * a_dec + 1)
    comb = Decimal(math.comb(n_val, r_val))
    prod_top = Decimal(1)
    for i in range(2, int(a_dec) + 1):
        prod_top *= (Decimal(i)**2 + a_dec*Decimal(i) + a_dec**2)
    prod_bottom = Decimal(1)
    for j in range(int(k_dec - a_dec + 2), int(k_dec) + 1):
        prod_bottom *= (Decimal(j)**2 + a_dec*Decimal(j) + a_dec**2)
    return comb * (prod_top / prod_bottom)

# --- ช่องใส่ค่า ---
a = st.number_input("ใส่ค่า a:", value=1)
k_input = st.text_input("ใส่ค่า k (คั่นด้วยคอมม่า):", value="10, 100, 1000, 10000")

# --- ปุ่มรัน ---
if st.button("เปรียบเทียบความเร็ว"):
    try:
        k_values = [int(x.strip()) for x in k_input.split(",")]
        results = []
        for k in k_values:
            iterations = max(0, k - a)
            start_bf = time.time()
            val_bf = brute_force(a, k)
            time_bf = time.time() - start_bf
            
            start_hs = time.time()
            val_hs = high_speed(a, k)
            time_hs = time.time() - start_hs
            
            is_correct = "✅ ถูกต้อง" if abs(val_bf - val_hs) < Decimal('1e-6') else "❌ ไม่ถูกต้อง"
            speed_ratio = time_bf / time_hs if time_hs > 0 else 0
            
            results.append({
                "k": k,
                "รอบการทำงาน (BF)": iterations,
                "BF Time(s)": f"{time_bf:.6f}",
                "HS Time(s)": f"{time_hs:.6f}",
                "อัตราส่วนความเร็ว": f"{speed_ratio:.1f} เท่า",
                "ผลลัพธ์ (BF)": f"{val_bf:.4f}",
                "ผลลัพธ์ (HS)": f"{val_hs:.4f}",
                "สถานะ": is_correct
            })
        st.table(pd.DataFrame(results))
    except Exception as err:
        st.error("เกิดข้อผิดพลาด: " + str(err))
