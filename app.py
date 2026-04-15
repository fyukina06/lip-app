import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
import numpy as np
from sklearn.cluster import KMeans
import math

# --- 1. 初期設定とデータベース ---
st.set_page_config(page_title="LCC - LipColorCode", layout="centered")
st.title("💄 LCC - ハイブリッド解析")

if 'points' not in st.session_state:
    st.session_state.points = []

# --- データベース　（そのまま保持）　---
LIP_DATABASE = [
    {"name":"王道コーラルピンク","color":(255,102,102)},
    {"name":"大人なテラコッタ","color":(153,51,0)},
    {"name":"透明感ラズベリー","color":(204,0,102)},
    {"name":"華やか朱色レッド","color":(255,69,0)},
    {"name":"落ち着いたベージュ","color":(210,180,140)},
    {"name":"Ririmew_muted sheer tint_02pink fondue","color":(193,90,93)},
]

# --- 2. モード選択とリセット ---
mode = st.radio("モードを選択", ["1点抽出 (DB登録用)", "範囲指定 (パレット解析)"], horizontal=True)

if st.button("リセット"):
    st.session_state.points = []
    st.rerun()

# --- 3. ファイルアップロード ---
uploaded_file = st.file_uploader("写真をアップロード", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_w, img_h = image.size
    
    # 画像を表示してクリックを取得
    # keyにmodeを入れることで、モード切り替え時のバグを防ぎます
    value = streamlit_image_coordinates(image, key=f"coords_{mode}")

    if value:
        # 座標計算
        px = int(value["x"] * (img_w / value["width"]))
        py = int(value["y"] * (img_h / value["height"]))
        current_click = (px, py)

        # --- A. 1点抽出モード ---
        if mode == "1点抽出 (DB登録用)":
            r, g, b = image.getpixel(current_click)
            st.divider()
            st.success(f"📍 抽出成功！ RGB: ({r}, {g}, {b})")
            # データベースにコピペしやすい形式で表示
            st.code(f'{{"name": "商品名", "color": ({r}, {g}, {b})}},', language="python")
            st.color_picker("色の確認", '#{:02x}{:02x}{:02x}'.format(r, g, b))

        # --- B. 範囲指定モード ---
        else:
            if len(st.session_state.points) < 2:
                # 重複登録を防ぐ
                if not st.session_state.points or st.session_state.points[-1] != current_click:
                    st.session_state.points.append(current_click)
                    st.rerun()

    # 範囲指定の解析実行
    if mode == "範囲指定 (パレット解析)" and len(st.session_state.points) == 2:
        p1, p2 = st.session_state.points
        left, right = sorted([p1[0], p2[0]])
        top, bottom = sorted([p1[1], p2[1]])
        
        if right - left > 5 and bottom - top > 5:
            roi = image.crop((left, top, right, bottom))
            st.image(roi, caption="解析範囲", width=150)
            
            # k-meansでパレット作成
            pixels = np.array(roi.resize((50, 50))).reshape(-1, 3)
            kmeans = KMeans(n_clusters=5, n_init=10).fit(pixels)
            palette = kmeans.cluster_centers_.astype(int)
            
            st.subheader("🎨 カラーパレット")
            cols = st.columns(5)
            for i, color in enumerate(palette):
                hex_c = '#{:02x}{:02x}{:02x}'.format(*color)
                cols[i].markdown(f'<div style="background-color:{hex_c};height:50px;border-radius:5px;"></div>', unsafe_allow_html=True)
                cols[i].caption(hex_c)