#!/usr/bin/env python3
"""
Streamlit Cloud用のspaCyモデルセットアップスクリプト
"""

import subprocess
import sys
import os

def download_spacy_models():
    """必要なspaCyモデルをダウンロード"""
    models = [
        "ja_ginza",
        "en_core_web_sm"
    ]
    
    for model in models:
        try:
            print(f"ダウンロード中: {model}")
            subprocess.check_call([
                sys.executable, "-m", "spacy", "download", model
            ])
            print(f"✅ {model} のダウンロードが完了しました")
        except subprocess.CalledProcessError as e:
            print(f"❌ {model} のダウンロードに失敗しました: {e}")
        except Exception as e:
            print(f"❌ 予期しないエラー: {e}")

if __name__ == "__main__":
    print("🚀 spaCyモデルのダウンロードを開始します...")
    download_spacy_models()
    print("�� セットアップが完了しました！") 