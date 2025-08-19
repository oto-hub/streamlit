import streamlit as st
from urllib.request import urlopen
import json
from deep_translator import GoogleTranslator
from datetime import date, timedelta
from random import choice

def main():
    API_KEY = 'BxovKYfmCAfRy9ADfwDZP5p2CwAkgeUtctb1QfkI'
    if not API_KEY:
        st.warning("APIキーを入力してください。")
        return

    # デフォルトの日付範囲
    start_day = date(1995, 6, 16)
    end_day = date.today() - timedelta(1)

    if 'select_date' not in st.session_state:
        st.session_state.select_date = end_day

    st.title('NASAの天文写真アーカイブ')
    st.write('毎日、宇宙のさまざまな画像や動画が簡単な説明とともに紹介されます。')

    # 日付選択機能
    disp_date_selector(start_day, end_day)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.select_date > start_day:
            st.button('前の日', on_click=change_date, args=(-1,))
    with col2:
        st.button('ランダムな日付', on_click=random_date, args=(start_day, end_day))
    with col3:
        if st.session_state.select_date < end_day:
            st.button('次の日', on_click=change_date, args=(1,))

    # 選択された日付のデータ取得
    with st.spinner("データを取得中..."):
        data = fetch_apod_data(API_KEY, st.session_state.select_date)

    if data:
        display_content(data)
    else:
        st.error("データを取得できませんでした。APIキーや日付を確認してください。")


def disp_date_selector(start_day, end_day):
    """年・月・日を選択するセレクトボックスを表示"""
    select_date = st.session_state.select_date

    year = st.selectbox('年', range(start_day.year, end_day.year + 1), index=select_date.year - start_day.year)
    month = st.selectbox('月', range(1, 13), index=select_date.month - 1)
    day = st.selectbox('日', range(1, 32), index=select_date.day - 1)

    try:
        st.session_state.select_date = date(year, month, day)
    except ValueError:
        st.warning("無効な日付です。再選択してください。")


def change_date(offset):
    """選択された日付を前後に変更"""
    st.session_state.select_date += timedelta(days=offset)


def random_date(start_day, end_day):
    """ランダムな日付を選択"""
    st.session_state.select_date = start_day + timedelta(days=choice(range((end_day - start_day).days + 1)))


def fetch_apod_data(api_key, selected_date):
    """NASA APOD APIからデータを取得"""
    try:
        api_url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={selected_date}"
        with urlopen(api_url) as response:
            if response.getcode() == 200:
                data = json.load(response)
                data['trans_title'] = GoogleTranslator(source='en', target='ja').translate(data['title'])
                data['trans_explanation'] = GoogleTranslator(source='en', target='ja').translate(data['explanation'])
                return data
    except Exception as e:
        st.error(f"データ取得中にエラーが発生しました: {e}")
    return None


def display_content(data):
    """データを表示"""
    st.header(data['trans_title'])
    st.subheader(f"原題: {data['title']}")

    if data['media_type'] == 'image':
        st.image(data['url'], caption=f"出典: {data.get('copyright', 'NASA')}")
    elif data['media_type'] == 'video':
        st.video(data['url'])
    else:
        st.warning("このメディアタイプはサポートされていません。")

    # 説明の表示
    explanation_type = st.radio("説明の表示形式", ["日本語訳", "原文"])
    if explanation_type == "日本語訳":
        st.write(data['trans_explanation'])
    else:
        st.write(data['explanation'])

if __name__ == "__main__":
    main()
