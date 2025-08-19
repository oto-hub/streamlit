import streamlit as st
import app_242105.chatbot
import app_242105.stone_game
import app_242105.home
import app_242105.stone_game_new

def main():
    # ページ選択
    page = st.selectbox("ページを選択してください", ["home","チャットボット", "石取りゲーム","石取りゲーム(強)"])

    # ページに応じて関数を呼び出す
    if page =="home":
        app_242105.home.hello()
    elif page == "チャットボット":
        app_242105.chatbot.main()
    elif page == "石取りゲーム":
        app_242105.stone_game.play_game()
    elif page == "石取りゲーム(強)":
        app_242105.stone_game_new.play_game()

if __name__ == "__main__":
    main()
