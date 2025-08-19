import streamlit as st
import pandas as pd
import numpy as np

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def calculate_average_temperature(data):
    return np.mean(data['temperature'])

def main():
    st.title("人の体温検知アプリ")
    st.title('体温のヒストグラム')
    # st.xlabel('体温 (℃)')
    # st.ylabel('頻度')
    # st.pyplot('plt')
    uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")
    
    if uploaded_file is not None:

        data = load_data(uploaded_file)
        
        average_temp = calculate_average_temperature(data)
        
        st.write("平均体温:", average_temp)
        
        if average_temp > 37.5:
            st.warning("警告: 平均体温が正常範囲を超えています！")
        else:
            st.success("体温は正常範囲内です。")
        
        if average_temp > 30.5:
            st.warning("警告: 平均体温が正常範囲を低すぎます!")
        else:
             st.success("体温は正常範囲内です。")
        st.image("app_242120/2sCcPz3GMblCFoVayuIPwgVFjkU-0x0.png", caption="体温検知アプリのイメージ", use_column_width=True)

if __name__ == "__main__":
    main()