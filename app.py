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

# 画像を作成 (幅800, 高さ450に少し高く設定)
width, height = 800, 450
image = Image.new('RGB', (width, height), '#f9f9f9')
draw = ImageDraw.Draw(image)

# フォントの設定 (システム標準のゴシック体を大きく設定)
try:
    # 緒方仕様：以前の2倍程度の大きさに設定
    font_xl = ImageFont.truetype("arial.ttf", 55) # V-in, V-outなど
    font_lg = ImageFont.truetype("arial.ttf", 45) # R1, R2, GND
    font_md = ImageFont.truetype("arial.ttf", 30) # 計算式
except:
    # フォントが読み込めない場合のフォールバック（Streamlit Cloudなど）
    font_xl = ImageFont.load_default()
    font_lg = ImageFont.load_default()
    font_md = ImageFont.load_default()

# 線の色
line_color = '#333'
label_color = '#1E90FF' # 青（視認性の高い色に変更）
res_color = '#444'     # 抵抗

# 回路の描画位置調整
x_left = 180  # R1, R2ラベル用スペース確保
x_right = 650 # V-in, V-outラベル用スペース確保
y_top = 100
y_mid = 225
y_bot = 350

# 電源ライン
draw.line((x_left, y_top, x_right, y_top), fill=line_color, width=4) # V-in
# グランドライン
draw.line((x_left, y_bot, x_right, y_bot), fill=line_color, width=4) # GND

# 抵抗の描画 (サイズを少し大きく)
res_w = 50
res_h = 70

# R1
draw.rectangle((x_left - res_w/2, y_mid - res_h*1.3, x_left + res_w/2, y_mid - res_h*0.3), fill=res_color)
# R2
draw.rectangle((x_left - res_w/2, y_mid + res_h*0.3, x_left + res_w/2, y_mid + res_h*1.3), fill=res_color)

# 接続線
draw.line((x_left, y_top, x_left, y_mid - res_h*1.3), fill=line_color, width=3) # V-in to R1
draw.line((x_left, y_mid - res_h*0.3, x_left, y_mid + res_h*0.3), fill=line_color, width=3) # R1 to R2
draw.line((x_left, y_mid + res_h*1.3, x_left, y_bot), fill=line_color, width=3) # R2 to GND

# 出力線
draw.line((x_left, y_mid, x_right, y_mid), fill=line_color, width=3) # Mid to V-out

# グランドシンボル
draw.line((x_right - 40, y_bot, x_right + 40, y_bot), fill=line_color, width=3)
draw.line((x_right - 25, y_bot + 12, x_right + 25, y_bot + 12), fill=line_color, width=3)
draw.line((x_right - 10, y_bot + 24, x_right + 10, y_bot + 24), fill=line_color, width=3)

# --- ラベルの追加 (特大フォント) ---

# R1, R2ラベル (左側、大きく)
draw.text((x_left - 130, y_mid - res_h - 20), "R1", fill=line_color, font=font_lg)
draw.text((x_left - 130, y_mid + res_h*0.3 + 10), "R2", fill=line_color, font=font_lg)

# V-in, V-outラベル (右側、特大・青色で強調)
# テキストのベースライン合わせで座標を微調整
draw.text((x_right - 230, y_top - 65), "V-in", fill=label_color, font=font_xl)
draw.text((x_right - 230, y_mid - 65), "V-out", fill=label_color, font=font_xl)

# GNDラベル (右下、大きく)
draw.text((x_right - 60, y_bot + 35), "GND", fill=line_color, font=font_lg)

# 計算式のテキスト (下部、見やすく)
draw.text((width/2 - 250, height - 40), "V-out = V-in × R2 / (R1 + R2)", fill='#555', font=font_md)

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
st.caption("※分圧後のV-outは、V-inとGNDの間の電位差となります。GNDレベルの変動には注意してください。")

# --- 画面下部中央に「戻る」ボタンを配置 ---
st.markdown("---")  # 区切り線
col1, col2, col3 = st.columns([1, 1, 1])

with col2:  # 中央の列を使用
    # 水色のアイコン（🏠）と「戻る」を表示するボタン
    if st.link_button("🏠\n\n戻る", "https://menue3-pkwzfkwnoxnnuljkqg7mdt.streamlit.app/", use_container_width=True):
        pass

# ボタンの色（水色）を調整するカスタム設定
st.markdown("""
    <style>
    div.stLinkButton > a {
        background-color: #00BFFF !important; /* 水色（DeepSkyBlue） */
        color: white !important;
        border-radius: 10px;
        text-align: center;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)
