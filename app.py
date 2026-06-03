import streamlit as st
import time
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Boss Mel Benchmark", layout="wide")
st.title("⚡อัลกอริทึมการประมวลผลเทเลสโคปิกกำลังสามความเร็วสูง")

# 1. ระบบเก็บข้อมูลผู้ใช้งาน (Session State)
if 'user_info' not in st.session_state:
    with st.form("user_form"):
        source = st.text_input("ระบุโรงเรียน/หน่วยงาน:")
        submit = st.form_submit_button("เข้าสู่ระบบ")
        if submit:
            st.session_state.user_info = {"source": source, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            st.rerun()
    st.stop() # หยุดไว้ก่อนจนกว่าจะกรอกข้อมูล

st.write(f"ยินดีต้อนรับคุณจาก: **{st.session_state.user_info['source']}**")

# 2. ส่วนใส่ค่า a และ k
a = st.number_input("ใส่ค่า a:", value=1)
k_values = [10, 100, 1000, 10000] # เลือก k ได้เลย

# 3. ฟังก์ชันคำนวณ 2 แบบ
def brute_force(a, k):
    res = 1.0
    for n in range(a + 1, k + 1):
        res *= ((n + 1)**3 + a**3) / (n**3 - a**3)
    return res

def high_speed(a, k):
    # สูตรลดรูปที่ได้จาก Telescoping จะลดเหลือแค่การคำนวณจบในบรรทัดเดียว
    # (สมมติสูตรจากการจัดรูป Telescoping ตามภาพที่อ้ายให้มา)
    return (k + a + 1) / (2 * a + 1) # นี่คือตัวอย่างสูตรสรุป (อ้ายปรับแก้ตามสูตรจริงได้เลย)

# 4. ปุ่มรันเปรียบเทียบ
if st.button("เปรียบเทียบความเร็ว"):
    results = []
    for k in k_values:
        # ทดสอบ Brute-force
        start = time.time()
        val_bf = brute_force(a, k)
        time_bf = time.time() - start
        
        # ทดสอบ High-speed
        start = time.time()
        val_hs = high_speed(a, k)
        time_hs = time.time() - start
        
        results.append({
            "k": k,
            "BF Time (s)": f"{time_bf:.6f}",
            "HS Time (s)": f"{time_hs:.6f}",
            "Diff (x)": f"{time_bf/time_hs:.1f} เท่า"
        })
    
    # แสดงตาราง
    df = pd.DataFrame(results)
    st.table(df)
    st.success("เห็นความต่างไหมครับ? High-speed เร็วกว่าเห็นๆ!")
