import streamlit as st

def main():
    # ここから記述
     # ページのタイトル
    st.title("宿題TODOリスト 📚")

    # セッション状態を使ってTODOリストを保持
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    # 新しい宿題を追加するフォーム
    with st.form("add_task_form", clear_on_submit=True):
        new_task = st.text_input("新しい宿題を追加してください：", placeholder="例: 数学の課題 1ページ")
        submitted = st.form_submit_button("追加")
        if submitted and new_task.strip():  # 空白は登録しない
            st.session_state.tasks.append({"task": new_task, "completed": False})
            st.success(f"「{new_task}」を追加しました！")

    # 宿題の一覧を表示
    st.header("📋 宿題リスト")
    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks):
            col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
            with col1:
                # チェックボックスで完了状態を変更
                completed = st.checkbox("", value=task["completed"], key=f"task-{i}")
                st.session_state.tasks[i]["completed"] = completed
            with col2:
                # 宿題の内容を表示
                task_text = f"~~{task['task']}~~" if task["completed"] else task["task"]
                st.write(task_text)
            with col3:
                # 削除ボタン
                if st.button("削除", key=f"delete-{i}"):
                    st.session_state.tasks.pop(i)
                    st.experimental_rerun()  # 再描画する

    else:
        st.info("宿題がまだありません。上記のフォームから追加してください。")

    # 宿題の進捗を表示
    total_tasks = len(st.session_state.tasks)
    completed_tasks = sum(task["completed"] for task in st.session_state.tasks)
    if total_tasks > 0:
        progress = (completed_tasks / total_tasks) * 100
        st.header("📊 進捗状況")
        st.progress(progress / 100)
        st.write(f"完了済み: {completed_tasks} / {total_tasks}")
    else:
        st.write("宿題が登録されていません。")

    # フッター
    st.write("---")
    st.caption("宿題TODOリストアプリ！")

# このスクリプトが直接実行された場合にのみ `main()` を呼び出す
if __name__ == "__main__":
    main()


