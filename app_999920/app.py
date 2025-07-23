import streamlit as st
import cv2
import numpy as np
# import mediapipe as mp
from io import BytesIO

# def main():
#     # mediapipeユーティリティ
#     mp_pose = mp.solutions.pose
#     mp_face_mesh = mp.solutions.face_mesh
#     mp_drawing = mp.solutions.drawing_utils
#     mp_drawing_styles = mp.solutions.drawing_styles

#     st.title("Pose・Gaze・Smile判定アプリ")

#     # --- サイドバー ---
#     mode = st.sidebar.radio("判定モードを選択してください", 
#                             ["骨格推定（画像）", "目線判定（画像）", "笑顔判定（画像）"])

#     # 各モードごとのパラメータ設定（日本語ラベル）
#     if mode == "骨格推定（画像）":
#         pose_conf = st.sidebar.slider("検出信頼度（骨格推定）", 0.0, 1.0, 0.5, 0.05)
#         pose_complex = st.sidebar.selectbox("モデルの複雑さ（骨格推定）", [0, 1, 2], index=2)

#     elif mode in ["目線判定（画像）", "笑顔判定（画像）"]:
#         face_conf = st.sidebar.slider("検出信頼度（顔推定）", 0.0, 1.0, 0.5, 0.05)
#         max_faces = st.sidebar.slider("最大検出顔数", 1, 5, 1)
#         refine = st.sidebar.checkbox("精密ランドマーク（目・口）", value=True)

#     # --- 画像入力 ---
#     input_method = st.radio("画像入力方法", ["ファイルアップロード", "カメラで撮影"])
#     if input_method == "ファイルアップロード":
#         uploaded_img = st.file_uploader("画像ファイルをアップロード", type=['png', 'jpg', 'jpeg'])
#     else:
#         uploaded_img = st.camera_input("カメラで撮影")

#     # --- 処理開始 ---
#     if uploaded_img is not None:
#         bytes_data = uploaded_img.getvalue()
#         cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
#         img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
#         output_img = img.copy()

#         if mode == "骨格推定（画像）":
#             with mp_pose.Pose(static_image_mode=True,
#                               min_detection_confidence=pose_conf,
#                               model_complexity=pose_complex) as pose:
#                 results = pose.process(img)

#                 if results.pose_landmarks:
#                     mp_drawing.draw_landmarks(
#                         output_img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

#                     # 手の挙上判定
#                     right = results.pose_landmarks.landmark[20].y - results.pose_landmarks.landmark[12].y
#                     left = results.pose_landmarks.landmark[19].y - results.pose_landmarks.landmark[11].y
#                     st.text(f'右手は：{"挙がっている" if right < 0 else "挙がっていない"}')
#                     st.text(f'左手は：{"挙がっている" if left < 0 else "挙がっていない"}')
#                 else:
#                     st.warning("人物が検出できませんでした。")

#         elif mode in ["目線判定（画像）", "笑顔判定（画像）"]:
#             with mp_face_mesh.FaceMesh(static_image_mode=True,
#                                        max_num_faces=max_faces,
#                                        refine_landmarks=refine,
#                                        min_detection_confidence=face_conf) as face_mesh:
#                 results = face_mesh.process(img)

#                 if results.multi_face_landmarks:
#                     face_landmarks = results.multi_face_landmarks[0]

#                     if mode == "目線判定（画像）":
#                         # 目線判定
#                         iris_x = face_landmarks.landmark[468].x
#                         eye_center_x = (face_landmarks.landmark[33].x + face_landmarks.landmark[133].x) / 2
#                         gaze_dir = '右' if iris_x < eye_center_x else '左'
#                         st.text(f'目線は：{gaze_dir}')

#                         # 描画
#                         mp_drawing.draw_landmarks(
#                             image=output_img,
#                             landmark_list=face_landmarks,
#                             connections=mp_face_mesh.FACEMESH_CONTOURS,
#                             landmark_drawing_spec=None,
#                             connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
#                         mp_drawing.draw_landmarks(
#                             image=output_img,
#                             landmark_list=face_landmarks,
#                             connections=mp_face_mesh.FACEMESH_IRISES,
#                             landmark_drawing_spec=None,
#                             connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())

#                         # 両目を囲う矩形
#                         ih, iw, _ = img.shape
#                         for eye in [[33, 133], [362, 263]]:
#                             x1 = int(min(face_landmarks.landmark[eye[0]].x, face_landmarks.landmark[eye[1]].x) * iw)
#                             x2 = int(max(face_landmarks.landmark[eye[0]].x, face_landmarks.landmark[eye[1]].x) * iw)
#                             y1 = int(min(face_landmarks.landmark[eye[0]].y, face_landmarks.landmark[eye[1]].y) * ih)
#                             y2 = int(max(face_landmarks.landmark[eye[0]].y, face_landmarks.landmark[eye[1]].y) * ih)
#                             cv2.rectangle(output_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

#                     elif mode == "笑顔判定（画像）":
#                         ref_y = (face_landmarks.landmark[13].y + face_landmarks.landmark[14].y) / 2
#                         smile_value = face_landmarks.landmark[291].y - ref_y
#                         state = '笑顔' if smile_value < 0 else '真顔'
#                         st.text(f'表情は：{state}')

#                         # 口元描画
#                         mp_drawing.draw_landmarks(
#                             image=output_img,
#                             landmark_list=face_landmarks,
#                             connections=mp_face_mesh.FACEMESH_LIPS,
#                             landmark_drawing_spec=None,
#                             connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
#                 else:
#                     st.warning("顔が検出できませんでした。")

#         # --- 結果表示とダウンロード ---
#         st.image(output_img, caption='予測結果', use_column_width=True)
#         ret, enco_img = cv2.imencode(".png", cv2.cvtColor(output_img, cv2.COLOR_RGB2BGR))
#         BytesIO_img = BytesIO(enco_img.tobytes())
#         st.download_button(label='画像をダウンロード',
#                            data=BytesIO_img,
#                            file_name="output.png",
#                            mime="image/png")

# if __name__ == "__main__":
#     main()
