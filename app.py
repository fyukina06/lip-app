import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
import math
import numpy as np
import colorsys
from typing import Tuple

# --- 1. 初期設定とデータベース ---
st.set_page_config(page_title="MyLipCode", layout="centered")
st.markdown("""
<h2 style='text-align: center; color:#ff4b6e; margin-bottom:0;'>👩‍❤️‍💋‍👨plimy </h2>
<p style='text-align: center; font-size:14px; color:#666; margin-top:5px;'>
- 写真から似ているリップを見つけるカラー診断アプリ -</p>
""", unsafe_allow_html=True)

st.markdown("""
手持ちのリップの写真から色を分析して、 
似ている色味のリップ候補を見つけられるWebアプリです。
ブルべ・イエベなどの色味の傾向も参考として表示します。
""")

st.markdown("""<h3 style='text-align: center; font-size:18px;'>
        使い方
        </h3> 
        """, unsafe_allow_html=True)
st.markdown("""
1. リップの写真をアップロード  
2. リップ部分をタップ  
3. 肌色部分をタップ  
4. 近い色味のリップ候補をチェック
""")

st.markdown("""<h3 style='text-align: center; font-size:18px;'>
        ご利用時のポイント
        </h3> 
        """, unsafe_allow_html=True)
st.markdown("""
- 明るい場所で撮影した写真がおすすめです  
- 光の当たり方によって色の見え方は変わります  
- 診断結果は「近い色味の候補」として表示しています
""")

