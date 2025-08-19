import streamlit as st
import pandas as pd
import re
from collections import Counter

def simple_text_analysis(text):
    """シンプルなテキスト分析（spaCyなし）"""
    # 基本的な品詞分類（簡易版）
    words = re.findall(r'\w+', text.lower())
    
    # 日本語の品詞分類（簡易版）
    nouns = []
    verbs = []
    
    for word in words:
        # 名詞っぽいもの（長い単語、特定のパターン）
        if len(word) > 2 and not word.endswith(('る', 'う', 'く', 'す', 'つ', 'ぬ', 'む', 'る')):
            nouns.append(word)
        # 動詞っぽいもの
        elif word.endswith(('る', 'う', 'く', 'す', 'つ', 'ぬ', 'む')):
            verbs.append(word)
    
    return nouns, verbs

def main():
    st.title("テキスト分析アプリ（軽量版）")
    st.info("🔧 軽量モード: spaCyライブラリが利用できないため、基本的なテキスト分析機能のみ利用可能です。")
    st.markdown("---")
    
    # サイドバーで機能選択
    st.sidebar.title("機能選択")
    function_choice = st.sidebar.selectbox(
        "使用する機能を選択してください",
        ["テキスト入力による分析", 
         "CSVファイルによる分析", 
         "単語出現回数グラフ"]
    )
    
    # 品詞選択（共通）
    select_pos = st.sidebar.multiselect('分析対象', 
        ['名詞', '動詞'], ['名詞'])
    
    st.title("自然言語処理アプリ")
    
    # 機能1: テキスト入力による分析
    if function_choice == "テキスト入力による分析":
        st.header("テキスト入力による分析")
        
        # Input(テキスト入力ボックス)
        input_text = st.text_area('文章入力', height=100)
        
        # Process
        if st.button('実行'):
            if input_text:
                nouns, verbs = simple_text_analysis(input_text)
                
                # Output(結果を出力)
                st.write('入力した文章：', input_text)
                st.markdown("---")
                
                if '名詞' in select_pos:
                    st.subheader("検出された名詞")
                    if nouns:
                        st.write(nouns)
                    else:
                        st.write("名詞が検出されませんでした")
                
                if '動詞' in select_pos:
                    st.subheader("検出された動詞")
                    if verbs:
                        st.write(verbs)
                    else:
                        st.write("動詞が検出されませんでした")
            else:
                st.warning("テキストを入力してください")
    
    # 機能2: CSVファイルによる分析
    elif function_choice == "CSVファイルによる分析":
        st.header("CSVファイルによる分析")
        
        # Input(ファイルアップロード)
        uploaded_file = st.file_uploader("CSVを選択", type='csv')
        
        # Process
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file) # データフレームの作成
            data = data.dropna() # 欠損値処理
            
            # 列選択
            if 'comment' in data.columns:
                text_column = 'comment'
            else:
                text_column = st.selectbox("テキスト列を選択", data.columns)
            
            input_text = ' '.join(data[text_column].astype(str))
            
            if st.button('実行'):
                nouns, verbs = simple_text_analysis(input_text)
                
                # Output(結果を出力)
                st.dataframe(data)
                st.markdown("---")
                
                if '名詞' in select_pos:
                    st.subheader("検出された名詞")
                    if nouns:
                        st.write(nouns[:20])  # 最初の20個のみ表示
                    else:
                        st.write("名詞が検出されませんでした")
                
                if '動詞' in select_pos:
                    st.subheader("検出された動詞")
                    if verbs:
                        st.write(verbs[:20])  # 最初の20個のみ表示
                    else:
                        st.write("動詞が検出されませんでした")
    
    # 機能3: 単語出現回数グラフ
    elif function_choice == "単語出現回数グラフ":
        st.header("単語出現回数グラフ")
        
        # Input(ファイルアップロード)
        uploaded_file = st.file_uploader("CSVを選択", type='csv')
        
        # Process
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file) # データフレームの作成
            data = data.dropna() # 欠損値処理
            
            # 列選択
            if 'comment' in data.columns:
                text_column = 'comment'
            else:
                text_column = st.selectbox("テキスト列を選択", data.columns)
            
            input_text = ' '.join(data[text_column].astype(str))
            
            if st.button('実行'):
                # 単語の出現回数をカウント
                words = re.findall(r'\w+', input_text.lower())
                word_counts = Counter(words)
                
                # 上位10個の単語を表示
                top_words = word_counts.most_common(10)
                
                # グラフ表示
                if top_words:
                    word_df = pd.DataFrame(top_words, columns=['単語', '出現回数'])
                    st.bar_chart(word_df.set_index('単語'))
                    
                    st.subheader("出現回数データ")
                    st.dataframe(word_df)
                else:
                    st.write("単語が検出されませんでした")

if __name__ == "__main__":
    main()
