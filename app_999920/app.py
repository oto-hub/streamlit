import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from io import BytesIO, BufferedReader

# モデルの初期化
mp_pose = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

pose = mp_pose.Pose(static_image_mode=True,
                    min_detection_confidence=0.5, model_complexity=2)
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True,
                                  max_num_faces=1,
                                  refine_landmarks=True,
                                  min_detection_confidence=0.5)

st.title("Pose & Gaze Estimation")

# サイドバーでモード選択
mode = st.sidebar.radio("判定モードを選択してください", ["骨格推定（画像）", "目線判定（画像）"])

# 画像入力
input_method = st.radio("画像入力方法", ["ファイルアップロード", "カメラで撮影"])
if input_method == "ファイルアップロード":
    uploaded_img = st.file_uploader("画像ファイルをアップロード", type=['png', 'jpg', 'jpeg'])
else:
    uploaded_img = st.camera_input("カメラで撮影")

# 処理開始
if uploaded_img is not None:
    # 画像読み込みと変換
    bytes_data = uploaded_img.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    output_img = img.copy()

    if mode == "骨格推定（画像）":
        results = pose.process(img)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                output_img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # 両手の挙上判定
            right_th = results.pose_landmarks.landmark[20].y - results.pose_landmarks.landmark[12].y
            left_th = results.pose_landmarks.landmark[19].y - results.pose_landmarks.landmark[11].y
            right_state = '挙がっている' if right_th < 0 else '挙がっていない'
            left_state = '挙がっている' if left_th < 0 else '挙がっていない'

            st.text(f'右手は：{right_state}')
            st.text(f'左手は：{left_state}')
        else:
            st.warning("人物が検出できませんでした。")

    elif mode == "目線判定（画像）":
        results = face_mesh.process(img)

        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]

            # 目線判定
            iris_x = face_landmarks.landmark[468].x
            eye_center_x = (face_landmarks.landmark[33].x + face_landmarks.landmark[133].x) / 2
            gaze_dir = '右' if iris_x < eye_center_x else '左'
            st.text(f'目線は：{gaze_dir}')

            # 描画
            mp_drawing.draw_landmarks(
                image=output_img,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_contours_style())

            mp_drawing.draw_landmarks(
                image=output_img,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_iris_connections_style())

            # 両目を囲う矩形（視認性向上）
            ih, iw, _ = img.shape
            for eye in [[33, 133], [362, 263]]:
                x1 = int(min(face_landmarks.landmark[eye[0]].x, face_landmarks.landmark[eye[1]].x) * iw)
                x2 = int(max(face_landmarks.landmark[eye[0]].x, face_landmarks.landmark[eye[1]].x) * iw)
                y1 = int(min(face_landmarks.landmark[eye[0]].y, face_landmarks.landmark[eye[1]].y) * ih)
                y2 = int(max(face_landmarks.landmark[eye[0]].y, face_landmarks.landmark[eye[1]].y) * ih)
                cv2.rectangle(output_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        else:
            st.warning("顔が検出できませんでした。")

    # 結果表示とダウンロード機能
    st.image(output_img, caption='予測結果', use_column_width=True)
    ret, enco_img = cv2.imencode(".png", cv2.cvtColor(output_img, cv2.COLOR_RGB2BGR))
    BytesIO_img = BytesIO(enco_img.tobytes())
    BufferedReader_img = BufferedReader(BytesIO_img)
    st.download_button(label='画像をダウンロード',
                       data=BufferedReader_img,
                       file_name="output.png",
                       mime="image/png")

if __name__ == "__main__":
    main()
