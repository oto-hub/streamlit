import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from io import BytesIO, BufferedReader

# --- MediaPipeモデルの初期化（一度だけ実行するためにキャッシュ化） ---
@st.cache_resource
def load_mediapipe_models():
    """MediaPipeのPoseとFaceMeshモデルをロードしてキャッシュする関数"""
    mp_pose = mp.solutions.pose
    mp_face_mesh = mp.solutions.face_mesh

    pose_model = mp_pose.Pose(static_image_mode=True,
                              min_detection_confidence=0.5,
                              model_complexity=2)
    face_mesh_model = mp_face_mesh.FaceMesh(static_image_mode=True,
                                             max_num_faces=1,
                                             refine_landmarks=True,
                                             min_detection_confidence=0.5)
    return pose_model, face_mesh_model, mp_pose, mp_face_mesh

# 描画ユーティリティはモデルとは別に定義
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def main():
    """Streamlitアプリのメイン関数"""

    # モデルとモジュールをロード
    pose, face_mesh, mp_pose, mp_face_mesh = load_mediapipe_models()

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
        img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB) # MediaPipeはRGBを期待
        output_img = img.copy() # 描画用にコピー

        if mode == "骨格推定（画像）":
            results = pose.process(img)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    output_img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()) # スタイル追加
                st.text(f'右手は：{"挙がっている" if results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y < results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y else "挙がっていない"}')
                st.text(f'左手は：{"挙がっている" if results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y < results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y else "挙がっていない"}')

            else:
                st.warning("人物が検出できませんでした。")

        elif mode == "目線判定（画像）":
            results = face_mesh.process(img)

            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]

                # 目線判定 (右目の虹彩と目尻/目頭で判定)
                # 左目 (画面上では右側) を使ってより安定した判定を行う
                # 目の中心点: (左目尻(33) + 左目頭(133)) / 2
                # 虹彩の中心: 左目(468)
                iris_x = face_landmarks.landmark[mp_face_mesh.FACEMESH_IRISES[0][0].start_index].x
                eye_left_inner_x = face_landmarks.landmark[mp_face_mesh.FACEMESH_LEFT_EYE[0][0].start_index].x
                eye_right_outer_x = face_landmarks.landmark[mp_face_mesh.FACEMESH_LEFT_EYE[0][10].start_index].x
                
                # 目全体の中央を基準に虹彩の位置を比較
                eye_center_x = (eye_left_inner_x + eye_right_outer_x) / 2
                
                gaze_dir = '正面'
                if iris_x < eye_center_x - 0.02: # 閾値を設けて安定化
                    gaze_dir = '右'
                elif iris_x > eye_center_x + 0.02:
                    gaze_dir = '左'

                st.text(f'目線は：{gaze_dir}')

                # 描画
                mp_drawing.draw_landmarks(
                    image=output_img,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
                )

                mp_drawing.draw_landmarks(
                    image=output_img,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style()
                )

                # 両目を囲う矩形（視認性向上）
                ih, iw, _ = img.shape
                # MediaPipeのランドマークインデックスを使用して目の外側と内側のポイントを取得
                # 左目: 33, 133, 160, 144, 159, 145, 158, 153, 144, 163, 7, 33
                # 右目: 263, 362, 387, 373, 386, 374, 385, 380, 373, 390, 249, 263
                # これらのランドマークから目のバウンディングボックスを計算
                left_eye_landmarks_indices = [
                    33, 7, 163, 144, 145, 153, 158, 159, 160, 133
                ]
                right_eye_landmarks_indices = [
                    263, 249, 390, 373, 374, 380, 385, 386, 387, 362
                ]

                all_x_coords = []
                all_y_coords = []
                
                # 左目の矩形
                for idx in left_eye_landmarks_indices:
                    all_x_coords.append(face_landmarks.landmark[idx].x)
                    all_y_coords.append(face_landmarks.landmark[idx].y)
                
                if all_x_coords and all_y_coords: # リストが空でないことを確認
                    x1 = int(min(all_x_coords) * iw)
                    x2 = int(max(all_x_coords) * iw)
                    y1 = int(min(all_y_coords) * ih)
                    y2 = int(max(all_y_coords) * ih)
                    cv2.rectangle(output_img, (x1 - 5, y1 - 5), (x2 + 5, y2 + 5), (0, 255, 0), 2) # 余白を追加

                all_x_coords = []
                all_y_coords = []
                # 右目の矩形
                for idx in right_eye_landmarks_indices:
                    all_x_coords.append(face_landmarks.landmark[idx].x)
                    all_y_coords.append(face_landmarks.landmark[idx].y)

                if all_x_coords and all_y_coords: # リストが空でないことを確認
                    x1 = int(min(all_x_coords) * iw)
                    x2 = int(max(all_x_coords) * iw)
                    y1 = int(min(all_y_coords) * ih)
                    y2 = int(max(all_y_coords) * ih)
                    cv2.rectangle(output_img, (x1 - 5, y1 - 5), (x2 + 5, y2 + 5), (0, 255, 0), 2) # 余白を追加
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

# スクリプトが直接実行された場合にmain関数を呼び出す
if __name__ == "__main__":
    main()
