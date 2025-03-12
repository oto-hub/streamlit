import streamlit as st
from transformers import pipeline

# Hugging Faceの生成AIを使って応答を取得する関数
def get_bot_response(user_input):
    try:
        # Hugging FaceのGPT-2モデルを使った生成パイプラインを作成
        generator = pipeline('text-generation', model='gpt2')

        # モデルに入力を与えて応答を生成
        response = generator(user_input, max_length=100, num_return_sequences=1)

        # 生成されたテキストを返す
        return response[0]['generated_text'].strip()
    except Exception as e:
        return f"エラーが発生しました: {e}"

def main():
    # タイトルを表示
    st.title("チャットボット")
    st.write("こんにちは！質問をどうぞ。英語入力の方が精度がいいです")

    # ユーザーの入力を受け付ける
    user_input = st.text_input("あなたの質問:", "")

    # ユーザーが入力を送信した場合に応答を表示
    if user_input:
        # Hugging FaceのGPT-2モデルを使って応答を生成
        bot_response = get_bot_response(user_input)
        st.write(f"ボットの回答: {bot_response}")


