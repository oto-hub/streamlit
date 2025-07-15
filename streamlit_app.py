import streamlit as st
import sys
import os

# app_999950のパスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'app_999950'))

# app_999950のapp.pyをインポートして実行
try:
    from app_999950.app import main
    main()
except ImportError as e:
    st.error(f"アプリの読み込みに失敗しました: {e}")
    st.write("app_999950フォルダ内のapp.pyを確認してください。")
except Exception as e:
    st.error(f"予期しないエラーが発生しました: {e}") 