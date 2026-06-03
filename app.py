import streamlit as st
import time
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- ตั้งค่า Google Sheets ---
def save_to_sheets(source, entry_time):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("BossMelLog").sheet1 # เปลี่ยนชื่อไฟล์ให้ตรงกับที่อ้ายตั้ง
    sheet.append_row([source, entry_time])

# --- หน้าจอหลัก ---
st.set_page_config(page_title="Boss Mel Performance Lab", layout="wide")
st.title("⚡ Boss Mel Performance Lab")

if 'user_info' not in st.session_state:
    with st.form("user_form"):
        source = st.text_input("คุณมาจากที่ไหนครับ?")
        submit = st.form_submit_button("เข้าสู่ระบบ")
        if submit and source:
            t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_to_sheets(source, t) # เก็บข้อมูลลง Sheets
            st.session_state.user_info = {"source": source, "time": t}
            st.rerun()
    st.stop()

# --- ส่วนคำนวณ ---
a = st.number_input("ใส่ค่า a:", value=1)
k_input = st.text_input("ใส่ค่า k (คั่นด้วยคอมม่า):", value="10, 100, 1000, 10000")

def brute_force(a, k):
    res = 1.0
    for n in range(a + 1, k + 1):
        res *= ((n + 1)**3 + a**3) / (n**3 - a**3)
    return res

def high_speed(a, k):
    return (k + a + 1) / (2 * a + 1)

if st.button("เปรียบเทียบความเร็ว"):
    try:
        k_values = [int(x.strip()) for x in k_input.split(",")]
        results = []
        for k in k_values:
            start = time.time()
            val_bf = brute_force(a, k)
            time_bf = time.time() - start
            
            start = time.time()
            val_hs = high_speed(a, k)
            time_hs = time.time() - start
            
            results.append({"k": k, "BF Time(s)": f"{time_bf:.6f}", "HS Time(s)": f"{time_hs:.6f}", "Result": f"{val_hs:.4f}"})
        
        st.table(pd.DataFrame(results))
    except:
        st.error("ใส่ค่า k ให้ถูกต้องนะครับ")
