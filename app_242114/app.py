import streamlit as st
import random
import os
import pandas as pd

def main():
    # ここから記述
    # サイドバーにタブを作成
    st.sidebar.title("アプリメニュー")
    app_mode=st.sidebar.radio("選択してください:", ["乱数生成", "シャッフル"])
    if app_mode=='乱数生成':
        #タイトルを表示
        st.title("乱数メーカー")
        # 入力欄: 範囲の下限
        minVal=st.number_input("乱数の下限値を入力してください:", value=1)

        # 入力欄: 範囲の上限
        maxVal=st.number_input("乱数の上限値を入力してください:", value=10)

        # 入力欄: 生成する乱数の個数
        count=st.number_input("生成する乱数の個数を入力してください:", value=5, min_value=1, step=1)
        # 同じ数を除外
        unique=st.checkbox("同じ数を除外する")
        # ボタンが押されたときの動作
        if st.button("乱数を生成"):
            # 入力チェック: 下限値が上限値より大きい場合は数値を入れ替える
            if minVal >= maxVal:
                tmp=minVal
                minVal=maxVal
                maxVal=tmp
                st.write('下限値は上限値より小さい必要があります。数値が自動的に調整されました。')
            # 乱数を生成
            if unique:
                # 重複を除外する　かつ　生成個数が生成限界を超えていた場合　生成個数を調整する
                if count>(maxVal-minVal+1):
                    count=maxVal-minVal+1
                    st.write("生成個数が範囲内の値の数を超えています。個数が自動的に調整されました。")
                st.write(f'{minVal}から{maxVal}まで{count}個生成')
                randNums=random.sample(range(int(minVal), int(maxVal) + 1), int(count))
            else:
                st.write(f'{minVal}から{maxVal}まで{count}個生成')
                randNums=[random.randint(int(minVal), int(maxVal)) for _ in range(int(count))]
            st.write("生成された乱数:")
            for num in randNums:
                st.text(num)
    elif app_mode == "シャッフル":
        st.title("シャッフル")
        # 入力欄: シャッフル対象のリスト
        items=st.text_area("シャッフルする項目を1行ずつ入力してください:")
        # ファイルアップロード
        uploaded_file = st.file_uploader("CSVファイルをドラッグアンドドロップまたは選択してください", type="csv")
        # チェックボックス
        textIn=st.checkbox("入力データを優先して使用する")
        # 注意書き
        st.write('※csvファイルの1列目のみをシャッフルします')
        st.write('※csvファイルの1行目はリストに反映されません')
        # ボタンが押されたときの動作
        if st.button("シャッフル"):
            runed=False
            if items:
                if textIn or uploaded_file==None:
                    # リストを作成してシャッフル
                    item_list = items.splitlines()
                    item_list = [item.strip() for item in item_list]  # 空白を削除
                    random.shuffle(item_list)
                    # シャッフル後のリストを表示
                    st.write("シャッフルされたリスト:")
                    for i in range(len(item_list)):
                        st.write(f'{i+1}　　{item_list[i]}')
                    runed=True
            if runed==False:
                if uploaded_file is not None:
                    try:
                        # CSVファイルの読み込み
                        df = pd.read_csv(uploaded_file)
                        shaffle(df)
                    except Exception as e:
                        st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
                else:
                    try:
                        # Itemsフォルダ内のCSVファイルを読み込む
                        items_dir = "Items"
                        csv_files = [f for f in os.listdir(items_dir) if f.endswith('.csv')]
                        if not csv_files:
                            st.error("`Items` フォルダにCSVファイルが見つかりません。")
                        else:
                            # 最初のCSVファイルを読み込む
                            csv_file = csv_files[0]
                            file_path = os.path.join(items_dir, csv_file)
                            # CSVをpandasで読み込む
                            df = pd.read_csv(file_path)
                            shaffle(df,csv_file)
                    except FileNotFoundError:
                        st.error(f"`Items` フォルダが存在しないか、アクセスできません。")
                    except pd.errors.EmptyDataError:
                        st.error(f"指定されたCSVファイルは空です: {file_path}")
                    except Exception as e:
                        st.error(f"エラーが発生しました: {e}")
                    

def shaffle(df,csv_file=''):
    try:
        if not df.empty:
            # データの1列目をリストに変換
            item_list = df.iloc[:, 0].dropna().tolist()
            # シャッフル
            random.shuffle(item_list)
            # シャッフル後のリストを表示
            if csv_file=='':
                st.write(f"アップロードされたファイルからシャッフルされたリスト:")
            else:
                st.write(f"CSVファイル「{csv_file}」からシャッフルされたリスト:")
            for i in range(len(item_list)):
                    st.write(f'{i+1}　　{item_list[i]}')
        else:
            st.error("CSVファイルが空です。内容を確認してください。")
    except Exception as e:
        st.error(f"シャッフル中にエラーが発生しました: {e}")



main()