import streamlit as st

st.title("ระบบ Boss Mel ทำงานได้แล้ว! 🚀")
st.write("ถ้าคุณเห็นหน้านี้ แสดงว่าระบบอัปเดตผ่าน GitHub สำเร็จแล้ว")

if st.button("กดเช็คระบบ"):
    st.balloons()
    st.success("ระบบทำงานสมบูรณ์แบบ!")
