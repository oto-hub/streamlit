import streamlit as st
import cv2
import numpy as np
import torch
from PIL import Image
from io import BytesIO, BufferedReader

def main():
    # モデルのロード
    # Note: torch.hub.load は初回実行時にモデルをダウンロードするため、時間がかかる場合があります。
    # 実際のデプロイ時には、事前にモデルをダウンロードしておくことを検討してください。
    model1 = torch.hub.load("bryandlee/animegan2-pytorch:main", "generator", pretrained="face_paint_512_v2")
    model2 = torch.hub.load("bryandlee/animegan2-pytorch:main", "generator", pretrained="celeba_distill")
    face2paint = torch.hub.load("bryandlee/animegan2-pytorch:main", "face2paint")

    # Streamlit UI
    st.title("アニメ顔変換アプリ") # アプリのタイトルを追加
    col1, col2 = st.columns(2)

    # Input
    upload_img = st.sidebar.file_uploader("画像をアップロードしてください", type=['png','jpg'])
    select_model = st.sidebar.selectbox('変換モデルを選択してください:',['face_paint_512_v2', 'celeba_distill'])

    # Process
    if upload_img is not None:
        # アップロードされた画像を処理
        bytes_data = upload_img.getvalue()
        tg_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        tg_img = cv2.cvtColor(tg_img, cv2.COLOR_BGR2RGB)
        original_img = tg_img.copy()

        tg_img = Image.fromarray(tg_img)

        # 選択されたモデルで変換
        if select_model == 'face_paint_512_v2':
            output_img = face2paint(model1, tg_img, size=512)
        elif select_model == 'celeba_distill':
            output_img = face2paint(model2, tg_img, size=512)

        # ダウンロード用に画像を準備
        # StreamlitのダウンロードボタンはBytesIOオブジェクトを期待します
        ret, enco_img = cv2.imencode(".png", cv2.cvtColor(np.array(output_img), cv2.COLOR_BGR2RGB))
        BytesIO_img = BytesIO(enco_img.tobytes()) # .tostring() は非推奨なので .tobytes() を使用
        BufferedReader_img = BufferedReader(BytesIO_img)

        # Output
        with col1:
            st.header("元画像")
            st.image(original_img, caption="元の画像", use_column_width=True)

        with col2:
            st.header("変換結果")
            st.image(output_img, caption="アニメ顔変換後の画像", use_column_width=True)

            st.download_button(
                label='変換画像をダウンロード',
                data=BufferedReader_img,
                file_name="anime_output.png",
                mime="image/png"
            )
    else:
        st.info("左側のサイドバーから画像をアップロードしてください。")

# アプリケーションのエントリポイント
if __name__ == '__main__':
    main()