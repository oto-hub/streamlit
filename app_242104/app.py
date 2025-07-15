import streamlit as st
import random
import datetime

def main():
    
    # 初期筋トレメニュー
    workout_menu = {
        "胸": ["ベンチプレス - 3セット x 10回", "ダンベルフライ - 3セット x 12回", "腕立て伏せ - 3セット x 15回"],
        "背中": ["懸垂 - 3セット x 8回", "デッドリフト - 4セット x 6回", "ラットプルダウン - 3セット x 12回"],
        "脚": ["スクワット - 3セット x 10回", "レッグプレス - 4セット x 12回", "ランジ - 3セット x 15回"],
        "肩": ["ショルダープレス - 3セット x 10回", "サイドレイズ - 3セット x 12回", "リアレイズ - 3セット x 15回"],
        "腕": ["アームカール - 3セット x 12回", "トライセプスエクステンション - 3セット x 12回", "ディップス - 3セット x 10回"]
    }
    workout_exercises = {
        "ベンチプレス": "https://www.youtube.com/shorts/K6FQrDhTtXw",  # ベンチプレスのやり方動画URL
        "ダンベルフライ": "https://www.youtube.com/watch?v=eozdVDA78K0",  # ダンベルフライのやり方動画URL
        "スクワット": "https://www.youtube.com/watch?v=aclHkVaku9U",  # スクワットのやり方動画URL
        "懸垂": "https://www.youtube.com/shorts/02S1drgjK_Q",  # 懸垂のやり方動画URL
        "ショルダープレス": "https://www.youtube.com/shorts/IH24_ohO4Jc"  # ショルダープレスのやり方動画URL
    }

    # StreamlitのUI構築
    # st.set_page_config(page_title="筋トレメニューサポート", page_icon="🏋️‍♂️", layout="wide")
    st.title("🏋️‍♂️ あなたの筋トレをサポート 💪")

    # セッション状態に筋トレメニューが保存されていない場合は初期メニューを保存
    if "workout_menu" not in st.session_state:
        st.session_state.workout_menu = workout_menu

    # ページ選択のセレクトボックス
    page = st.sidebar.selectbox("ページを選択", ["ホーム", "筋トレメニュー", "今日のトレーニング", "トレーニング履歴","やり方"])

    # ホームページ
    if page == "ホーム":
        st.header("ようこそ！筋トレメニュー提案アプリへ")
    
        # 画像を中央に配置するために、st.columnsを使用
        col1, col2, col3 = st.columns([1, 4, 1])  # 中央カラムに画像を配置
        with col2:
            st.image("app_242104/jisan.webp", caption="山中筋肉", use_container_width=True)

        st.write(""" 
        このアプリでは以下のことができます：
        - 部位ごとの筋トレメニューを確認
        - 今日のトレーニングプランを作成
        - 過去のトレーニング履歴を確認
        まずはサイドバーから好きなページを選んでみてください！
        """)

    elif page == "筋トレメニュー":
        st.header("部位ごとの筋トレメニューとカスタム種目の追加")
        selected_part = st.selectbox("鍛えたい部位を選択", ["選択してください"] + list(st.session_state.workout_menu.keys()))


        if selected_part != "選択してください":
            # 現在の種目一覧を表示
            st.write(f"### {selected_part}の筋トレメニュー")
            for exercise in st.session_state.workout_menu[selected_part]:
                st.write(f"- {exercise}")

         # 新しい種目を追加するUI
            st.write("### 新しい種目を追加")
            new_exercise = st.text_input(f"{selected_part}に追加したい種目を入力してください")

            # 種目追加ボタン
            if st.button(f"{selected_part}に種目を追加"):
                if new_exercise:
                    # セッション状態に追加した種目を反映
                    st.session_state.workout_menu[selected_part].append(new_exercise)  # メニューに新しい種目を追加
                    st.success(f"新しい種目『{new_exercise}』を「{selected_part}」に追加しました！", icon="✅")
                
                else:
                    st.error("種目名を入力してください。", icon="❌")

    elif page == "今日のトレーニング":
        st.header("今日のトレーニングを作成")
        st.write("以下から好きなトレーニングを選んで、プランを作成しましょう！")

        selected_exercises = []  # ユーザーが選択したトレーニングを保存するリスト

        # 部位ごとにトレーニングメニューを表示
        for part, exercises in st.session_state.workout_menu.items():
            selected = st.multiselect(f"{part}のトレーニングを選ぶ", exercises)
            selected_exercises.extend(selected)  # 選択されたトレーニングをリストに追加

        # 選択したトレーニングを表示
        if selected_exercises:
            st.write("### 今日のトレーニングメニュー:")
            for exercise in selected_exercises:
                st.write(f"- {exercise}")

        # トレーニングを保存するボタン
            if st.button("今日のトレーニングを保存"):
                try:
                    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("app_242104/workout_log.txt", "a", encoding="utf-8") as f:
                        f.write(f"日付: {date}\n")
                        for exercise in selected_exercises:
                            f.write(f"{exercise}\n")
                        f.write("\n")
                    st.success("トレーニング内容を保存しました！", icon="✅")
                except Exception as e:
                    st.error(f"保存時にエラーが発生しました: {e}", icon="❌")
        else:
            st.write("トレーニングを選択してください！")

    # トレーニング履歴ページ
    elif page == "トレーニング履歴":
        st.header("トレーニング履歴")
    
        try:
            # トレーニング履歴を読み込む
            with open("app_242104/workout_log.txt", "r", encoding="utf-8") as f:
                logs = f.readlines()

            if logs:
                st.write("### 過去のトレーニング内容:")

                # 各履歴の横に削除ボタンを配置
                for i, log in enumerate(logs, start=1):
                    col1, col2 = st.columns([3, 1])
                    col1.write(f"{i}. {log.strip()}")
                    if col2.button(f"削除 {i}", key=f"delete_{i}"):
                        logs.pop(i - 1)  # 履歴を削除
                        # 新しい履歴を書き戻す
                        with open("app_242104/workout_log.txt", "w", encoding="utf-8") as f:
                            f.writelines(logs)
                        # st.experimental_rerun()  # ページをリロードして削除を反映
                        st.write("履歴が削除されました。")

            else:
                st.write("トレーニング履歴がまだありません。")
    
        except FileNotFoundError:
            st.warning("トレーニング履歴ファイルが見つかりません。初めて利用する場合はトレーニングを保存してください。")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}", icon="❌")

    # やり方ページ
    elif page == "やり方":
        st.header("やり方")
        for exercise, url in workout_exercises.items():
            st.write(f"### {exercise}")  # エクササイズ名を表示
            st.markdown(f"[【{exercise}のやり方を見る】]({url})", unsafe_allow_html=True)  # URLリンクを作成
main()
    