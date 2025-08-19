import requests
import folium
import streamlit as st
from streamlit_folium import st_folium


def create_route_map(origin, destination, api_key, travel_mode):
    try:
        # Google Maps Directions APIを利用してルート情報を取得
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode={travel_mode}&key={api_key}"
        response = requests.get(url)
        data = response.json()

        # APIレスポンスのエラーチェック
        if response.status_code != 200 or "routes" not in data or len(data["routes"]) == 0:
            st.error("ルート情報が取得できませんでした。出発地や目的地、交通手段を確認してください。")
            return folium.Map(location=[36.7239949, 137.0904008], zoom_start=13), None  # 富山県をデフォルトに設定

        # ルート情報の取得
        route = data["routes"][0]
        overview_polyline = route["overview_polyline"]["points"]
        legs = route["legs"][0]

        # 出発地と目的地の緯度経度を取得
        start_location = legs["start_location"]
        end_location = legs["end_location"]
        start_lat, start_lng = start_location["lat"], start_location["lng"]
        end_lat, end_lng = end_location["lat"], end_location["lng"]

        # 所要時間を取得
        duration = legs["duration"]["text"]

        # 地図の中心を決定
        center_lat = (start_lat + end_lat) / 2
        center_lng = (start_lng + end_lng) / 2

        # Folium地図の作成
        map = folium.Map(location=[center_lat, center_lng], zoom_start=13)

        # 出発地と目的地のマーカーを追加
        folium.Marker(
            location=[start_lat, start_lng],
            popup=f"出発地: {origin}",
            icon=folium.Icon(color="green")
        ).add_to(map)

        folium.Marker(
            location=[end_lat, end_lng],
            popup=f"目的地: {destination}",
            icon=folium.Icon(color="red")
        ).add_to(map)

        # ルートのポリラインを地図に追加
        decoded_polyline = folium.PolyLine(
            locations=folium.utilities.decode_polyline(overview_polyline),
            color="blue",
            weight=5,
            opacity=0.8
        )
        map.add_child(decoded_polyline)

        return map, duration
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        return folium.Map(location=[36.7239949, 137.0904008], zoom_start=13), None


def main():
    st.title("地図ルート検索アプリ")

    # ユーザー入力フォーム
    origin = st.text_input("出発地を入力してください", "")
    destination = st.text_input("目的地を入力してください", "")
    Key=API_KEY= st.text_input("APIキーを入力してください", type="password")

    # 交通手段を選択
    travel_mode = st.radio(
        "交通手段を選択してください：",
        options=["自家用車", "電車", "徒歩"],
        index=0,
        horizontal=True
    )

    # モードに対応するGoogle APIのパラメータ
    mode_mapping = {"自家用車": "driving", "電車": "transit", "徒歩": "walking"}
    travel_mode_param = mode_mapping[travel_mode]

    # 入力が全て揃ったら地図を生成
    if API_KEY and origin and destination:
        map, duration = create_route_map(origin, destination,API_KEY, travel_mode_param)
        st_folium(map, width=800, height=600)

        # 所要時間を表示
        if duration:
            st.subheader("所要時間:")
            st.write(f"出発地から目的地までの所要時間は **{duration}** です。")
    else:
        st.error("出発地、または目的地を正しく入力してください。")


if __name__ == "__main__":
    main()