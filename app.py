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
    #ケイト_リップモンスター
     {"name": "ケイト_リップモンスター_01 欲望の塊", "color": (221, 96, 102), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f657fe.9080b630.52f657ff.0dc4fc88/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fjackknife%2Faj47376c26e070f9%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
     {"name": "ケイト_リップモンスター_02 Pink banana", "color": (207, 94, 88), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/4be17cec.5f1de9c8.4be17ced.6e0541fe/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmatsuya-cosme%2F82018%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
    {"name": "ケイト_リップモンスター_03 陽炎", "color": (208, 121, 94), 
     "link": "https://hb.afl.rakuten.co.jp/ichiba/4be181e5.85aa38ae.4be181e6.80bc2ede/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fsian%2F820186%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
     {"name": "ケイト_リップモンスター_04 パンプキンワイン", "color": (205, 106, 74), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f657fe.9080b630.52f657ff.0dc4fc88/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fjackknife%2Faj47377bbcc1b04a%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
    {"name": "ケイト_リップモンスター_05 ダークフィグ", "color": (197, 100, 93), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/4be17cec.5f1de9c8.4be17ced.6e0541fe/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmatsuya-cosme%2F82024%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
     {"name": "ケイト_リップモンスター_06 2:00AM", "color": (195, 92, 93), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f66530.a80785fa.52f66531.812ef570/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Ffuture00store%2F0226%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
     {"name": "ケイト_リップモンスター_07 ラスボス", "color": (195, 92, 87), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/4be17cec.5f1de9c8.4be17ced.6e0541fe/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmatsuya-cosme%2F82030%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
     {"name": "ケイト_リップモンスター_08 モーヴシャワー", "color": (208, 114, 115), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f66dde.2f6d4c73.52f66ddf.b3f47dff/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmorro%2F20250607142646_94%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
     {"name": "ケイト_リップモンスター_09 水晶玉のマダム", "color": (208, 85, 77), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f670e0.715782af.52f670e1.95c074c2/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fs4gshop%2F20250507145406_95%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
     {"name": "ケイト_リップモンスター_10 地底探索", "color": (219, 115, 88), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f670e0.715782af.52f670e1.95c074c2/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fs4gshop%2F20250507145400_95%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
     {"name": "ケイト_リップモンスター_11 5:00AM", "color": (183, 108, 87), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f66dde.2f6d4c73.52f66ddf.b3f47dff/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmorro%2F20250607142659_94%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
     {"name": "ケイト_リップモンスター_12 誓いのルビー", "color": (207, 76, 84), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f67c77.b8203543.52f67c78.06c26b9a/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fshopypp22%2F20251115-963-1%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
     {"name": "ケイト_リップモンスター_13 3:00AMの微酔", "color": (201, 81, 80), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f680de.160ca656.52f680df.1cef7028/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2F24exp%2Fb09tqtfwfs%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
    {"name": "ケイト_リップモンスター_14 憧れの日光浴", "color": (222, 103, 63), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f684c6.9b2f16f8.52f684c7.0365b5b1/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fizuka%2Faj400943d7357135%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
    {"name": "ケイト_リップモンスター_15 綿雲33000ft", "color": (216, 109, 93), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f6886b.8bac0b2f.52f6886c.d4b4ab9f/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fdaikisone%2Fkate4687%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
    {"name": "ケイト_リップモンスター_16 100億haの砂海", "color": (195, 107, 67), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f6886b.8bac0b2f.52f6886c.d4b4ab9f/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fdaikisone%2Fkate4694%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
    {"name": "ケイト_リップモンスター_17 神秘のローズ園", "color": (207, 110, 103), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f6886b.8bac0b2f.52f6886c.d4b4ab9f/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fdaikisone%2Fkate4700%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
    {"name": "ケイト_リップモンスター_18 とろけ落ちる蜜桃", "color": (211, 113, 100), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f6a61e.b2fe60e0.52f6a61f.61ad65d4/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fcosme-village%2F4973167049846-c%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
    {"name": "ケイト_リップモンスター_19 口染めライチの甘い罠", "color": (200, 114, 99), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/4be181e7.1c1d6c8c.4be181e8.43c18085/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fyayoi-cosme%2Fka049853%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},
    {"name": "ケイト_リップモンスター_20 いたずらベリーの道標", "color": (187, 80, 86), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f6a61e.b2fe60e0.52f6a61f.61ad65d4/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fcosme-village%2F4973167049860-c%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"},

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
        st.markdown("""<h3 style='text-align: center; font-size:18px;'>
        📍 抽出した色
        </h3> 
        """, unsafe_allow_html=True)
        st.write(f"RGB: ({r}, {g}, {b})")
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
        top3 = sorted(results, key=lambda x: x["distance"])[:3]

        st.divider()
        st.markdown("""<h3 style='text-align: center; font-size:18px;'>
        👧 似ている色味のリップ TOP3
        </h3> 
        """, unsafe_allow_html=True)

        st.markdown("""
        <p style='text-align: center; font-size:13px; color:#666;'>
        ※写真や光の加減によって見え方が変わるため、近い色味の候補を表示しています。
        </p>
        """, unsafe_allow_html=True)

        medals = ["🥇", "🥈", "🥉"]

        for i, lip in enumerate(top3):
            if i < 3:
                rank = medals[i]

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
                    f"<div style='font-size:22px; font-weight:700; line-height:1.4;'>{item_name} {shade}</div>",
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
#イエベブルべ
#値段で絞る
#タグ、プチプラ、青みより、ツヤ、明るいとかつける
#お気に入り保存
