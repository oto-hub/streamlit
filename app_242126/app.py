import streamlit as st
import random



def main():
    
    st.image("app_242126/数字写真.jpg")
    st.title('数字当てゲーム')
    
    """数字当てゲームのメイン関数"""

    # ゲームの状態を保持
    if 'count' not in st.session_state:
        st.session_state.count = 0
        st.session_state.game_over = False
        st.session_state.ans = random.randint(1, 100)  # 正解の数字をセッションに保存
        st.session_state.guess = None  # 初期値としてNone
        st.session_state.guesses = []  # これまでの入力された数字を保持するリスト

    # ゲーム終了後の処理
    if st.session_state.game_over:
        st.write(f"正解です！{st.session_state.count}回で当てられました！")
        st.write("ボタンを押すと新しいゲームが始まります。")

        # エンターキーを押したらゲームをリセットして再実行
        if st.button("次のゲームへ"):
            st.session_state.count = 0
            st.session_state.game_over = False
            st.session_state.ans = random.randint(1, 100)  # 新しい正解の数字を生成
            st.session_state.guess = None
            st.session_state.guesses = []  # 過去の数字をリセット
            st.rerun()  # 再実行して新しいゲームを開始

    else:
        # ユーザー入力
        guess = st.text_input("1から100までの数字を予想してください")

        # guessが入力された場合の処理
        if guess:
            try:
                # 入力されたguessを整数に変換
                st.session_state.guess = int(guess)

                # 範囲外の数値の場合
                if st.session_state.guess < 1 or st.session_state.guess > 100:
                    st.write("1から100までの数字を入力してください。")
                else:
                    st.session_state.count += 1  # 予想回数を増やす
                    st.session_state.guesses.append(st.session_state.guess)  # 入力された数字をリストに追加

                    # 正解を探すためにfor文を使って繰り返し
                    for _ in range(1):
                        if st.session_state.guess < st.session_state.ans:
                            st.write("小さすぎます！")
                            break
                        elif st.session_state.guess > st.session_state.ans:
                            st.write("大きすぎます！")
                            break
                        else:
                            st.session_state.game_over = True  # 正解を出した場合
                            st.write(f"正解です！{st.session_state.count}回で当てられました！")
                            break

            except ValueError:
                st.write("有効な数字を入力してください。")
        else:
            # 入力が空の場合の警告
            st.write("数字を入力してください。")

        # 今まで入力された数字をカンマ区切りで表示
        st.write("これまで入力した数字：", ', '.join(map(str, st.session_state.guesses)))

if __name__ == "__main__":
    main()
