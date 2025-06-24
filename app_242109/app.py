import streamlit as st
import random
from PIL import Image

# 画像ファイル
try:
    gu_image = Image.open("app_242109/gu.png").resize((100, 100))
    choki_image = Image.open("app_242109/choki.png").resize((100, 100))
    pa_image = Image.open("app_242109/pa.png").resize((100, 100))
except FileNotFoundError:
    st.error("画像ファイル (gu.png, choki.png, pa.png) が見つかりません。")
    st.stop()

def janken():
    hands = ["グー", "チョキ", "パー"]
    secure_random = random.SystemRandom()
    computer_hand = secure_random.choice(hands)
    return computer_hand

def judge(player_hand, computer_hand):
    if player_hand == computer_hand:
        return "あいこでしょ！"
    elif (player_hand == "グー" and computer_hand == "チョキ") or \
         (player_hand == "チョキ" and computer_hand == "パー") or \
         (player_hand == "パー" and computer_hand == "グー"):
        return "あなたのかち！"
    else:
        return "おまえのまけ！"

def main():
    st.title("じゃんけんシュミレーター")
    st.write("じゃんけんポン！")

    if "show_button" not in st.session_state:
        st.session_state.show_button = True
    if "result" not in st.session_state:
        st.session_state.result = None
    if "computer_hand" not in st.session_state:
        st.session_state.computer_hand = None

    player_hand = st.radio(
        "何を出す？",
        ("グー", "チョキ", "パー"),
        horizontal=True,
        key="player_choice"
    )

    col1, col2 = st.columns(2)

    if st.session_state.show_button:
        if st.button("勝負！"):
            st.session_state.show_button = False
            st.session_state.computer_hand = janken()
            st.session_state.result = judge(player_hand, st.session_state.computer_hand)
            st.rerun()  
            
    if st.session_state.result is not None and st.session_state.computer_hand is not None:
        with col1:
            st.write("あなた:")
            if player_hand == "グー":
                st.image(gu_image)
            elif player_hand == "チョキ":
                st.image(choki_image)
            elif player_hand == "パー":
                st.image(pa_image)
        with col2:
            st.write("コンピューター:")
            if st.session_state.computer_hand == "グー":
                st.image(gu_image)
            elif st.session_state.computer_hand == "チョキ":
                st.image(choki_image)
            elif st.session_state.computer_hand == "パー":
                st.image(pa_image)
        st.write(st.session_state.result)

    if st.button("リセット"):
        st.session_state.show_button = True
        st.session_state.result = None
        st.session_state.computer_hand = None

if __name__ == "__main__":
    main()