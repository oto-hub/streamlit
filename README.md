# Streamlitアプリ研究所

富山県の某専門学校学生が作成したWebアプリ集

## 更新: 自然言語処理アプリ (app_999940)

### 既存機能
- テキスト入力による品詞抽出
- CSVファイルによる品詞抽出
- CSVファイルによる出現回数グラフ
- CSVファイルによる列選択とグラフ

### 新機能: 依存関係解析
- 日本語・英語テキストの依存関係解析
- 視覚的な依存関係グラフの表示
- トークン詳細情報の表示
- 固有表現の抽出
- 文の分割表示

### Streamlit Cloudでの使用方法

1. **モデルのダウンロード**
   ```bash
   python -m spacy download ja_ginza
   python -m spacy download en_core_web_sm
   ```

2. **アプリの実行**
   - サイドバーから「999940」を選択
   - 機能選択で「依存関係解析」を選択
   - テキストを入力して「解析実行」をクリック

### 技術仕様
- spaCy 3.x
- displacy for visualization
- Streamlit components for HTML rendering
- 日本語: ja_ginzaモデル
- 英語: en_core_web_smモデル