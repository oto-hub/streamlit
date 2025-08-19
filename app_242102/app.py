import streamlit as st
import pytz
from datetime import datetime
from PIL import Image  # 画像処理ライブラリ

# 各都市のタイムゾーンと国旗のファイル名を辞書で定義
city_timezones = {
    "東京": ["Asia/Tokyo", "app_242102/japan.png"],
    "ロンドン": ["Europe/London", "app_242102/united-kingdom.png"],
    "ニューヨーク": ["America/New_York", "app_242102/usa.png"],
    "上海": ["Asia/Shanghai", "app_242102/china.png"],
    "リオデジャネイロ": ["America/Sao_Paulo", "app_242102/brazil.png"],
    "モスクワ": ["Europe/Moscow", "app_242102/russia.png"],
    "シドニー": ["Australia/Sydney", "app_242102/australia.png"],
    "ベルリン": ["Europe/Berlin", "app_242102/germany.png"],
    "ポルトガル": ["Europe/Lisbon", "app_242102/portugal.png"]
}

def get_world_time(tokyo_time_str):
    try:
        tokyo_time = datetime.strptime(tokyo_time_str, "%Y-%m-%d %H:%M:%S")
        tokyo_tz = pytz.timezone('Asia/Tokyo')
        tokyo_dt = tokyo_tz.localize(tokyo_time)

        for city, (timezone, flag_file) in city_timezones.items():
            local_tz = pytz.timezone(timezone)
            local_dt = tokyo_dt.astimezone(local_tz)
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(flag_file, width=50)
            with col2:
                st.write(f"{city}: {local_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    except ValueError:
        st.error("日付と時刻の形式が不正です。YYYY-MM-DD HH:MM:SSの形式で入力してください。")

def main():
    st.title("世界の時刻表示")

    tokyo_time = st.text_input("東京の時間を入力してください(YYYY-MM-DD HH:MM:SS)")

    if st.button("変換"):
        get_world_time(tokyo_time)

if __name__ == "__main__":
    main()