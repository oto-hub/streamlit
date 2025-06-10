import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import cv2
from sklearn import datasets
from sklearn.neural_network import MLPClassifier

def main():
    # タイトルと説明
    st.title("手書き数字認識アプリ")

    # 数字データのロード
    digits = datasets.load_digits()
    X_train, y_train = digits.data, digits.target

    # サイドバーでモデルパラメータを設定
    st.sidebar.header("モデルパラメータ")
    tol = st.sidebar.selectbox("許容誤差 (tol)", [1e-8, 1e-6, 1e-4, 1e-2], index=1)
    max_iter = st.sidebar.number_input("最大反復回数 (max_iter)", min_value=100, max_value=1000, value=300, step=50)
    hidden_layer_sizes = st.sidebar.radio("隠れ層のサイズ", options=[(16,), (32,), (64,), (128,), (64, 32), (128, 64)], index=2)
    activation = st.sidebar.selectbox("活性化関数 (activation)", ["identity", "logistic", "tanh", "relu"], index=3)
    solver = st.sidebar.selectbox("ソルバー (solver)", ["lbfgs", "sgd", "adam"], index=2)

    # Session State の初期化
    if "clf" not in st.session_state:
        st.session_state.clf = None
        st.session_state.model_generated = False
        st.session_state.show_image = False

    # AIを生成ボタン
    if st.button("AIを生成"):
        st.caption("モデルを生成中... しばらくお待ちください。")
        clf = MLPClassifier(
            random_state=0,
            hidden_layer_sizes=hidden_layer_sizes,
            solver=solver,
            max_iter=max_iter,
            activation=activation,
            tol=tol
        )
        clf.fit(X_train, y_train)
        st.session_state.clf = clf
        st.session_state.model_generated = True
        st.session_state.show_image = True
        st.success("AIモデルの生成が完了しました！")

    # モデルが生成された場合
    if st.session_state.model_generated:
        # 画像を一度だけ表示
        if st.session_state.show_image:
            st.image("app_242127/aiimage.png", width=300, caption="あんまり当てられないから期待しないでね・・・")
            # st.session_state.show_image = True  # 再表示を防ぐフラグ

        # キャンバスを表示
        st.subheader("キャンバスに数字を書いてください。")
        canvas_result = st_canvas(
            fill_color="#FFFFFF",  # 背景色
            stroke_width=30,       # 線の太さ
            stroke_color="#000000",  # 線の色
            background_color="#FFFFFF",  # キャンバス背景色
            height=300,            # キャンバスの高さ
            width=300,             # キャンバスの幅
            drawing_mode="freedraw",  # 自由描画モード
            key="canvas"
        )

        # 認識開始ボタン
        if st.button("認識開始"):
            if canvas_result.image_data is not None:
                # キャンバスデータを処理
                img = canvas_result.image_data

                # グレースケール変換
                img_gray = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGBA2GRAY)

                # 8x8 にリサイズしスケール変換
                img_resized = cv2.resize(img_gray, (8, 8), interpolation=cv2.INTER_AREA)
                img_rescaled = 16 - (img_resized / 255.0 * 16).astype(np.int32)

                # 1次元配列に変換
                img_flattened = img_rescaled.ravel()

                # 予測
                prediction = st.session_state.clf.predict([img_flattened])[0]
                st.subheader(f"認識した数字: {prediction}")
                st.write("別の数字を試したい場合は、キャンバス下のゴミ箱ボタンをクリックしてください。")
            else:
                st.warning("キャンバスに数字を書いてから認識開始ボタンを押してください！")

if __name__ == "__main__":
    main()
