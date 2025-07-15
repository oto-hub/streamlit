import streamlit as st
import random

def reset_game():
    st.session_state.pc_ans = random.randint(1, 100)
    st.session_state.message = "数字を入力してください"
    st.session_state.game_over = False

def main():
    st.title("数当てゲーム")
    
    if "pc_ans" not in st.session_state:
        reset_game()
    
    st.write("コンピュータが1～100の数字を1つ決めました。")
    
    your_ans = st.number_input("当ててみてください：", min_value=1, max_value=100, step=1)
    
    if st.button("判定"):
        if not st.session_state.game_over:
            if your_ans < st.session_state.pc_ans:
                st.session_state.message = "残念、それよりも大きいです"
            elif your_ans > st.session_state.pc_ans:
                st.session_state.message = "残念、それよりも小さいです"
            else:
                st.session_state.message = "おめでとうございます！ 正解です✨"
                st.session_state.game_over = True
    
    st.write(st.session_state.message)
    
    if st.session_state.game_over:
        if st.button("もう一度プレイ"):
            reset_game()

if __name__ == "__main__":
    main()
