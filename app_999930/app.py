import streamlit as st
import cv2
import numpy as np
import torch
from PIL import Image
from io import BytesIO

# Streamlit Cloud用の設定
@st.cache_resource
def load_models():
    """モデルをキャッシュして読み込み"""
    with st.spinner("モデルを読み込み中..."):
        model1 = torch.hub.load("bryandlee/animegan2-pytorch:main", "generator", pretrained="face_paint_512_v2", trust_repo=True)
        model2 = torch.hub.load("bryandlee/animegan2-pytorch:main", "generator", pretrained="celeba_distill", trust_repo=True)
        face2paint = torch.hub.load("bryandlee/animegan2-pytorch:main", "face2paint", trust_repo=True)
        return model1, model2, face2paint

def apply_animegan2(model, image, size=512):
    """AnimeGAN2モデルを適用する関数"""
    # 画像を適切なサイズにリサイズ
    image_resized = image.resize((size, size))
    
    # モデルを適用
    with torch.no_grad():
        # 画像をテンソルに変換
        img_tensor = torch.from_numpy(np.array(image_resized)).permute(2, 0, 1).float() / 255.0
        img_tensor = img_tensor.unsqueeze(0)
        
        # モデルで変換
        output = model(img_tensor)
        
        # 結果を画像に変換
        output_img = output.squeeze(0).permute(1, 2, 0).detach().numpy()
        output_img = np.clip(output_img * 255, 0, 255).astype(np.uint8)
        
        return Image.fromarray(output_img)

def main():   
    # モデルのロード
    model1, model2, face2paint = load_models()

    # Streamlit UI
    st.title("🎨 アニメ顔変換アプリ")
    st.markdown("---")
    
    # サイドバーに設定を配置
    st.sidebar.header("設定")
    
    input_method = st.sidebar.radio(
        "画像の入力方法",
        ["📁 画像をアップロード", "📷 Webカメラで撮影"]
    )
    
    select_model = st.sidebar.selectbox(
        '変換モデル',
        ['face_paint_512_v2', 'celeba_distill']
    )
    
    # 変換度合いの調整
    blend_strength = st.sidebar.slider(
        "変換度合いの調整", 
        0.0, 0.5, 1.0, 0.01,
        help="0.0: 元画像に近い、1.0: 完全変換"
    )
    
    # モデル説明
    if select_model == 'face_paint_512_v2':
        st.sidebar.info("**face_paint_512_v2**: より鮮やかでアニメらしい変換")
    else:
        st.sidebar.info("**celeba_distill**: より自然でリアルな変換")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("AnimeGAN2を用いたアニメ顔変換アプリケーション")
    
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

        # 変換処理
        with st.spinner("変換中..."):
            try:
                # AnimeGAN2変換
                tg_img_pil = Image.fromarray(tg_img)
                
                # 選択されたモデルで変換
                if select_model == 'face_paint_512_v2':
                    output_img = apply_animegan2(model1, tg_img_pil, size=512)
                else:
                    output_img = apply_animegan2(model2, tg_img_pil, size=512)
                
                # 変換度合いの調整
                if blend_strength < 1.0:
                    output_img_array = np.array(output_img)
                    original_resized = cv2.resize(original_img, (output_img_array.shape[1], output_img_array.shape[0]))
                    blended_img = (1 - blend_strength) * original_resized + blend_strength * output_img_array
                    blended_img = np.clip(blended_img, 0, 255).astype(np.uint8)
                    final_output = Image.fromarray(blended_img)
                else:
                    final_output = output_img
                
            except Exception as e:
                st.error(f"変換中にエラーが発生しました: {str(e)}")
                return

        # ダウンロード用に画像を準備
        final_output_array = np.array(final_output)
        ret, enco_img = cv2.imencode(".png", cv2.cvtColor(final_output_array, cv2.COLOR_RGB2BGR))
        BytesIO_img = BytesIO(enco_img.tobytes())

        # 結果表示
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📸 元画像")
            st.image(original_img, caption="元の画像", use_container_width=True)

        with col2:
            st.subheader("🎨 変換結果")
            st.image(final_output, caption=f"変換後の画像 (強度: {blend_strength:.2f})", use_container_width=True)

        # 変換度合いの視覚的表示
        st.markdown("---")
        st.subheader("📊 変換度合い")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.progress(blend_strength)
            st.caption(f"変換強度: {blend_strength:.2f} ({blend_strength*100:.0f}%)")

        # ダウンロードボタン
        st.markdown("---")
        st.download_button(
            label='💾 変換画像をダウンロード',
            data=BytesIO_img,
            file_name=f"anime_{select_model}_{blend_strength:.2f}.png",
            mime="image/png",
            use_container_width=True
        )
    else:
        st.info("👆 上記から画像をアップロードするか、Webカメラで撮影してください。")

# アプリケーションのエントリポイント
if __name__ == '__main__':
    main()