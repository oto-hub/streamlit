import streamlit as st
import random

# ランダムな数字リストを生成する関数
def generate_numbers():
    correct_numbers = random.sample(range(1, 101), 10)  # 1～100の範囲からランダムに10個選択
    incorrect_numbers = correct_numbers.copy()
    
    # 1つの数字を変更することで間違いを作成
    incorrect_index = random.randint(0, 9)
    incorrect_numbers[incorrect_index] = random.randint(1, 100)
    
    return correct_numbers, incorrect_numbers

# Streamlit アプリケーション
def main():
    # セッションステートに数字リストが存在しない場合にのみリストを生成
    if 'correct_numbers' not in st.session_state or 'incorrect_numbers' not in st.session_state:
        correct_numbers, incorrect_numbers = generate_numbers()
        st.session_state.correct_numbers = correct_numbers
        st.session_state.incorrect_numbers = incorrect_numbers
    
    st.title("数字の間違い探しアプリ")
    
    # 常に同じ位置にリストを表示するために、st.empty()を使ってリストを表示
    list_placeholder = st.empty()
    
    # リスト表示をこの場所に固定
    with list_placeholder.container():
        # 正しい数字と間違った数字をコンマ区切りで表示
        st.write("正しい数字のリスト: ", ", ".join(map(str, st.session_state.correct_numbers)))
        st.write("間違った数字のリスト: ", ", ".join(map(str, st.session_state.incorrect_numbers)))
    
    # ユーザーが入力するフォーム
    st.write("次の2つの数字リストを見比べて、間違っている数字を入力してください。")
    
    # 数字を入力するフォーム
    user_input = st.text_input("間違っている数字のインデックスを入力してください （0～9） ")

    if user_input:
        try:
            # 入力された値を整数に変換
            user_input = int(user_input)
            
            # 入力がリストの範囲内かチェック
            if user_input < 0 or user_input >= len(st.session_state.incorrect_numbers):
                st.write("無効なインデックスです。0から9までの数字を入力してください。")
            else:
                # ユーザーが選んだインデックスの数字が間違いリストにあるかチェック
                if st.session_state.incorrect_numbers[user_input] != st.session_state.correct_numbers[user_input]:
                    st.write(f"正解！{user_input}番目の数字 {st.session_state.incorrect_numbers[user_input]} は間違っています。")
                    st.write(f"正しい数字は {st.session_state.correct_numbers[user_input]} です。")
                    
                    # 正解したらリストを更新
                    correct_numbers, incorrect_numbers = generate_numbers()
                    st.session_state.correct_numbers = correct_numbers
                    st.session_state.incorrect_numbers = incorrect_numbers
                    
                    # 新しいリストを表示（同じ位置に表示される）
                    with list_placeholder.container():
                        st.write("新しい正しい数字のリスト: ", ", ".join(map(str, st.session_state.correct_numbers)))
                        st.write("新しい間違った数字のリスト: ", ", ".join(map(str, st.session_state.incorrect_numbers)))
                    
                else:
                    st.write(f"不正解！{user_input}番目の数字 {st.session_state.incorrect_numbers[user_input]} は正しいです。")
        except ValueError:
            st.write("数字を入力してください。")
    
if __name__ == "__main__":
    main()