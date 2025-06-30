import streamlit as st
import pandas as pd
import spacy

def main():
    # モデルの読み込み
    nlp = spacy.load('ja_ginza')
    # 品詞のリスト
    pos_dic = {'名詞':'NOUN', '代名詞':'PRON', '固有名詞':'PROPN','動詞':'VERB'}
    
    # サイドバーで機能選択
    st.sidebar.title("機能選択")
    function_choice = st.sidebar.selectbox(
        "使用する機能を選択してください",
        ["テキスト入力による品詞抽出", 
         "CSVファイルによる品詞抽出", 
         "CSVファイルによる出現回数グラフ",
         "CSVファイルによる列選択とグラフ"]
    )
    
    # 品詞選択（共通）
    select_pos = st.sidebar.multiselect('品詞選択', 
        ['名詞','代名詞','固有名詞','動詞'], ['名詞'])
    
    st.title("自然言語処理アプリ")
    
    # 機能1: テキスト入力による品詞抽出
    if function_choice == "テキスト入力による品詞抽出":
        st.header("テキスト入力による品詞抽出")
        
        # Input(テキスト入力ボックス)
        input_text = st.text_input('文章入力')
        
        # Process
        if st.button('実行'):
            doc = nlp(input_text) # 形態素解析
            output_word = []
            tg_pos = [pos_dic[x] for x in select_pos]  
            for token in doc:
               if token.pos_ in tg_pos: # 特定の品詞を抽出
                   output_word.append(token.lemma_)

            # Output(結果を出力)
            st.write('入力した文章：', input_text)
            st.write(output_word)
    
    # 機能2: CSVファイルによる品詞抽出
    elif function_choice == "CSVファイルによる品詞抽出":
        st.header("CSVファイルによる品詞抽出")
        
        # Input(ファイルアップロード)
        uploaded_file = st.file_uploader("CSVを選択", type='csv')
        
        # Process
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file) # データフレームの作成
            data = data.dropna() # 欠損値処理
            input_text = data['comment'] # comment列の抽出
            input_text = ' '.join(input_text)
            if st.button('実行'):
                doc = nlp(input_text) # 形態素解析
                output_word = []
                tg_pos = [pos_dic[x] for x in select_pos]
                for token in doc: # 特定の品詞を抽出
                    if token.pos_ in tg_pos: 
                        output_word.append(token.lemma_)

                # Output(結果を出力)
                st.dataframe(data)
                st.write(output_word)
    
    # 機能3: CSVファイルによる出現回数グラフ
    elif function_choice == "CSVファイルによる出現回数グラフ":
        st.header("CSVファイルによる出現回数グラフ")
        
        # Input(ファイルアップロード)
        uploaded_file = st.file_uploader("CSVを選択", type='csv')
        
        # Process
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file) # データフレームの作成
            data = data.dropna() # 欠損値処理
            input_text = data['comment'] # comment列の抽出
            input_text = ' '.join(input_text)
            if st.button('実行'):
                doc = nlp(input_text) # 形態素解析
                output_word = []
                tg_pos = [pos_dic[x] for x in select_pos]
                for token in doc: # 特定の品詞を抽出
                    if token.pos_ in tg_pos: 
                        output_word.append(token.lemma_)

                # 抽出結果を処理するためのデータフレームを生成
                output_df = pd.DataFrame({'Word':output_word})

                # 単語ごとに出現回数を計算して、回数の多い順に並び替え
                word_counts = output_df.groupby('Word').size().reset_index()
                word_counts.columns = ['Word', 'count']
                word_counts.sort_values(by='count', ascending=False, inplace=True)
                output_df = word_counts.set_index('Word')

                # Output(結果を出力)
                st.dataframe(data)
                st.bar_chart(data=output_df.head(10)) # 上位10件を表示
    
    # 機能4: CSVファイルによる列選択とグラフ
    elif function_choice == "CSVファイルによる列選択とグラフ":
        st.header("CSVファイルによる列選択とグラフ")
        
        # Input(ファイルアップロード)
        uploaded_file = st.file_uploader("CSVを選択", type='csv')
        
        # Process
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file) # データフレームの作成
            tg_col = st.selectbox('対象列選択', data.columns) # 抽出したい列の選択
            if tg_col is not None:
                data = data.dropna() # 欠損値処理
                input_text = data[tg_col] # 指定した列の抽出
                input_text = ' '.join(input_text)
                if st.button('実行'):
                    doc = nlp(input_text) # 形態素解析
                    output_word = []
                    tg_pos = [pos_dic[x] for x in select_pos]
                    for token in doc: # 特定の品詞を抽出
                        if token.pos_ in tg_pos: 
                            output_word.append(token.lemma_)

                    # 抽出結果を処理するためのデータフレームを生成
                    output_df = pd.DataFrame({'Word':output_word})

                    # 単語ごとに出現回数を計算して、回数の多い順に並び替え
                    word_counts = output_df.groupby('Word').size().reset_index()
                    word_counts.columns = ['Word', 'count']
                    word_counts.sort_values(by='count', ascending=False, inplace=True)
                    output_df = word_counts.set_index('Word')

                    # Output(結果を出力)
                    st.dataframe(data)
                    st.bar_chart(data=output_df.head(10)) # 上位10件を表示
                
if __name__ == "__main__":
    main()