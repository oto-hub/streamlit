import streamlit as st
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
from deep_translator import GoogleTranslator
from geopy.geocoders import Nominatim

# グラフの日本語対応
rcParams['font.family'] = 'Meiryo'

COUNTRY_MAP = {
    "JP": "日本", "US": "アメリカ合衆国", "ES": "スペイン", "FR": "フランス", 
    "DE": "ドイツ", "CN": "中国", "KR": "韓国", "IT": "イタリア", 
    "GB": "イギリス", "CA": "カナダ", "AU": "オーストラリア", "IN": "インド", 
    "BR": "ブラジル", "MX": "メキシコ", "RU": "ロシア"
}

WIND_DIRECTIONS = [
    "北", "北北東", "北東", "東北東", "東", 
    "東南東", "南東", "南南東", "南", 
    "南南西", "南西", "西南西", "西", 
    "西北西", "北西", "北北西", "北"
]

def main():
    st.title("天気情報アプリ")
    API_KEY = st.text_input('APIキーを入力してください', type='password', key="api_key_input")
    city = st.text_input("都市名を入力してください", key="city_input")
    option = st.selectbox("表示する天気を選んでください", ("今日の天気", "５日間の天気"), key="weather_option")

    if city:
        translated_city = translate_city(city)
        if option == "今日の天気":
            display_today_weather(translated_city, city, API_KEY)
        elif option == "５日間の天気":
            display_five_day_weather(translated_city, city, API_KEY)

# 日本語を英語に変換
def translate_city(city):
    return GoogleTranslator(source='auto', target='en').translate(city)

# 今日の天気データを表示
def display_today_weather(english_city, japanese_city, API_KEY):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={english_city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "国": COUNTRY_MAP.get(data['sys']['country'], "不明"),
            "都市": japanese_city,
            "天候": GoogleTranslator(source='auto', target='ja').translate(data['weather'][0]['description']),
            "気温": f"{data['main']['temp']}°C",
            "体感温度": f"{data['main']['feels_like']}°C",
            "最高気温": f"{data['main']['temp_max']}°C",
            "最低気温": f"{data['main']['temp_min']}°C",
            "気圧": f"{data['main']['pressure']} hPa",
            "湿度": f"{data['main']['humidity']}%",
            "風速": f"{data['wind']['speed']} m/s",
            "風向き": get_wind_direction(data['wind']['deg'])
        }

        if 'gust' in data['wind']:
            weather_data["最大瞬間風速"] = f"{data['wind']['gust']} m/s"

        for key, value in weather_data.items():
            st.write(f"{key}：{value}")
        
    else:
        st.error("天気情報を取得できませんでした。都市名を確認してください。")

# ５日間の天気データをグラフで表示
def display_five_day_weather(english_city, japanese_city, API_KEY):
    lat, lon = get_lat_lon(english_city)
    if lat is None or lon is None:
        st.error(f"{japanese_city} の緯度経度を取得できませんでした。")
        return

    forecast_data = get_five_day_forecast(lat, lon, API_KEY)
    if not forecast_data:
        return

    grouped_data = group_forecast_data_by_day(forecast_data)

    for date, forecasts in grouped_data.items():
        st.title(f"{date}の天気")
        display_weather_graph(forecasts)

# 緯度と経度を取得
def get_lat_lon(city_name):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    return None, None

# ５日間の天気データを取得
def get_five_day_forecast(lat, lon, API_KEY):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"lat": lat, "lon": lon, "units": "metric", "appid": API_KEY}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get('list', [])
    st.error(f"天気情報を取得できませんでした。エラーコード: {response.status_code}")
    return []

# 日ごとに分けた天気データを取得
def group_forecast_data_by_day(forecast_list):
    grouped = {}
    for forecast in forecast_list:
        date = forecast['dt_txt'].split(" ")[0]
        if date not in grouped:
            grouped[date] = []
        grouped[date].append(forecast)
    return grouped

# 天気グラフの作成・表示
def display_weather_graph(forecasts):
    timestamps = [datetime.strptime(f['dt_txt'], "%Y-%m-%d %H:%M:%S") for f in forecasts]
    temperatures = [f['main']['temp'] for f in forecasts]
    precipitation_chances = [f['pop'] * 100 for f in forecasts]
    weather_descriptions = [GoogleTranslator(source='auto', target='ja').translate(f['weather'][0]['description']) for f in forecasts]

    fig, ax = plt.subplots(figsize=(15, 6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.plot(timestamps, temperatures, marker='o', linestyle='-', color='b', label="気温")
    ax.set_ylabel("気温 (°C)", fontsize=12, color='b')
    ax.grid()

    ax2 = ax.twinx()
    ax2.bar(timestamps, precipitation_chances, width=0.09, color='c', alpha=0.6, label="降水確率")
    ax2.set_ylabel("降水確率 (%)", fontsize=12, color='c')

    st.pyplot(fig)

def get_wind_direction(degrees):
    idx = round(degrees / 22.5) % 16
    return WIND_DIRECTIONS[idx]

main()
