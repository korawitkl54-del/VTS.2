import streamlit as st
import time
import pandas as pd
from datetime import datetime

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="Boss Mel Performance Lab", layout="wide")
st.title("⚡ อัลกอริทึมประมวลผลเทเลสโคปิกกำลังสามความเร็วสูง")

# --- 1. ระบบเก็บข้อมูลผู้ใช้ ---
if 'user_info' not in st.session_state:
    st.subheader("ยินดีต้อนรับเข้าสู่ระบบ")
    with st.form("user_form"):
        source = st.text_input("ระบุโรงเรียน/หน่วยงาน")
        submit = st.form_submit_button("เข้าสู่ระบบ")
        if submit and source:
            st.session_state.user_info = {
                "source": source, 
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.rerun()
    st.stop()

st.sidebar.write(f"ผู้ใช้: {st.session_state.user_info['source']}")
st.sidebar.write(f"เวลาเข้า: {st.session_state.user_info['time']}")

# --- 2. ส่วนรับค่า k และ a ---
a = st.number_input("ใส่ค่า a:", value=1)
k_input = st.text_input("ใส่ค่า k (คั่นด้วยคอมม่า):", value="10, 100, 1000, 10000")

try:
    k_values = [int(x.strip()) for x in k_input.split(",")]
except:
    st.error("กรุณาใส่ตัวเลขโดยใช้เครื่องหมายคอมม่าคั่นเท่านั้น")
    k_values = []

# --- 3. ฟังก์ชันคำนวณ ---
def brute_force(a, k):
    res = 1.0
    for n in range(a + 1, k + 1):
        res *= ((n + 1)**3 + a**3) / (n**3 - a**3)
    return res

def high_speed(a, k):
    # สูตรจากการลดรูป Telescoping
    return (k + a + 1) / (2 * a + 1)

# --- 4. ปุ่มรันและแสดงผล ---
if st.button("เปรียบเทียบความเร็ว"):
    if k_values:
        results = []
        for k in k_values:
            # วัดเวลา Brute-force
            start = time.time()
            val_bf = brute_force(a, k)
            time_bf = time.time() - start
            
            # วัดเวลา High-speed
            start = time.time()
            val_hs = high_speed(a, k)
            time_hs = time.time() - start
            
            results.append({
                "k": k,
                "BF Time (s)": f"{time_bf:.6f}",
                "HS Time (s)": f"{time_hs:.6f}",
                "BF Result": f"{val_bf:.4f}",
                "HS Result": f"{val_hs:.4f}"
            })
        
        df = pd.DataFrame(results)
        st.table(df)
        st.success("เปรียบเทียบเสร็จสิ้น!")
    else:
        st.warning("กรุณาระบุค่า k ก่อนครับ")
