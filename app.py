import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
import math

# --- 1. 初期設定とデータベース ---
st.set_page_config(page_title="MLC - MyLipCode -", layout="centered")
st.title("💄 MLC - MyLipCode -")

# --- データベース ---
LIP_DATABASE = [
    {"name": "王道コーラルピンク", "color": (255, 102, 102), "image":"", "link":"" },
    {"name": "大人なテラコッタ", "color": (153, 51, 0), "image":"", "link": ""},
    {"name": "透明感ラズベリー", "color": (204, 0, 102), "image":"", "link":""},
    {"name": "華やか朱色レッド", "color": (255, 69, 0), "image":"", "link":"" },
    {"name": "落ち着いたベージュ", "color": (210, 180, 140), "image":"", "link": ""},
    {"name": "Ririmew_muted sheer tint_02pink fondue", "color": (193, 90, 93), "image": "https://shop.r10s.jp/lilyanna/cabinet/gazou/r/ririmew_tint_n_09.jpg", "link": "https://hb.afl.rakuten.co.jp/ichiba/52e52694.a8b522e5.52e52695.0c1b728d/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Flilyanna%2Fririmew-tint%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
]

# --- 2. 色の距離を計算する関数 ---
def color_distance(c1, c2):
    return math.sqrt(
        (c1[0] - c2[0]) ** 2 +
        (c1[1] - c2[1]) ** 2 +
        (c1[2] - c2[2]) ** 2
    )

# --- 3. ファイルアップロード ---
uploaded_file = st.file_uploader("リップの写真をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_w, img_h = image.size

    st.write("画像の中のリップ部分をクリックしてください")
    value = streamlit_image_coordinates(image, key="coords")

    if value:
        # クリック座標を元画像サイズに変換
        px = int(value["x"] * (img_w / value["width"]))
        py = int(value["y"] * (img_h / value["height"]))

        # クリック位置の色を取得
        r, g, b = image.getpixel((px, py))
        selected_color = (r, g, b)
        hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)

        st.divider()
        st.subheader("📍 抽出した色")
        st.write(f"RGB: ({r}, {g}, {b})")
        st.code(hex_color)
        st.color_picker("色の確認", hex_color, disabled=True)

        # データベース内の各リップとの距離を計算
        results = []
        for lip in LIP_DATABASE:
            dist = color_distance(selected_color, lip["color"])
            results.append({
                "name": lip["name"],
                "color": lip["color"],
                "link": lip["link"],
                "distance": dist
            })

        # 距離が近い順に並べて上位5件取得
        top5 = sorted(results, key=lambda x: x["distance"])[:5]

        st.divider()
        st.subheader("💋 似ている色のリップ TOP5")

        for i, lip in enumerate(top5, 1):
            lr, lg, lb = lip["color"]
            lip_hex = '#{:02x}{:02x}{:02x}'.format(lr, lg, lb)

            st.markdown(f"### {i}. {lip['name']}")
            st.image(lip["image"], width=150)
            st.markdown(
                f"""
                <div style="
                    background-color:{lip_hex};
                    width:80px;
                    height:30px;
                    border-radius:6px;
                    border:1px solid #ccc;
                    margin-bottom:8px;
                "></div>
                """,
                unsafe_allow_html=True
            )
            st.write(f"RGB: {lip['color']}")
            st.markdown(f"[商品リンクを見る]({lip['link']})")
            st.write("---")