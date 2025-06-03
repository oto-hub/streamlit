import streamlit as st
from datetime import datetime

def main():
    if "diary_entries" not in st.session_state:
        st.session_state.diary_entries = []

    st.title("日記アプリ")

    with st.form("diary_form"):
        diary_text = st.text_area("今日の日記を書いてください")
        submitted = st.form_submit_button("保存")

    if submitted and diary_text.strip():
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.diary_entries.append({
            "date": now_str,
            "text": diary_text
        })
        st.success("日記を保存しました！")

    st.sidebar.header("過去の日記")
    if st.session_state.diary_entries:
        dates = [entry["date"] for entry in st.session_state.diary_entries]
        selected_date = st.sidebar.selectbox("日付を選択してください", options=dates[::-1])

        for entry in st.session_state.diary_entries:
            if entry["date"] == selected_date:
                st.header(f"日記（{selected_date}）")
                st.write(entry["text"])
                break
    else:
        st.sidebar.write("まだ日記がありません。")

if __name__ == "__main__":
    main()
