import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

def apply_simple_filter(image):
    """シンプルなフィルター効果（AnimeGAN2なし）"""
    # 画像をPIL形式に変換
    if isinstance(image, np.ndarray):
        pil_image = Image.fromarray(image)
    else:
        pil_image = image
    
    # グレースケール変換
    gray = pil_image.convert('L')
    
    # カラー画像に戻す（セピア調）
    sepia = Image.new('RGB', pil_image.size)
    for x in range(pil_image.width):
        for y in range(pil_image.height):
            r, g, b = pil_image.getpixel((x, y))
            gray_val = int(0.299 * r + 0.587 * g + 0.114 * b)
            sepia.putpixel((x, y), (int(gray_val * 1.2), int(gray_val * 0.8), int(gray_val * 0.6)))
    
    return sepia

def main():   
    st.title("🎨 画像フィルターアプリ（軽量版）")
    st.info("🔧 軽量モード: AnimeGAN2ライブラリが利用できないため、基本的なフィルター機能のみ利用可能です。")
    st.markdown("---")
    
    # サイドバーに設定を配置
    st.sidebar.header("設定")
    
    input_method = st.sidebar.radio(
        "画像の入力方法",
        ["📁 画像をアップロード", "📷 Webカメラで撮影"]
    )
    
    filter_type = st.sidebar.selectbox(
        'フィルター効果',
        ['セピア調', 'グレースケール', 'ネガポジ反転']
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("軽量版画像フィルターアプリケーション")
    
    # メイン画面
    st.header("🖼️ 画像変換")
    
    # 選択された方法に応じてUIを表示
    if input_method == "📁 画像をアップロード":
        upload_img = st.file_uploader("画像をアップロードしてください", type=['png','jpg','jpeg'])
        camera_img = None
    else:
        upload_img = None
        camera_img = st.camera_input("Webカメラで撮影してください", key="camera")
        
        if camera_img is not None:
            st.info("📸 撮影した画像が表示されます。撮影ボタンを押して画像を確定してください。")

    # Process
    input_image = upload_img if upload_img is not None else camera_img
    
    if input_image is not None:
        # 画像を処理
        bytes_data = input_image.getvalue()
        tg_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        tg_img = cv2.cvtColor(tg_img, cv2.COLOR_BGR2RGB)
        original_img = tg_img.copy()

        # 元画像を表示
        st.subheader("元画像")
        st.image(original_img, caption="元の画像", use_container_width=True)

        # 変換処理
        with st.spinner("変換中..."):
            pil_image = Image.fromarray(original_img)
            
            if filter_type == 'セピア調':
                result_img = apply_simple_filter(pil_image)
            elif filter_type == 'グレースケール':
                result_img = pil_image.convert('L')
            elif filter_type == 'ネガポジ反転':
                result_img = Image.eval(pil_image, lambda x: 255 - x)

        # 結果を表示
        st.subheader("変換結果")
        st.image(result_img, caption=f"{filter_type}フィルター適用", use_container_width=True)
        
        # ダウンロードボタン
        if hasattr(result_img, 'save'):
            buf = BytesIO()
            result_img.save(buf, format='PNG')
            st.download_button(
                label="変換画像をダウンロード",
                data=buf.getvalue(),
                file_name=f"filtered_{filter_type}.png",
                mime="image/png"
            )

if __name__ == "__main__":
    main()