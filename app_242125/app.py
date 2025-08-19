import streamlit as st
import random
import numpy as np

# ビンゴカードを作成する関数
def create_bingo_card():
    card = []
    # 各列は異なる範囲の数字を持つ
    for i in range(5):
        if i == 0:
            card.append(random.sample(range(1, 16), 5))
        elif i == 1:
            card.append(random.sample(range(16, 31), 5))
        elif i == 2:
            card.append(random.sample(range(31, 46), 5))
        elif i == 3:
            card.append(random.sample(range(46, 61), 5))
        elif i == 4:
            card.append(random.sample(range(61, 76), 5))
    return np.array(card)

# ビンゴチェックを行う関数
def check_bingo(card, called_numbers):
    # 横、縦、斜めのチェックを行う
    for i in range(5):
        if all(card[i][j] in called_numbers for j in range(5)):  # 横
            return True
        if all(card[j][i] in called_numbers for j in range(5)):  # 縦
            return True
    if all(card[i][i] in called_numbers for i in range(5)):  # 斜め（左上から右下）
        return True
    if all(card[i][4-i] in called_numbers for i in range(5)):  # 斜め（右上から左下）
        return True
    return False

# ランダムで数字を出力する関数
def get_random_number(called_numbers):
    available_numbers = set(range(1, 100)) - set(called_numbers)
    return random.choice(list(available_numbers))

# 数字が呼ばれた際にカードの数字を●に置き換える関数
def replace_with_circle(card, called_numbers):
    return np.where(np.isin(card, called_numbers), '●', card)

# ゲームを実行するメイン関数
def main():
    st.title("ビンゴゲーム")

    # ビンゴカードの数をユーザーが入力できるようにする
    num_cards = st.text_input("ビンゴカードの数を入力してください:", "1")

    # 入力された値を整数に変換
    try:
        num_cards = int(num_cards)
    except ValueError:
        st.error("数値を入力してください。")
        num_cards = 1

    # ビンゴカードと呼ばれた数字を保持
    if 'bingo_cards' not in st.session_state or 'called_numbers' not in st.session_state:
        st.session_state.bingo_cards = [create_bingo_card() for _ in range(num_cards)]
        st.session_state.called_numbers = []

    # ビンゴカードの上に「数字を引く」ボタンを配置
    if st.button("ランダムで数字を引く"):
        number = get_random_number(st.session_state.called_numbers)
        st.session_state.called_numbers.append(number)
        st.write(f"引かれた数字: {number}")

    # カードの表示
    for i, card in enumerate(st.session_state.bingo_cards):
        updated_card = replace_with_circle(card, st.session_state.called_numbers)
        st.write(f"ビンゴカード {i+1}")
        st.write(updated_card)

        # ビンゴチェックと結果表示
        if check_bingo(card, st.session_state.called_numbers):
            st.write(f"カード {i+1} はビンゴです！🎉")
            # ビンゴになったら画像を表示
            st.image("app_242125/bingo.jpg", caption=f"ビンゴ！カード {i+1}")

    # 呼ばれた数字を表示
    st.write("呼ばれた数字:")
    st.write(", ".join(map(str, st.session_state.called_numbers)))

    # リセットボタン
    if st.button("リセット"):
        st.session_state.bingo_cards = [create_bingo_card() for _ in range(num_cards)]
        st.session_state.called_numbers = []
        st.write("ゲームがリセットされました。")

# メイン関数を実行
if __name__ == "__main__":
    main()









