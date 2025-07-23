import streamlit as st
import pandas as pd
import spacy
from spacy import displacy
import streamlit.components.v1 as components

# def main():
#     # モデルの読み込み（エラーハンドリング付き）
#     try:
#         nlp = spacy.load('ja_ginza')
#     except OSError:
#         st.error("""
#         ❌ 日本語モデル（ja_ginza）がインストールされていません。
        
#         初回起動時は、以下のコマンドでモデルをダウンロードしてください：
#         ```
#         python -m spacy download ja_ginza
#         ```
#         """)
#         st.stop()
    
#     # 品詞のリスト
#     pos_dic = {'名詞':'NOUN', '代名詞':'PRON', '固有名詞':'PROPN','動詞':'VERB'}
    
#     # サイドバーで機能選択
#     st.sidebar.title("機能選択")
#     function_choice = st.sidebar.selectbox(
#         "使用する機能を選択してください",
#         ["テキスト入力による品詞抽出", 
#          "CSVファイルによる品詞抽出", 
#          "CSVファイルによる出現回数グラフ",
#          "CSVファイルによる列選択とグラフ",
#          "依存関係解析"]
#     )
    
#     # 品詞選択（共通）
#     select_pos = st.sidebar.multiselect('品詞選択', 
#         ['名詞','代名詞','固有名詞','動詞'], ['名詞'])
    
#     st.title("自然言語処理アプリ")
    
#     # 機能1: テキスト入力による品詞抽出
#     if function_choice == "テキスト入力による品詞抽出":
#         st.header("テキスト入力による品詞抽出")
        
#         # Input(テキスト入力ボックス)
#         input_text = st.text_input('文章入力')
        
#         # Process
#         if st.button('実行'):
#             doc = nlp(input_text) # 形態素解析
#             output_word = []
#             tg_pos = [pos_dic[x] for x in select_pos]  
#             for token in doc:
#                if token.pos_ in tg_pos: # 特定の品詞を抽出
#                    output_word.append(token.lemma_)

#             # Output(結果を出力)
#             st.write('入力した文章：', input_text)
#             st.write(output_word)
    
#     # 機能2: CSVファイルによる品詞抽出
#     elif function_choice == "CSVファイルによる品詞抽出":
#         st.header("CSVファイルによる品詞抽出")
        
#         # Input(ファイルアップロード)
#         uploaded_file = st.file_uploader("CSVを選択", type='csv')
        
#         # Process
#         if uploaded_file is not None:
#             data = pd.read_csv(uploaded_file) # データフレームの作成
#             data = data.dropna() # 欠損値処理
#             input_text = data['comment'] # comment列の抽出
#             input_text = ' '.join(input_text)
#             if st.button('実行'):
#                 doc = nlp(input_text) # 形態素解析
#                 output_word = []
#                 tg_pos = [pos_dic[x] for x in select_pos]
#                 for token in doc: # 特定の品詞を抽出
#                     if token.pos_ in tg_pos: 
#                         output_word.append(token.lemma_)

#                 # Output(結果を出力)
#                 st.dataframe(data)
#                 st.write(output_word)
    
#     # 機能3: CSVファイルによる出現回数グラフ
#     elif function_choice == "CSVファイルによる出現回数グラフ":
#         st.header("CSVファイルによる出現回数グラフ")
        
#         # Input(ファイルアップロード)
#         uploaded_file = st.file_uploader("CSVを選択", type='csv')
        
#         # Process
#         if uploaded_file is not None:
#             data = pd.read_csv(uploaded_file) # データフレームの作成
#             data = data.dropna() # 欠損値処理
#             input_text = data['comment'] # comment列の抽出
#             input_text = ' '.join(input_text)
#             if st.button('実行'):
#                 doc = nlp(input_text) # 形態素解析
#                 output_word = []
#                 tg_pos = [pos_dic[x] for x in select_pos]
#                 for token in doc: # 特定の品詞を抽出
#                     if token.pos_ in tg_pos: 
#                         output_word.append(token.lemma_)

#                 # 抽出結果を処理するためのデータフレームを生成
#                 output_df = pd.DataFrame({'Word':output_word})

#                 # 単語ごとに出現回数を計算して、回数の多い順に並び替え
#                 word_counts = output_df.groupby('Word').size().reset_index()
#                 word_counts.columns = ['Word', 'count']
#                 word_counts.sort_values(by='count', ascending=False, inplace=True)
#                 output_df = word_counts.set_index('Word')

#                 # Output(結果を出力)
#                 st.dataframe(data)
#                 st.bar_chart(data=output_df.head(10)) # 上位10件を表示
    
#     # 機能4: CSVファイルによる列選択とグラフ
#     elif function_choice == "CSVファイルによる列選択とグラフ":
#         st.header("CSVファイルによる列選択とグラフ")
        
