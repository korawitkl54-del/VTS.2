import streamlit as st
import time
import pandas as pd
import requests
import math
from datetime import datetime
from decimal import Decimal, getcontext

getcontext().prec = 50

st.set_page_config(page_title="เทเลสโคปิกกำลังสาม", layout="wide")

# --- ล็อกอิน ---
if 'user_info' not in st.session_state:
    st.title("เข้าสู่ระบบ")
    with st.form("user_form"):
        source = st.text_input("ระบุโรงเรียน/หน่วยงาน")
        submit = st.form_submit_button("เข้าสู่ระบบ")
        if submit and source:
            st.session_state.user_info = {"source": source}
            st.rerun()
    st.stop() # ถ้ายังไม่ล็อกอิน ให้หยุดทำงานที่นี่

# --- ส่วนนี้จะรันก็ต่อเมื่อ Login ผ่านแล้วเท่านั้น ---
st.title("⚡ Telescoping Cubic: ระบบคำนวณประสิทธิภาพสูง")

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

# --- ปุ่มคำนวณ ---
if st.button("เปรียบเทียบความเร็ว"):
    try:
        k_values = [int(x.strip()) for x in k_input.split(",")]
        results = []
        for k in k_values:
            val_bf = brute_force(a, k)
            val_hs = high_speed(a, k)
            is_correct = "✅ ถูกต้อง" if abs(val_bf - val_hs) < Decimal('1e-6') else "❌ ไม่ถูกต้อง"
            
            results.append({
                "k": k,
                "ผลลัพธ์ (BF)": f"{val_bf:.2f}",
                "ผลลัพธ์ (HS)": f"{val_hs:.2f}",
                "สถานะ": is_correct
            })
        st.table(pd.DataFrame(results))
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
