import streamlit as st
import cv2
import tempfile
import numpy as np
import pandas as pd
from ultralytics import YOLO
import os

def process_image(img_bytes, model, conf, person_only):
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
    results = model(img, conf=conf, classes=[0] if person_only else None)
    output_img = results[0].plot(labels=True, conf=True)
    return cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)

def process_video(uploaded_file, model, conf, person_only):
    temp_input_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    try:
        temp_input_file.write(uploaded_file.read())
        temp_input_path = temp_input_file.name
    finally:
        temp_input_file.close()

    cap = cv2.VideoCapture(temp_input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    temp_output_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    output_path = temp_output_file.name
    temp_output_file.close()

    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame, conf=conf, classes=[0] if person_only else None)
        frame = results[0].plot(labels=True, conf=True)
        writer.write(frame)

    cap.release()
    writer.release()
    os.unlink(temp_input_path)

    return output_path

def process_video_count(uploaded_file, model, conf):
    temp_input_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    try:
        temp_input_file.write(uploaded_file.read())
        temp_input_path = temp_input_file.name
    finally:
        temp_input_file.close()

    cap = cv2.VideoCapture(temp_input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    temp_output_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    output_path = temp_output_file.name
    temp_output_file.close()

    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    frame_nums = []
    person_counts = []
    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame, conf=conf, classes=[0])
        categories = results[0].boxes.cls
        person_num = len(categories)
        frame = results[0].plot(labels=False, conf=True)

        writer.write(frame)
        frame_nums.append(frame_id)
        person_counts.append(person_num)
        frame_id += 1

    cap.release()
    writer.release()
    os.unlink(temp_input_path)

    df = pd.DataFrame({'frame': frame_nums, 'count': person_counts})
    df['sec'] = df['frame'] / fps
    return output_path, df[['sec', 'count']]

def main():
    st.title("物体検出アプリ（YOLOv8）")

    st.sidebar.header("設定")
    app_mode = st.sidebar.radio("モード選択", ["画像で検出", "動画で検出"])
    conf = st.sidebar.slider("確信度 (conf)", 0.1, 1.0, 0.5, 0.05)

    @st.cache_resource
    def load_model():
        return YOLO("yolov8n.pt")
    
    model = load_model()
    st.markdown("---")

    if app_mode == "画像で検出":
        st.header("🖼️ 画像で検出")
        input_method = st.radio("画像入力方法", ["ファイルアップロード", "カメラで撮影"])
        if input_method == "ファイルアップロード":
            uploaded_img = st.file_uploader("画像ファイル", type=["jpg", "png", "jpeg"])
        else:
            uploaded_img = st.camera_input("カメラで撮影")

        if uploaded_img:
            # Webカメラ撮影時は元画像を表示しない
            if input_method == "ファイルアップロード":
                st.subheader("入力画像")
                st.image(uploaded_img, caption="元の画像", use_container_width=True)

            with st.spinner("画像を処理中..."):
                result_img = process_image(uploaded_img.getvalue(), model, conf, person_only=True)

            st.subheader("検出結果")
            st.image(result_img, caption="検出結果", use_container_width=True)

    elif app_mode == "動画で検出":
        st.header("🎥 動画で検出")
        st.info("動画をアップロードしてください（mp4形式）。検出動画と人数カウントグラフを生成します。")
        
        uploaded_video = st.file_uploader("動画ファイル (mp4)", type=["mp4"])
        person_only = st.checkbox("人だけを検出", value=True)
        show_graph = st.checkbox("カウントグラフを表示", value=True)

        if uploaded_video:
            st.subheader("元の動画")
            st.video(uploaded_video)

            my_bar = st.progress(0, text="動画を処理中...")

            try:
                output_path, count_df = process_video_count(uploaded_video, model, conf) if show_graph else (
                    process_video(uploaded_video, model, conf, person_only), None)

                my_bar.progress(100, text="動画処理完了！")
                st.success("動画の処理が完了しました。")

                st.subheader("検出結果動画")
                with open(output_path, 'rb') as f:
                    video_bytes = f.read()
                    st.video(video_bytes, format="video/mp4")

                if show_graph and count_df is not None:
                    st.subheader("フレームごとの人数推移")
                    st.line_chart(count_df.set_index("sec"))
                    st.subheader("カウントデータ")
                    st.dataframe(count_df)

            except Exception as e:
                st.error(f"処理中にエラーが発生しました: {e}")
            finally:
                if output_path and os.path.exists(output_path):
                    os.unlink(output_path)

    st.markdown("---")
    st.sidebar.markdown("---")
    st.sidebar.markdown("YOLOv8を用いた物体検出アプリケーション")

if __name__ == "__main__":
    main()