#         # Input(ファイルアップロード)
#         uploaded_file = st.file_uploader("CSVを選択", type='csv')
        
#         # Process
#         if uploaded_file is not None:
#             data = pd.read_csv(uploaded_file) # データフレームの作成
#             tg_col = st.selectbox('対象列選択', data.columns) # 抽出したい列の選択
#             if tg_col is not None:
#                 data = data.dropna() # 欠損値処理
#                 input_text = data[tg_col] # 指定した列の抽出
#                 input_text = ' '.join(input_text)
#                 if st.button('実行'):
#                     doc = nlp(input_text) # 形態素解析
#                     output_word = []
#                     tg_pos = [pos_dic[x] for x in select_pos]
#                     for token in doc: # 特定の品詞を抽出
#                         if token.pos_ in tg_pos: 
#                             output_word.append(token.lemma_)

#                     # 抽出結果を処理するためのデータフレームを生成
#                     output_df = pd.DataFrame({'Word':output_word})

#                     # 単語ごとに出現回数を計算して、回数の多い順に並び替え
#                     word_counts = output_df.groupby('Word').size().reset_index()
#                     word_counts.columns = ['Word', 'count']
#                     word_counts.sort_values(by='count', ascending=False, inplace=True)
#                     output_df = word_counts.set_index('Word')

#                     # Output(結果を出力)
#                     st.dataframe(data)
#                     st.bar_chart(data=output_df.head(10)) # 上位10件を表示
    
#     # 機能5: 依存関係解析
#     elif function_choice == "依存関係解析":
#         st.header("🔍 依存関係解析")
#         st.markdown("---")
        
#         # 日本語の説明
#         st.markdown("""
#         ### 📝 使い方
#         1. テキストを入力してください（日本語または英語）
#         2. 「解析実行」ボタンをクリックしてください
#         3. 依存関係解析の結果が表示されます
#         """)
        
#         # テキスト入力
#         text_input = st.text_area(
#             "解析したいテキストを入力してください:",
#             placeholder="例: 私は今日学校に行きました。",
#             height=150
#         )
        
#         # 言語選択
#         language = st.selectbox(
#             "言語を選択してください:",
#             ["日本語", "英語"],
#             help="日本語の場合はja_ginza、英語の場合はen_core_web_smを使用します"
#         )
        
#         # 解析実行ボタン
#         if st.button("🔍 解析実行", type="primary"):
#             if text_input.strip():
#                 with st.spinner("解析中..."):
#                     try:
#                         # 言語モデルの読み込み
#                         if language == "日本語":
#                             nlp = spacy.load("ja_ginza")
#                         else:
#                             nlp = spacy.load("en_core_web_sm")
                        
#                         # テキストの解析
#                         doc = nlp(text_input)
                        
#                         # 結果表示
#                         st.success("✅ 解析が完了しました！")
                        
#                         # 基本情報の表示
#                         col1, col2, col3 = st.columns(3)
#                         with col1:
#                             st.metric("トークン数", len(doc))
#                         with col2:
#                             st.metric("文の数", len(list(doc.sents)))
#                         with col3:
#                             st.metric("固有表現", len(doc.ents))
                        
#                         # 依存関係解析の可視化
#                         st.subheader("📊 依存関係解析")
                        
#                         # displacyでHTMLを生成
#                         html = displacy.render(
#                             doc, 
#                             style='dep', 
#                             jupyter=False, 
#                             options={'distance': 60, 'compact': True}
#                         )
                        
#                         # HTMLをStreamlitで表示
#                         components.html(html, height=400, scrolling=True)
                        
#                         # 詳細情報の表示
#                         st.subheader("📋 詳細情報")
                        
#                         # トークン情報
#                         if st.checkbox("トークン詳細を表示"):
#                             token_data = []
#                             for token in doc:
#                                 token_data.append({
#                                     "トークン": token.text,
#                                     "品詞": token.pos_,
#                                     "詳細品詞": token.tag_,
#                                     "依存関係": token.dep_,
#                                     "親トークン": token.head.text if token.head else "ROOT"
#                                 })
                            
#                             st.dataframe(token_data, use_container_width=True)
                        
#                         # 固有表現
#                         if doc.ents and st.checkbox("固有表現を表示"):
#                             ent_data = []
#                             for ent in doc.ents:
#                                 ent_data.append({
#                                     "テキスト": ent.text,
#                                     "ラベル": ent.label_,
#                                     "説明": ent.label_
#                                 })
                            
#                             st.dataframe(ent_data, use_container_width=True)
                        
#                         # 文の分割
#                         if st.checkbox("文の分割を表示"):
#                             for i, sent in enumerate(doc.sents, 1):
#                                 st.write(f"**文 {i}:** {sent.text}")
                        
