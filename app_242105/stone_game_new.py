import streamlit as st
import time  # 時間を制御するためのライブラリ

def play_game():
    st.title("石取りゲーム(強)")
    st.write("1～3個の石を取ることができます。29個目の石を取った人が負けです。")

    # セッション状態の初期化
    if "total_stones" not in st.session_state:
        st.session_state.total_stones = 29  # 石の総数
        st.session_state.player_turn = True  # プレイヤーのターン
        st.session_state.message = ""  # メッセージ
        st.session_state.stones_to_take = 0  # プレイヤーが取った石数を保存する変数

    # 残りの石を表示
    st.write(f"残りの石: {st.session_state.total_stones}")

    # 勝敗の確認
    if st.session_state.total_stones <= 0:
        if st.session_state.player_turn:
            st.success("あなたの勝ちです！")
        else:
            st.success("コンピュータの勝ちです！")

        # 再スタートボタン
        if st.button("再スタート"):
            st.session_state.total_stones = 29  # 初期値にリセット
            st.session_state.player_turn = True
            st.session_state.message = ""
        return

    # ゲーム進行
    if st.session_state.player_turn:
        st.write("あなたのターンです。1～3個の石を取ってください。")
        stones_to_take = st.number_input(
            "取る石の数を選んでください (1～3):", min_value=1, max_value=3, step=1
        )
        
        if st.button("石を取る"):
            if 1 <= stones_to_take <= 3 and stones_to_take <= st.session_state.total_stones:
                st.session_state.total_stones -= stones_to_take
                st.session_state.stones_to_take = stones_to_take  # プレイヤーの取った石数を保存
                st.session_state.player_turn = False
                st.rerun()  # 画面更新
            else:
                st.warning("有効な数を選んでください。")
    else:
        st.write("コンピュータのターンです...")

        # プレイヤーが取った石数に基づいてコンピュータが取る石数を決定
        computer_take = 4 - st.session_state.stones_to_take  # プレイヤーが取った石数に基づく計算
        if computer_take < 1:  # 取るべき石数が0未満になるのを防ぐ
            computer_take = 1

        st.session_state.total_stones -= computer_take
        st.session_state.player_turn = True
        st.write(f"コンピュータが {computer_take} 個の石を取りました。")  # コンピュータの行動を表示

        # 少し待ってから次のターンに進む
        time.sleep(1.5)  # 1.5秒間待機

        st.rerun()  # 画面更新

    # メッセージを表示
    if st.session_state.message:
        st.write(st.session_state.message)
