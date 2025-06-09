import streamlit as st
import cv2
import tempfile
import numpy as np
import pandas as pd
from ultralytics import YOLO

def process_image(img_bytes, model, conf, person_only):
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
    results = model(img, conf=conf, classes=[0] if person_only else None)
    output_img = results[0].plot(labels=True, conf=True)
    return cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)

def process_video(uploaded_file, model, conf, person_only):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    temp_path = temp_file.name

    cap = cv2.VideoCapture(temp_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    output_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
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
    return output_path

def process_video_count(uploaded_file, model, conf):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    temp_path = temp_file.name

    cap = cv2.VideoCapture(temp_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    output_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
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

    df = pd.DataFrame({'frame': frame_nums, 'count': person_counts})
    df['sec'] = df['frame'] / fps
    return output_path, df[['sec', 'count']]

def main():
    # st.set_page_config(layout="centered")
    st.title("物体検出アプリ（YOLOv8）")

    app_mode = st.sidebar.radio("モード選択", ["画像で検出", "動画で検出", "人数カウント"])
    conf = st.sidebar.slider("確信度 (conf)", 0.1, 1.0, 0.5, 0.05)
    person_only = st.sidebar.checkbox("人だけを検出", value=True)

    model = YOLO("yolov8n.pt")

    if app_mode == "画像で検出":
        input_method = st.radio("画像入力方法", ["ファイルアップロード", "カメラで撮影"])
        if input_method == "ファイルアップロード":
            uploaded_img = st.file_uploader("画像ファイル", type=["jpg", "png"])
        else:
            uploaded_img = st.camera_input("カメラで撮影")

        if uploaded_img:
            result_img = process_image(uploaded_img.getvalue(), model, conf, person_only)
            st.image(result_img, caption="検出結果", use_column_width=True)

    elif app_mode == "動画で検出":
        st.info("動画をアップロードしてください")
        uploaded_video = st.file_uploader("動画ファイル (mp4)", type=["mp4"])

        if uploaded_video:
            output_path = process_video(uploaded_video, model, conf, person_only)
            st.success("動画の検出が完了しました。")
            st.video(output_path)

    elif app_mode == "人数カウント":
        st.info("アップロードされた動画からフレームごとの人数をカウントし、グラフ化します")
        uploaded_video = st.file_uploader("動画ファイル (mp4)", type=["mp4"])
        show_graph = st.checkbox("棒グラフを表示", value=True)

        if uploaded_video:
            output_path, count_df = process_video_count(uploaded_video, model, conf)
            st.success("人数カウントが完了しました。")
            st.video(output_path)
            if show_graph:
                st.line_chart(count_df.set_index("sec"))
                st.dataframe(count_df)

if __name__ == "__main__":
    main()
