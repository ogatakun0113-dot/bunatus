import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# --- ページ設定 ---
st.set_page_config(page_title="分圧計算ツール", layout="centered")

# --- 見た目の設定 (CSS) ---
st.markdown("""
<style>
.stNumberInput label { font-size: 18px !important; font-weight: 800 !important; color: #2E8B57 !important; }
.result-box { background-color: #f0fff4; padding: 20px; border-radius: 10px; border-left: 5px solid #2E8B57; margin-top: 20px; }
.credit { text-align: right; font-size: 14px; color: #666; margin-bottom: -20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="credit">開発/制作：緒方</p>', unsafe_allow_html=True)
st.title('🛠️ 分圧・倍率器計算ツール')
st.markdown("---")

# --- 分圧回路の図解を生成して表示 ---
st.subheader("📊 分圧回路のイメージ")

# 画像を作成 (幅800, 高さ400)
width, height = 800, 400
image = Image.new('RGB', (width, height), '#f9f9f9')
draw = ImageDraw.Draw(image)

# フォントの設定 (システム標準のゴシック体)
try:
    font_lg = ImageFont.truetype("arial.ttf", 28)
    font_md = ImageFont.truetype("arial.ttf", 22)
    font_sm = ImageFont.truetype("arial.ttf", 18)
except:
    font_lg = ImageFont.load_default()
    font_md = ImageFont.load_default()
    font_sm = ImageFont.load_default()

# 線の色
line_color = '#333'
label_color = '#1E90FF' # 青
res_color = '#444'     # 抵抗

# 回路の描画
x_left = 200
x_right = 600
y_top = 80
y_mid = 200
y_bot = 320

# 電源ライン
draw.line((x_left, y_top, x_right, y_top), fill=line_color, width=3) # V-in
# グランドライン
draw.line((x_left, y_bot, x_right, y_bot), fill=line_color, width=3) # GND

# 抵抗の描画
res_w = 40
res_h = 60

# R1
draw.rectangle((x_left - res_w/2, y_mid - res_h*1.2, x_left + res_w/2, y_mid - res_h*0.2), fill=res_color)
# R2
draw.rectangle((x_left - res_w/2, y_mid + res_h*0.2, x_left + res_w/2, y_mid + res_h*1.2), fill=res_color)

# 接続線
draw.line((x_left, y_top, x_left, y_mid - res_h*1.2), fill=line_color, width=2) # V-in to R1
draw.line((x_left, y_mid - res_h*0.2, x_left, y_mid + res_h*0.2), fill=line_color, width=2) # R1 to R2
draw.line((x_left, y_mid + res_h*1.2, x_left, y_bot), fill=line_color, width=2) # R2 to GND

# 出力線
draw.line((x_left, y_mid, x_right, y_mid), fill=line_color, width=2) # Mid to V-out

# グランドシンボル
draw.line((x_right - 40, y_bot, x_right + 40, y_bot), fill=line_color, width=2)
draw.line((x_right - 25, y_bot + 10, x_right + 25, y_bot + 10), fill=line_color, width=2)
draw.line((x_right - 10, y_bot + 20, x_right + 10, y_bot + 20), fill=line_color, width=2)

# ラベルの追加
# 電圧
draw.text((x_right - 100, y_top - 40), "V-in (入力電圧)", fill=label_color, font=font_lg)
draw.text((x_right - 100, y_mid - 40), "V-out (出力電圧)", fill=label_color, font=font_lg)
draw.text((x_right - 50, y_bot + 30), "GND", fill=line_color, font=font_lg)

# 抵抗
draw.text((x_left - 100, y_mid - res_h*0.8), "R1", fill=line_color, font=font_lg)
draw.text((x_left - 100, y_mid + res_h*0.5), "R2", fill=line_color, font=font_lg)

# 計算式のテキスト
draw.text((x_left + 150, height - 70), "V-out = V-in × R2 / (R1 + R2)", fill='#555', font=font_md)

st.image(image, use_column_width=True)

st.markdown("---")

# --- 2. 入力と計算 ---
with st.expander("⚙️ 計算設定", expanded=True):
    col1, col2 = st.columns(2)
    v_in = col1.number_input("入力電圧 V-in (V)", value=24.000, format="%.3f")
    r1 = col2.number_input("抵抗 R1 (Ω)", value=1000.0, format="%.1f")
    
    col3, col4 = st.columns(2)
    r2 = col3.number_input("抵抗 R2 (Ω)", value=1000.0, format="%.1f")
    
    # 分圧計算 Vout = Vin * (R2 / (R1 + R2))
    if (r1 + r2) != 0:
        v_out = v_in * (r2 / (r1 + r2))
    else:
        v_out = 0.0

st.markdown('<div class="result-box">', unsafe_allow_html=True)
st.subheader("📊 計算結果")
st.metric("出力電圧 V-out (V)", f"{v_out:.3f} V")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("※分圧後のV-outは、V-inとGNDの間の電位差となります。")
