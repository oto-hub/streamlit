import streamlit as st
import torch
from transformers import BertForMaskedLM, BertTokenizer

# 日本語モデルに統一
TOKENIZER_NAME = "tohoku-nlp/bert-base-japanese"
MODEL_NAME = "tohoku-nlp/bert-base-japanese"

def predict_masked_word(input_text, mask_position):
    """
    BERTを使用してマスクされた単語を予測する関数（日本語対応）
    Args:
        input_text (str): 予測したい文章
        mask_position (int): マスクする単語の位置（0から開始）
    Returns:
        list: 予測された上位5つの単語
    """
    app_text1 = '[CLS]'
    app_text2 = '[SEP]'
    
    tokenizer = BertTokenizer.from_pretrained(TOKENIZER_NAME)
    words = tokenizer.tokenize(input_text)
    
    if 0 <= mask_position < len(words):
        words[mask_position] = '[MASK]'
    else:
        return ["指定された位置が無効です"]
    
    text = app_text1 + ' ' + ' '.join(words) + ' ' + app_text2
    words = tokenizer.tokenize(text)
    word_ids = tokenizer.convert_tokens_to_ids(words)
    word_tensor = torch.tensor([word_ids])

    msk_model = BertForMaskedLM.from_pretrained(MODEL_NAME)
    msk_model.eval()

    x = word_tensor
    y = msk_model(x)
    result = y[0]

    msk_idx = None
    for i, word in enumerate(words):
        if word == '[MASK]':
            msk_idx = i
            break
    if msk_idx is None:
        return ["[MASK]トークンが見つかりませんでした"]
    _, max_ids = torch.topk(result[0][msk_idx], k=5)
    result_words = tokenizer.convert_ids_to_tokens(max_ids.tolist())
    return result_words

def predict_masked_word_manual(input_text):
    """
    手動で[MASK]を含む文章から予測する関数（日本語対応）
    Args:
        input_text (str): [MASK]トークンを含む文章
    Returns:
        list: 予測された上位5つの単語
    """
    app_text1 = '[CLS]'
    app_text2 = '[SEP]'
    text = app_text1 + input_text + app_text2
    tokenizer = BertTokenizer.from_pretrained(TOKENIZER_NAME)
    words = tokenizer.tokenize(text)
    word_ids = tokenizer.convert_tokens_to_ids(words)
    word_tensor = torch.tensor([word_ids])
    msk_model = BertForMaskedLM.from_pretrained(MODEL_NAME)
    msk_model.eval()
    x = word_tensor
    y = msk_model(x)
    result = y[0]
    msk_idx = None
    for i, word in enumerate(words):
        if word == '[MASK]':
            msk_idx = i
            break
    if msk_idx is None:
        return ["[MASK]トークンが見つかりませんでした"]
    _, max_ids = torch.topk(result[0][msk_idx], k=5)
    result_words = tokenizer.convert_ids_to_tokens(max_ids.tolist())
    return result_words

def main():
    """Streamlitアプリのメイン関数"""
    st.title("BERT マスク言語モデル予測（日本語対応）")
    
    input_text = st.text_input('BERTに予測させたい文章を入力してください＞', 
                              placeholder="例: 私は野球が好きです")
    
    # マスク方法を選択
    mask_method = st.radio(
        "マスク方法を選択してください",
        ["ドロップダウンで選択", "数値で位置指定", "手動で[MASK]入力"],
        help="日本語の場合は「ドロップダウンで選択」がおすすめです"
    )
    
    if mask_method == "ドロップダウンで選択":
        if input_text.strip():
            # トークン化してドロップダウンで選択
            tokenizer = BertTokenizer.from_pretrained(TOKENIZER_NAME)
            words = tokenizer.tokenize(input_text)
            
            if words:
                # トークンと位置の辞書を作成
                token_options = {f"{i}: {word}" for i, word in enumerate(words)}
                selected_token = st.selectbox(
                    'マスクする単語を選択してください＞',
                    options=list(token_options),
                    help="トークン化された単語から選択してください"
                )
                
                if selected_token:
                    mask_position = int(selected_token.split(':')[0])
                    
                    if st.button('予測実行'):
                        predictions = predict_masked_word(input_text, mask_position)
                        st.write("**トークン化結果:**")
                        for i, word in enumerate(words):
                            if i == mask_position:
                                st.write(f"**{i}: [{word}] ← マスク対象**")
                            else:
                                st.write(f"{i}: {word}")
                        
                        st.write("**予測結果（上位5つ）:**")
                        for i, word in enumerate(predictions, 1):
                            st.write(f"{i}. {word}")
            else:
                st.warning("文章を入力してください")
        else:
            st.warning("文章を入力してください")
    
    elif mask_method == "数値で位置指定":
        # マスク位置を指定するテキストボックス
        mask_position = st.number_input('マスクする単語の位置（0から開始）＞', 
                                       min_value=0, 
                                       value=2, 
                                       help="0: 最初の単語, 1: 2番目の単語, 2: 3番目の単語...")
        
        if st.button('予測実行'):
            if input_text.strip():
                # トークン化して単語数を表示
                tokenizer = BertTokenizer.from_pretrained(TOKENIZER_NAME)
                words = tokenizer.tokenize(input_text)
                st.write(f"**トークン化結果:** {words}")
                st.write(f"**単語数:** {len(words)}")
                
                if mask_position < len(words):
                    predictions = predict_masked_word(input_text, mask_position)
                    st.write("**予測結果（上位5つ）:**")
                    for i, word in enumerate(predictions, 1):
                        st.write(f"{i}. {word}")
                else:
                    st.error(f"指定された位置 {mask_position} が単語数 {len(words)} を超えています")
            else:
                st.error("文章を入力してください")
    
    else:  # 手動で[MASK]入力
        st.info("文章に[MASK]を直接入力してください。例: 私は[MASK]が好きです")
        
        if st.button('予測実行'):
            if '[MASK]' in input_text:
                # 元の方法で処理
                predictions = predict_masked_word_manual(input_text)
                st.write("**予測結果（上位5つ）:**")
                for i, word in enumerate(predictions, 1):
                    st.write(f"{i}. {word}")
            else:
                st.error("入力テキストに[MASK]トークンが含まれていません")

if __name__ == "__main__":
    main()