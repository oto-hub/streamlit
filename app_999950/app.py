import streamlit as st
import random

def simple_word_prediction(input_text, mask_position):
    """
    シンプルな単語予測（BERTなし）
    Args:
        input_text (str): 予測したい文章
        mask_position (int): マスクする単語の位置
    Returns:
        list: 予測された単語の候補
    """
    words = input_text.split()
    
    if 0 <= mask_position < len(words):
        # 簡単な予測ロジック
        common_words = ['です', 'ます', 'する', 'いる', 'ある', 'なる', '見る', '聞く', '行く', '来る']
        context_words = ['良い', '悪い', '大きい', '小さい', '新しい', '古い', '高い', '安い']
        
        # 文脈に応じて候補を選択
        if any(word in input_text for word in ['好き', '嫌い', '良い', '悪い']):
            candidates = ['です', 'です', 'ます', 'だ', 'である']
        elif any(word in input_text for word in ['行く', '来る', '見る', '聞く']):
            candidates = ['ます', 'です', 'する', 'いる']
        else:
            candidates = common_words + context_words
        
        return random.sample(candidates, min(5, len(candidates)))
    else:
        return ["指定された位置が無効です"]

def main():
    """Streamlitアプリのメイン関数"""
    st.title("単語予測アプリ（軽量版）")
    st.info("🔧 軽量モード: BERTライブラリが利用できないため、基本的な単語予測機能のみ利用可能です。")
    st.markdown("---")
    
    input_text = st.text_input('予測させたい文章を入力してください＞', 
                              placeholder="例: 私は野球が好きです")
    
    # マスク方法を選択
    mask_method = st.radio(
        "マスク方法を選択してください",
        ["ドロップダウンで選択", "数値で位置指定"],
        help="軽量版では基本的な予測機能のみ利用可能です"
    )
    
    if mask_method == "ドロップダウンで選択":
        if input_text.strip():
            # 単語分割してドロップダウンで選択
            words = input_text.split()
            
            if words:
                st.subheader("単語の選択")
                st.write("予測したい単語の位置を選択してください：")
                
                # 単語と位置を表示
                for i, word in enumerate(words):
                    st.write(f"{i}: {word}")
                
                mask_position = st.selectbox(
                    "マスクする単語の位置を選択",
                    range(len(words)),
                    format_func=lambda x: f"{x}: {words[x]}"
                )
                
                if st.button("予測実行"):
                    with st.spinner("予測中..."):
                        predictions = simple_word_prediction(input_text, mask_position)
                    
                    st.subheader("予測結果")
                    st.write(f"元の文章: {input_text}")
                    st.write(f"マスク位置: {mask_position} ({words[mask_position]})")
                    st.write("予測候補:")
                    
                    for i, pred in enumerate(predictions, 1):
                        st.write(f"{i}. {pred}")
            else:
                st.warning("文章を入力してください")
    
    elif mask_method == "数値で位置指定":
        if input_text.strip():
            words = input_text.split()
            st.write(f"文章の単語数: {len(words)}")
            
            for i, word in enumerate(words):
                st.write(f"{i}: {word}")
            
            mask_position = st.number_input(
                "マスクする単語の位置（0から開始）",
                min_value=0,
                max_value=len(words)-1 if words else 0,
                value=0
            )
            
            if st.button("予測実行"):
                with st.spinner("予測中..."):
                    predictions = simple_word_prediction(input_text, mask_position)
                
                st.subheader("予測結果")
                st.write(f"元の文章: {input_text}")
                if words:
                    st.write(f"マスク位置: {mask_position} ({words[mask_position]})")
                st.write("予測候補:")
                
                for i, pred in enumerate(predictions, 1):
                    st.write(f"{i}. {pred}")
    
    st.markdown("---")
    st.sidebar.markdown("---")
    st.sidebar.markdown("軽量版単語予測アプリケーション")

if __name__ == "__main__":
    main()