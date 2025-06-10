import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO

st.title("骨格推定アプリ（YOLOv8 + Streamlit）")
st.subtitle('mediapipeを使えなかったので微妙な仕上がりです。。。1人ずつ写ってください')
model = YOLO("yolov8n-pose.pt")

def main():
    upload_img = st.camera_input("インカメラ画像")

    if upload_img is not None:
        # 画像読み込み
        image = Image.open(upload_img)
        if image.mode != "RGB":
            image = image.convert("RGB")
        img_array = np.array(image)

        # 推論
        results = model.predict(img_array, imgsz=640, save=False, verbose=False)[0]
        keypoints = results.keypoints  # 座標を取得

        if keypoints is not None and keypoints.data.numel() > 0:
            kp = keypoints.data[0].cpu().numpy()  # 最初の人物のみ

            # 手の判定：左(7), 右(4) の手首と肩(左5, 右2)
            left_wrist_y = kp[7][1]
            left_shoulder_y = kp[5][1]
            right_wrist_y = kp[4][1]
            right_shoulder_y = kp[2][1]

            left_state = "挙がっている" if left_wrist_y < left_shoulder_y else "挙がっていない"
            right_state = "挙がっている" if right_wrist_y < right_shoulder_y else "挙がっていない"

            st.text(f"左手：{left_state}")
            st.text(f"右手：{right_state}")

            # matplotlibで描画
            fig, ax = plt.subplots()
            ax.imshow(img_array)
            ax.scatter(kp[:, 0], kp[:, 1], c="red", s=10)

            for idx, (x, y, conf) in enumerate(kp):
                if conf > 0.5:
                    ax.text(x, y, str(idx), color="yellow", fontsize=6)

            ax.axis("off")
            st.pyplot(fig)
        else:
            st.warning("人物が検出されませんでした。")

if __name__ == "__main__":
    main()