#                     except OSError as e:
#                         if "ja_ginza" in str(e):
#                             st.error("""
#                             ❌ 日本語モデル（ja_ginza）がインストールされていません。
                            
#                             Streamlit Cloudで実行する場合は、以下のコマンドでモデルをダウンロードしてください：
#                             ```
#                             python -m spacy download ja_ginza
#                             ```
#                             """)
                            
#                             # モデルダウンロードボタン
#                             if st.button("📥 日本語モデルをダウンロード"):
#                                 with st.spinner("ダウンロード中..."):
#                                     try:
#                                         import subprocess
#                                         import sys
#                                         result = subprocess.run([
#                                             sys.executable, "-m", "spacy", "download", "ja_ginza"
#                                         ], capture_output=True, text=True, timeout=300)
#                                         if result.returncode == 0:
#                                             st.success("✅ 日本語モデルのダウンロードが完了しました！")
#                                             st.rerun()
#                                         else:
#                                             st.error(f"❌ ダウンロードに失敗しました: {result.stderr}")
#                                             st.info("💡 手動でダウンロードする場合は、ターミナルで以下を実行してください：")
#                                             st.code("python -m spacy download ja_ginza")
#                                     except subprocess.TimeoutExpired:
#                                         st.error("❌ ダウンロードがタイムアウトしました。時間をおいて再試行してください。")
#                                     except Exception as download_error:
#                                         st.error(f"❌ ダウンロードエラー: {download_error}")
#                                         st.info("💡 手動でダウンロードする場合は、ターミナルで以下を実行してください：")
#                                         st.code("python -m spacy download ja_ginza")
                                        
#                         elif "en_core_web_sm" in str(e):
#                             st.error("""
#                             ❌ 英語モデル（en_core_web_sm）がインストールされていません。
                            
#                             Streamlit Cloudで実行する場合は、以下のコマンドでモデルをダウンロードしてください：
#                             ```
#                             python -m spacy download en_core_web_sm
#                             ```
#                             """)
                            
#                             # モデルダウンロードボタン
#                             if st.button("📥 英語モデルをダウンロード"):
#                                 with st.spinner("ダウンロード中..."):
#                                     try:
#                                         import subprocess
#                                         import sys
#                                         result = subprocess.run([
#                                             sys.executable, "-m", "spacy", "download", "en_core_web_sm"
#                                         ], capture_output=True, text=True, timeout=300)
#                                         if result.returncode == 0:
#                                             st.success("✅ 英語モデルのダウンロードが完了しました！")
#                                             st.rerun()
#                                         else:
#                                             st.error(f"❌ ダウンロードに失敗しました: {result.stderr}")
#                                             st.info("💡 手動でダウンロードする場合は、ターミナルで以下を実行してください：")
#                                             st.code("python -m spacy download en_core_web_sm")
#                                     except subprocess.TimeoutExpired:
#                                         st.error("❌ ダウンロードがタイムアウトしました。時間をおいて再試行してください。")
#                                     except Exception as download_error:
#                                         st.error(f"❌ ダウンロードエラー: {download_error}")
#                                         st.info("💡 手動でダウンロードする場合は、ターミナルで以下を実行してください：")
#                                         st.code("python -m spacy download en_core_web_sm")
#                         else:
#                             st.error(f"❌ モデルの読み込みエラー: {e}")
                            
#                     except Exception as e:
#                         st.error(f"❌ 予期しないエラーが発生しました: {e}")
#             else:
#                 st.warning("⚠️ テキストを入力してください。")
        
#         # サンプルテキスト
#         st.markdown("---")
#         st.subheader("💡 サンプルテキスト")
        
#         sample_texts = {
#             "日本語": [
#                 "私は今日学校に行きました。",
#                 "田中さんは東京で働いています。",
#                 "この本はとても面白いです。"
#             ],
#             "英語": [
#                 "I went to school today.",
#                 "John works in Tokyo.",
#                 "This book is very interesting."
#             ]
#         }
        
#         selected_lang = st.selectbox("サンプル言語:", ["日本語", "英語"])
#         if selected_lang in sample_texts:
#             sample = st.selectbox("サンプルを選択:", sample_texts[selected_lang])
#             if st.button(f"「{sample}」を使用"):
#                 st.session_state.sample_text = sample
#                 st.rerun()
        
#         # セッション状態からサンプルテキストを復元
#         if 'sample_text' in st.session_state:
#             st.text_area("選択されたサンプル:", st.session_state.sample_text, disabled=True)
#             if st.button("このテキストで解析"):
#                 st.session_state.text_input = st.session_state.sample_text
#                 st.rerun()
                
# if __name__ == "__main__":
#     main()
