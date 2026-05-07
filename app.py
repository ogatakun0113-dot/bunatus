import streamlit as st

st.set_page_config(page_title="分圧計算ツール", layout="centered")

st.markdown("""
<style>
.stNumberInput label { font-size: 18px !important; font-weight: 800 !important; color: #2E8B57 !important; }
.result-box { background-color: #f0fff4; padding: 20px; border-radius: 10px; border-left: 5px solid #2E8B57; margin-top: 20px; }
.credit { text-align: right; font-size: 14px; color: #666; margin-bottom: -20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="credit">開発/制作：緒方</p>', unsafe_allow_html=True)
st.title('🛠️ 分圧・倍率器計算ツール')

with st.expander("ℹ️ 計算の仕組み", expanded=False):
    st.write("V-out = V-in × (R2 / (R1 + R2))")

col1, col2 = st.columns(2)
v_in = col1.number_input("入力電圧 V-in (V)", value=24.000, format="%.3f")
r1 = col2.number_input("抵抗 R1 (Ω)", value=1000.0, format="%.1f")

col3, col4 = st.columns(2)
r2 = col3.number_input("抵抗 R2 (Ω)", value=1000.0, format="%.1f")

if (r1 + r2) != 0:
    v_out = v_in * (r2 / (r1 + r2))
else:
    v_out = 0.0

st.markdown('<div class="result-box">', unsafe_allow_html=True)
st.subheader("📊 計算結果")
st.metric("出力電圧 V-out", f"{v_out:.3f} V")
st.markdown('</div>', unsafe_allow_html=True)
