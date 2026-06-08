import streamlit as st
import time
import pandas as pd
import requests
import math
from datetime import datetime, timedelta
from decimal import Decimal, getcontext

# ตั้งค่าความละเอียดทศนิยมสูงถึง 50 ตำแหน่ง
getcontext().prec = 50

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="Telescopic Lab", layout="wide")

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxdB4SRyRHLicIA5jqiFhCufN9TFaFcd9ebkF_JfWd4Jizey-Is5bJ44E3vY_8f1JJE/exec"

def save_to_sheets(source):
    thai_time = datetime.utcnow() + timedelta(hours=7)
    params = {'source': source, 'time': thai_time.strftime("%Y-%m-%d %H:%M:%S")}
    try:
        requests.post(WEB_APP_URL, data=params)
    except:
        pass

# --- Sidebar & Login ---
with st.sidebar:
    st.image("image-removebg-preview.png", width=200)
    st.write("โรงเรียนบัวใหญ่")
    st.markdown("---")
    st.write("ระบบคำนวณเชิงประสิทธิภาพสูง")

if 'user_info' not in st.session_state:
    with st.form("user_form"):
        source = st.text_input("ระบุโรงเรียน/หน่วยงาน")
        if st.form_submit_button("เข้าสู่ระบบ") and source:
            save_to_sheets(source)
            st.session_state.user_info = {"source": source}
            st.rerun()
    st.stop()

st.title("⚡🍗🍗🍗 เทเลสโคปิก Telescoping cubic จากคณิตศาสตร์บริสุทธิ์สูอัลกอริทึมการประมวลผลความเร็วสูง")

# --- ฟังก์ชันคำนวณ (ใช้ Decimal เพื่อความแม่นยำ) ---
def brute_force(a, k):
    res = Decimal(1.0)
    a_dec = Decimal(a)
    for n in range(int(a) + 1, int(k) + 1):
        n_dec = Decimal(n)
        res *= ((n_dec + 1)**3 + a_dec**3) / (n_dec**3 - a_dec**3)
    return res

def high_speed(a, k):
    a = int(a)
    k = int(k)
    comb = Decimal(math.comb(k + a + 1, 2 * a + 1))
    
    prod_top = Decimal(1)
    for i in range(2, a + 1):
        prod_top *= Decimal(i**2 + a*i + a**2)
        
    prod_bottom = Decimal(1)
    for j in range(k - a + 2, k + 1):
        prod_bottom *= Decimal(j**2 + a*j + a**2)
        
    return comb * (prod_top / prod_bottom)

# --- ส่วนรับค่า ---
a = st.number_input("ใส่ค่า a:", value=1)
k_input = st.text_input("ใส่ค่า k (คั่นด้วยคอมม่า):", value="10, 100, 1000, 10000, 20000")

# --- ปุ่มคำนวณ ---
if st.button("เปรียบเทียบความเร็วและแสดงผล"):
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
            
            # ตรวจสอบความถูกต้องด้วย Tolerance ที่น้อยมากๆ
            status = "✅ ตรงกัน" if abs(val_bf - val_hs) < Decimal('1e-10') else "❌ ไม่ตรง"
            
            results.append({
                "k": k, 
                "รอบคำนวณ": iterations,
                "BF Time(s)": f"{time_bf:.6f}",
                "HS Time(s)": f"{time_hs:.6f}",
                "ผลลัพธ์ (BF)": f"{val_bf:.4f}",
                "ผลลัพธ์ (HS)": f"{val_hs:.4f}",
                "สถานะ": status
            })
        
        df = pd.DataFrame(results)
        st.table(df)
        
        st.subheader("📊 กราฟเปรียบเทียบความเร็ว")
        st.line_chart(df.set_index('k')[['BF Time(s)', 'HS Time(s)']].astype(float))
        
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