# --- データベース ---
LIP_DATABASE = [
    {"name": "クレド・ポー・ボーテ_ルージュアレーブル_5 Camellia", "color": (187, 56, 63), 
     "link":"https://hb.afl.rakuten.co.jp/ichiba/52e56f85.b110c142.52e56f86.1714c1d5/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Friri-shop0707%2F4514254992449%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
     "price_type":"デパコス" },
    #ケイト_リップモンスター
     {"name": "ケイト_リップモンスター_01 欲望の塊", "color": (203, 93, 114), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f657fe.9080b630.52f657ff.0dc4fc88/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fjackknife%2Faj47376c26e070f9%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
     {"name": "ケイト_リップモンスター_02 Pink banana", "color": (195, 98, 106), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/4be17cec.5f1de9c8.4be17ced.6e0541fe/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmatsuya-cosme%2F82018%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
    {"name": "ケイト_リップモンスター_03 陽炎", "color": (192, 112, 100), 
     "link": "https://hb.afl.rakuten.co.jp/ichiba/4be181e5.85aa38ae.4be181e6.80bc2ede/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fsian%2F820186%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
     "price_type":"プチプラ" },
     {"name": "ケイト_リップモンスター_04 パンプキンワイン", "color": (181, 87, 69), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f657fe.9080b630.52f657ff.0dc4fc88/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fjackknife%2Faj47377bbcc1b04a%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
    {"name": "ケイト_リップモンスター_05 ダークフィグ", "color": (179, 100, 101), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/4be17cec.5f1de9c8.4be17ced.6e0541fe/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmatsuya-cosme%2F82024%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
     {"name": "ケイト_リップモンスター_06 2:00AM", "color": (165, 66, 87), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f66530.a80785fa.52f66531.812ef570/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Ffuture00store%2F0226%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
     {"name": "ケイト_リップモンスター_07 ラスボス", "color": (180, 83, 93), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/4be17cec.5f1de9c8.4be17ced.6e0541fe/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmatsuya-cosme%2F82030%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
     {"name": "ケイト_リップモンスター_08 モーヴシャワー", "color": (183, 101, 118), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f66dde.2f6d4c73.52f66ddf.b3f47dff/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmorro%2F20250607142646_94%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
     {"name": "ケイト_リップモンスター_09 水晶玉のマダム", "color": (189, 69, 75), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f670e0.715782af.52f670e1.95c074c2/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fs4gshop%2F20250507145406_95%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
     {"name": "ケイト_リップモンスター_10 地底探索", "color": (183, 79, 69), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f670e0.715782af.52f670e1.95c074c2/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fs4gshop%2F20250507145400_95%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
     {"name": "ケイト_リップモンスター_11 5:00AM", "color": (170, 99, 89), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f66dde.2f6d4c73.52f66ddf.b3f47dff/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmorro%2F20250607142659_94%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
     {"name": "ケイト_リップモンスター_12 誓いのルビー", "color": (189, 74, 92), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f67c77.b8203543.52f67c78.06c26b9a/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fshopypp22%2F20251115-963-1%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
     {"name": "ケイト_リップモンスター_13 3:00AMの微酔", "color": (185, 94, 101), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f680de.160ca656.52f680df.1cef7028/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2F24exp%2Fb09tqtfwfs%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
    {"name": "ケイト_リップモンスター_14 憧れの日光浴", "color": (201, 124, 107), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f684c6.9b2f16f8.52f684c7.0365b5b1/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fizuka%2Faj400943d7357135%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
    {"name": "ケイト_リップモンスター_15 綿雲33000ft", "color": (194, 104, 101), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f6886b.8bac0b2f.52f6886c.d4b4ab9f/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fdaikisone%2Fkate4687%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
    {"name": "ケイト_リップモンスター_16 100億haの砂海", "color": (181, 100, 69), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f6886b.8bac0b2f.52f6886c.d4b4ab9f/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fdaikisone%2Fkate4694%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
    {"name": "ケイト_リップモンスター_17 神秘のローズ園", "color": (183, 95, 95), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f6886b.8bac0b2f.52f6886c.d4b4ab9f/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fdaikisone%2Fkate4700%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
    {"name": "ケイト_リップモンスター_18 とろけ落ちる蜜桃", "color": (198, 109, 105), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f6a61e.b2fe60e0.52f6a61f.61ad65d4/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fcosme-village%2F4973167049846-c%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
    {"name": "ケイト_リップモンスター_19 口染めライチの甘い罠", "color": (181, 99, 96), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/4be181e7.1c1d6c8c.4be181e8.43c18085/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fyayoi-cosme%2Fka049853%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
    {"name": "ケイト_リップモンスター_20 いたずらベリーの道標", "color": (171, 74, 88), 
    "link":"https://hb.afl.rakuten.co.jp/ichiba/52f6a61e.b2fe60e0.52f6a61f.61ad65d4/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fcosme-village%2F4973167049860-c%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },

    {"name": "peripera_Gリップグロス_06 メイド イット", 
    "color": (121, 57, 64), 
     "link":"https://hb.afl.rakuten.co.jp/ichiba/4be50bb9.be99ec7e.4be50bba.38ca64b6/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2F0101marui%2Fce016292060101%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9" ,
     "price_type":"プチプラ" },
    {"name": "AMUSE_BEBE TINT_バニラローズ", "color": (159, 48, 55), 
    "link": "https://hb.afl.rakuten.co.jp/ichiba/52e58eed.23c7c9c4.52e58eee.cee59967/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fshop-lady%2Famuse-bebe-tint%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
    {"name": "Ririmew_muted sheer tint_02 pink fondue", "color": (172, 101, 117), 
    "link": "https://hb.afl.rakuten.co.jp/ichiba/52e52694.a8b522e5.52e52695.0c1b728d/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Flilyanna%2Fririmew-tint%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9",
    "price_type":"プチプラ" },
]

STANDARD_SKIN_RGB = (210, 180, 170)  # 仮の標準肌色。あとで調整してOK


def clamp(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(value, max_value))


def get_average_color(image: Image.Image, x: int, y: int, radius: int = 10) -> Tuple[int, int, int]:
    """
    クリック位置の周囲 radius px の平均RGBを返す
    """
    rgb_img = image.convert("RGB")
    arr = np.array(rgb_img)

    height, width = arr.shape[:2]

    x1 = clamp(x - radius, 0, width - 1)
    x2 = clamp(x + radius, 0, width - 1)
    y1 = clamp(y - radius, 0, height - 1)
    y2 = clamp(y + radius, 0, height - 1)

    region = arr[y1:y2 + 1, x1:x2 + 1]
    mean_rgb = region.mean(axis=(0, 1))

    r, g, b = [int(round(v)) for v in mean_rgb]
    return (r, g, b)


def adjust_lip_by_skin(
    lip_rgb: Tuple[int, int, int],
    skin_rgb: Tuple[int, int, int],
    standard_skin_rgb: Tuple[int, int, int] = STANDARD_SKIN_RGB
) -> Tuple[int, int, int]:
    """
    肌色との差分を使って、照明の影響を少し補正したリップ色を作る
    adjusted = lip - skin + standard_skin
    """
    adjusted = []
    for lip_c, skin_c, std_c in zip(lip_rgb, skin_rgb, standard_skin_rgb):
        value = lip_c - skin_c + std_c
        adjusted.append(clamp(int(round(value)), 0, 255))
    return tuple(adjusted)


def color_distance(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """
    RGBユークリッド距離
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def undertone_hint_from_skin_diff(
    lip_rgb: Tuple[int, int, int],
    skin_rgb: Tuple[int, int, int]
) -> str:
    """
    肌との差分からざっくり青み/黄みを出す
    """
    lr, lg, lb = lip_rgb
    sr, sg, sb = skin_rgb

    dr = lr - sr
    db = lb - sb

    if dr > db + 10:
        return "黄み・赤み寄り"
    elif db > dr + 10:
        return "青み寄り"
    else:
        return "中間寄り"

def get_depth_label(color):
    r, g, b = color
    brightness = (r + g + b) / 3

    if brightness < 120:
        return "深め"
    elif brightness > 180:
        return "淡め"
    else:
        return "中間"

def get_brightness_label(color):
    r, g, b = color
    brightness = (r + g + b) / 3

    if brightness >= 180:
        return "明るめ"
    elif brightness >= 130:
        return "中間"
    else:
        return "暗め"

def get_price_label(price_type):
    if price_type == "プチプラ":
        return "プチプラ"
    elif price_type == "デパコス":
        return "デパコス"
    else:
        return "価格帯不明"

def get_pc_label(color):
    r, g, b = color

    if b >= r + 10:
        return "ブルベ寄り"
    elif r >= b + 10:
        return "イエベ寄り"
    else:
        return "ニュートラル寄り"

# --- 3. ファイルアップロード ---
uploaded_file = st.file_uploader("リップの写真をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_w, img_h = image.size

    display_image = image.copy()
    display_image.thumbnail((350, 350))

    
    # セッションでクリック位置を保持
    if "lip_point" not in st.session_state:
        st.session_state.lip_point = None
    if "skin_point" not in st.session_state:
        st.session_state.skin_point = None

    st.info("""① まずリップ部分をクリック
            → ② 次に頬の肌部分をクリックしてください""")

    # --- リップ位置選択 ---
    st.write("① 画像の中のリップ部分をクリックしてください")
    lip_value = streamlit_image_coordinates(display_image, key="lip_coords")

    if lip_value:
        px = int(lip_value["x"] * (img_w / lip_value["width"]))
        py = int(lip_value["y"] * (img_h / lip_value["height"]))
        st.session_state.lip_point = (px, py)

    if st.session_state.lip_point:
        st.write(f"リップ位置: {st.session_state.lip_point}")

    # --- 肌位置選択 ---
    st.write("""② 肌色部分をクリックしてください
    （影の少ない場所がおすすめ）""")
    skin_value = streamlit_image_coordinates(display_image, key="skin_coords")

    if skin_value:
        px = int(skin_value["x"] * (img_w / skin_value["width"]))
        py = int(skin_value["y"] * (img_h / skin_value["height"]))
        st.session_state.skin_point = (px, py)

    if st.session_state.skin_point:
        st.write(f"肌位置: {st.session_state.skin_point}")

    # --- 両方そろったら解析 ---
    if st.session_state.lip_point and st.session_state.skin_point:
        lip_x, lip_y = st.session_state.lip_point
        skin_x, skin_y = st.session_state.skin_point

        # 周囲10px平均
        lip_avg = get_average_color(image, lip_x, lip_y, radius=10)
        skin_avg = get_average_color(image, skin_x, skin_y, radius=10)

        # 肌補正後の色
        adjusted_color = adjust_lip_by_skin(lip_avg, skin_avg)

        lip_hex = rgb_to_hex(lip_avg)
        skin_hex = rgb_to_hex(skin_avg)
        adjusted_hex = rgb_to_hex(adjusted_color)

        st.divider()
        st.markdown("""<h3 style='text-align: center; font-size:18px;'>
        📍 抽出した色
        </h3> 
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("リップ平均色")
            st.write(f"RGB: {lip_avg}")
            st.color_picker("リップ色", lip_hex, disabled=True, key="lip_color_picker")

        with col2:
            st.write("肌平均色")
            st.write(f"RGB: {skin_avg}")
            st.color_picker("肌色", skin_hex, disabled=True, key="skin_color_picker")

        with col3:
            st.write("補正後リップ色")
            st.write(f"RGB: {adjusted_color}")
            st.color_picker("補正色", adjusted_hex, disabled=True, key="adjusted_color_picker")

        selected_depth = get_depth_label(adjusted_color)
        selected_brightness = get_brightness_label(adjusted_color)
        selected_pc = get_pc_label(adjusted_color)
        selected_tone = undertone_hint_from_skin_diff(lip_avg, skin_avg)

        st.markdown("""<h3 style='text-align: center; font-size:18px;'>
        この色の特徴
        </h3> 
        """, unsafe_allow_html=True)
        st.write(f"・深さ：{selected_depth}")
        st.write(f"・明るさ：{selected_brightness}")
        st.write(f"・パーソナル傾向：{selected_pc}")
        st.write(f"・肌との差分：{selected_tone}")

        # データベース内の各リップとの距離を計算（補正後色で比較）
        results = []
        for lip in LIP_DATABASE:
            dist = color_distance(adjusted_color, lip["color"])
            results.append({
                "name": lip["name"],
                "color": lip["color"],
                "link": lip["link"],
                "distance": dist,
                "price_type": lip.get("price_type", "不明")
            })

        # 距離が近い順に並べて上位3件取得
        top3 = sorted(results, key=lambda x: x["distance"])[:3]

        st.divider()
        st.markdown("""<h3 style='text-align: center; font-size:18px;'>
        💄 近い色味のリップ候補 TOP3
        </h3> 
        """, unsafe_allow_html=True)

        st.markdown("""
        <p style='text-align: center; font-size:13px; color:#666;'>
        ※写真や光の加減によって見え方が変わるため、
        肌色との差分を使って近い候補を表示しています。
        </p>
        """, unsafe_allow_html=True)

        labels = ["🥇 一番近い候補", "🥈 近い候補", "🥉 近い候補"]

        for i, lip in enumerate(top3):
            rank = labels[i]

            parts = lip["name"].split("_")
            brand = parts[0] if len(parts) > 0 else ""
            item_name = parts[1] if len(parts) > 1 else ""
            shade = parts[2] if len(parts) > 2 else ""

            r, g, b = lip["color"]
            hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)

            depth_label = get_depth_label(lip["color"])
            brightness_label = get_brightness_label(lip["color"])
            pc_label = get_pc_label(lip["color"])
            price_label = get_price_label(lip.get("price_type", "不明"))

            tags = f"{price_label}｜{depth_label}｜{brightness_label}｜{pc_label}"

            st.markdown(
                f"<div style='font-size:16px; color:#888; font-weight:600;'>{rank} {brand}</div>",
                unsafe_allow_html=True
            )

            col1, col2 = st.columns([10, 1])

            with col1:
                st.markdown(
                    f"<div style='font-size:22px; font-weight:700; line-height:1.4;'>{item_name} {shade}</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div style='font-size:13px; color:#888; margin-top:4px;'>{tags}</div>",
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