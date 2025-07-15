import streamlit as st
import time
import random

# 絵柄と対応する画像ファイル名
symbols = ["777", "bar", "ピエロ", "ベル", "ぶどう", "いぬ", "チェリー"]
images = [f"app_242117/{symbol}.png" for symbol in symbols]
points = [777, 500, 300, 100, 50, 30, 10]

# スロットを回す関数
def spin():
    # 回数をカウントアップ
    st.session_state.count += 1

    # 確率を調整した乱数生成
    weights = [1, 2, 3, 4, 5, 6, 7]
    result = random.choices(symbols, weights=weights, k=3)

    # スロットの回転アニメーションを模倣
    time.sleep(1)

    # 結果を表示
    display_result(result)

    # ポイント計算
    earned_points = calculate_points(result)
    st.session_state.total_points += earned_points

    # 結果を表示
    st.write(f"{result[0]}が揃いました！ {earned_points}ポイント獲得！") if earned_points > 0 else st.write("はずれ")

def reset():
    st.session_state.count = 0
    st.session_state.total_points = 0    

def display_result(result):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(images[symbols.index(result[0])], width=200)
    with col2:
        st.image(images[symbols.index(result[1])], width=200)
    with col3:
        st.image(images[symbols.index(result[2])], width=200)

# ポイント計算関数
def calculate_points(result):
    if all(r == result[0] for r in result):
        index = symbols.index(result[0])
        return points[index]
    return 0

def main():
    if 'count' not in st.session_state:
        st.session_state.count = 0
    if 'total_points' not in st.session_state:
        st.session_state.total_points = 0
    
    st.title("🎰スロットマシーン")
    st.write(f"回した回数: {st.session_state.count}")
    st.write(f"獲得ポイント: {st.session_state.total_points}")
    
    # ボタンを配置
    if st.button("スロットを回す", key="spin_button"):
        spin()

    if st.button("リセット", key="reset_button"):
        reset()

if __name__ == "__main__":
    main()
