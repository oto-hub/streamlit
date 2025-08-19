import streamlit as st
import pandas as pd
from PIL import Image
import os

# メイン関数
def main():
    # ローカルファイルから画像を読み込む関数
    def load_image_from_path(path):
        try:
            if os.path.exists(path):
                return Image.open(path)
            else:
                return None
        except Exception as e:
            return None

    # CSVファイルの読み込み
    @st.cache_data
    def load_data(file_path):
        data = pd.read_csv(file_path)
        return data

    st.title("名字当てクイズ＆名字人口検索アプリ！")

    # CSVファイルを読み込む
    file_path = "app_242112/data.csv"  # CSVファイルのパスを指定
    data = load_data(file_path)

    st.sidebar.title("メニュー")
    option = st.sidebar.radio(
        "機能を選択してください", 
        ("名字検索", "名字当てクイズ"),  # 名字検索が先に表示されるよう変更
        index=0  # 初期値を「名字検索」に設定
    )

    if option == "名字検索":
        st.header("名字人口検索機能")
        st.write("日本の名字ランキング上位500位までのデータを検索できます。（データは正確でない可能性があります)")
        # 名字検索機能
        name_search = st.text_input("名字を入力してください:")

        if st.button("検索"):
            if name_search:
                # 名字で検索
                result = data[data["名字"] == name_search]
                if not result.empty:
                    population = result["推定人口数"].values[0]
                    rank = result["順位"].values[0]
                    img_path = result["img_path"].values[0]
                    st.success(f"名字: {name_search}\n推定人口数: {population}\n順位: {rank}")

                    if pd.notna(img_path):
                        face_image = load_image_from_path(img_path)
                        if face_image:
                            st.image(face_image, caption=f"名字「{name_search}」の画像")
                        #st.errorエラーっぽい表示
                        #st.warning危険っぽい表示
                        else:
                            st.error("この名字の画像が登録されていません。")
                    else:
                        st.warning("画像が登録されていません。")  
                else:
                    st.error("該当する名字が見つかりませんでした。")
            else:
                st.warning("名字を入力してください。")

        # データ表示
        if st.checkbox("名字ランキングデータを表示"):
            st.dataframe(data)

    elif option == "名字当てクイズ":
        st.header("名字当てクイズ！")
        st.write("画像を見て、その名字を予想してください。")
        st.write("画像が被る場合があります。(再読み込みでリセット)")
        # クイズの回数、下限値・上限値・初期値を選択
        num_quizzes = st.sidebar.slider("挑戦するクイズの回数", 1, 10, 3)

        # 画像のアスペクト比を設定するスライダー
        image_width = st.sidebar.slider("画像の縦横比変更（ピクセル）", 100, 800, 400)

        # 画像パスが空でないデータのみ
        quiz_data = data[data["img_path"].notna() & (data["img_path"] != "")]

        if quiz_data.empty:
            st.error("データが空です")
            return

        # セッション状態の初期化
        if "quiz_rows" not in st.session_state:
            st.session_state.quiz_rows = []

        # クイズの開始
        for i in range(num_quizzes):
            st.write(f"### クイズ {i+1}/{num_quizzes}")

            # セッションにクイズの行を保存（新しいクイズのみランダム選択）
            if len(st.session_state.quiz_rows) <= i:
                quiz_row = quiz_data.sample(1).iloc[0]
                st.session_state.quiz_rows.append(quiz_row)
            else:
                quiz_row = st.session_state.quiz_rows[i]

            correct_name = quiz_row["名字"]
            image_path = quiz_row["img_path"]

            # 画像の表示
            face_image = load_image_from_path(image_path)
            if face_image:
                st.image(face_image, caption="この人の名字は？", width=image_width)
            else:
                st.warning("追加している画像が少ないため、表示できません")

            # ユーザーが入力
            user_answer = st.text_input(f"クイズ {i+1}: 名字を入力してください:", key=f"answer_{i}")

            # 回答ボタン
            if st.button(f"クイズ {i+1} の回答を送信", key=f"submit_{i}"):
                if user_answer.strip() == correct_name:
                    st.success("正解！🎉")
                else:
                    st.error(f"不正解。正解は【 {correct_name} 】 です。")

            st.write("---")

        st.write("クイズ終了！挑戦してくれてありがとう！")
    
if __name__ == "__main__":
    main()
