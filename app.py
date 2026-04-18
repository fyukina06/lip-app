import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
import math

# --- 1. 初期設定とデータベース ---
st.set_page_config(page_title="MyLipCode", layout="centered")
st.markdown("""
<h2 style='text-align: center; color:#ff4b6e; margin-bottom:0;'>👩‍❤️‍💋‍👨plimy </h2>
<p style='text-align: center; font-size:14px; color:#666; margin-top:5px;'>
- リップカラー診断アプリ -</p>
""", unsafe_allow_html=True)

# --- データベース ---
LIP_DATABASE = [
    {"name": "クレド・ポー・ボーテ_ルージュアレーブル_5 Camellia", "color": (226, 96, 84), 
     "link":"https://hb.afl.rakuten.co.jp/ichiba/52e56f85.b110c142.52e56f86.1714c1d5/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Friri-shop0707%2F4514254992449%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9" },
    {"name": "ケイト_リップモンスター_03 陽炎", "color": (208, 121, 94), 
     "link": "https://hb.afl.rakuten.co.jp/ichiba/4be181e5.85aa38ae.4be181e6.80bc2ede/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fsian%2F820186%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
    {"name": "ケイト_リップモンスター_05 ダークフィグ", "color": (197, 100, 93), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/4be17cec.5f1de9c8.4be17ced.6e0541fe/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmatsuya-cosme%2F82024%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
    {"name": "peripera_Gリップグロス_06 メイド イット", 
    "color": (173, 83, 82), 
     "link":"https://hb.afl.rakuten.co.jp/ichiba/4be50bb9.be99ec7e.4be50bba.38ca64b6/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2F0101marui%2Fce016292060101%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9" },
    {"name": "AMUSE_BEBE TINT_バニラローズ", "color": (183, 68, 83), 
    "link": "https://hb.afl.rakuten.co.jp/ichiba/52e58eed.23c7c9c4.52e58eee.cee59967/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fshop-lady%2Famuse-bebe-tint%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
    {"name": "Ririmew_muted sheer tint_02 pink fondue", "color": (193, 90, 93), 
    "link": "https://hb.afl.rakuten.co.jp/ichiba/52e52694.a8b522e5.52e52695.0c1b728d/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Flilyanna%2Fririmew-tint%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
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

    display_image = image.copy()
    display_image.thumbnail((650, 650))

    st.write("画像の中のリップ部分をクリックしてください")
    
    value = streamlit_image_coordinates(display_image, key="coords")

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
        st.markdown("""<h3 style='text-align: center; font-size:15px;'>
        👧 似ている色のリップ TOP5
        </h3> 
        """, unsafe_allow_html=True)

        medals = ["🥇", "🥈", "🥉"]

        for i, lip in enumerate(top5):
            if i < 3:
                rank = medals[i]
            else:
                rank = f"{i+1}."

            parts = lip["name"].split("_")
            brand = parts[0] if len(parts) > 0 else ""
            item_name = parts[1] if len(parts) > 1 else ""
            shade = parts[2] if len(parts) > 2 else ""

            r, g, b = lip["color"]
            hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)

            # 1行目：順位 + ブランド
            st.markdown(
                f"<div style='font-size:16px; color:#888; font-weight:600;'>{rank} {brand}</div>",
                unsafe_allow_html=True
            )

            # 2行目：商品名と色丸
            col1, col2 = st.columns([10, 1])

            with col1:
                st.markdown(
                    f"<div style='font-size:26px; font-weight:700; line-height:1.4;'>{item_name} {shade}</div>",
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f"""
        <div style='
            width:18px;
            height:18px;
            border-radius:50%;
            background-color:{hex_color};
            margin-top:12px;
        '></div>
        """,
                    unsafe_allow_html=True
                )

            st.link_button("👉 商品を見る", lip["link"], use_container_width=True)
            st.write("---")

#写真拡大機能
#タイトルの文字大きさ小さくする