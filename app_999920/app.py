import streamlit as st
import cv2
import numpy as np
from io import BytesIO

def process_image_simple(img_bytes):
    """シンプルな画像処理（MediaPipeなし）"""
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 顔検出（OpenCVのHaar Cascade）
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # 顔を検出した場合、矩形を描画
    output_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    for (x, y, w, h) in faces:
        cv2.rectangle(output_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    return output_img, len(faces)

def main():
    st.title("画像処理アプリ（軽量版）")
    
    st.info("🔧 軽量モード: MediaPipeライブラリが利用できないため、基本的な画像処理機能のみ利用可能です。")
    st.markdown("---")
    
    # 画像入力
    input_method = st.radio("画像入力方法", ["ファイルアップロード", "カメラで撮影"])
    if input_method == "ファイルアップロード":
        uploaded_img = st.file_uploader("画像ファイルをアップロード", type=['png', 'jpg', 'jpeg'])
    else:
        uploaded_img = st.camera_input("カメラで撮影")
    
    # 処理開始
    if uploaded_img is not None:
        st.subheader("入力画像")
        st.image(uploaded_img, caption="元の画像", use_container_width=True)
        
        with st.spinner("画像を処理中..."):
            result_img, face_count = process_image_simple(uploaded_img.getvalue())
        
        st.subheader("処理結果")
        st.image(result_img, caption="顔検出結果", use_container_width=True)
        
        if face_count > 0:
            st.success(f"検出された顔の数: {face_count}")
        else:
            st.warning("顔が検出されませんでした")
    
    st.markdown("---")
    st.sidebar.markdown("---")
    st.sidebar.markdown("軽量版画像処理アプリケーション")

if __name__ == "__main__":
    main()
