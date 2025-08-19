import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # 年齢入力
    max_age = st.number_input("あなたの年齢を入力してください", min_value=0, max_value=120, value=30)

    # ライフログの入力
    life_log = {}
    age = 0
    sum = 0
    cnt = 0
    for age in range(0, max_age+1, 3):
        score = int(st.number_input(f"{age}歳の時のあなたの幸福度を0-100で入力してください"))
        life_log[age] = score
        sum += score
        cnt += 1
    if age < max_age:
        score = int(st.number_input('現在のあなたの幸福度を0-100で入力してください'))
        life_log[max_age] = score
        sum += score
        cnt += 1

    # データフレーム作成
    df = pd.DataFrame.from_dict(life_log, orient='index', columns=['幸福度'])

    # グラフの種類選択
    chart_type = st.selectbox("グラフの種類を選択", ["折れ線グラフ", "棒グラフ", "散布図"])

    # グラフの描画
    graph_button = st.button("グラフを表示")
    if graph_button:
        fig, ax = plt.subplots(figsize=(10, 6))
        if chart_type == "折れ線グラフ":
            ax.plot(df.index, df['幸福度'])
        elif chart_type == "棒グラフ":
            ax.bar(df.index, df['幸福度'])
        else:
            ax.scatter(df.index, df['幸福度'])
        ax.set_xlabel('Age')
        ax.set_ylabel('Happiness')
        ax.set_title('Graph of Your Life')
        ax.grid(True)
        ax.set_ylim(bottom=0)
        st.title('あなたの人生をグラフで表しました')
        st.pyplot(fig)
        
        #フィードバック
        st.title('フィードバック')
        avg = int(sum/cnt)
        if avg >= 67:
            st.text('あなたの人生は・・・全体的に幸福度が高いです！！')
            st.image('app_242119/幸福度が高い人.webp')
            st.text('これからも幸福でいましょう')
        elif avg >= 34:
            st.text('あなたの人生は・・・全体的に幸福度は普通です')
            st.image('app_242119/幸福度が普通の人.webp')
            st.text('楽しいことを見つけて、人生を楽しもう！')
        else:
            st.text('あなたの人生は・・・全体的に幸福度が低いです...')
            st.image('app_242119/幸福度が低い人.webp')
            st.text('''
            あなたが今、どんな状況にあっても、それが永遠に続くわけではないことを忘れないでください。
            人生には波があり、どんなに辛い時期でも必ず変化は訪れます。
            今はその変化の途中にいるだけかもしれません。
            小さな一歩を踏み出すことで、少しずつでも心が軽くなる瞬間がきっとあります。
            周りの人に支えを求めることも、自己を大切にすることも大切な一歩です。
            あなたの気持ちに寄り添いながら、少しずつ前に進んでいけることを願っています。
            '''.strip())
    

st.title('あなたの人生を振り返ろう')
main()