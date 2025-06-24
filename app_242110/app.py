import streamlit as st
import random
import csv

def main():
  """
  ガチャシミュレーターのメイン関数
  """

  # ガチャの結果を保存するリスト (セッション状態を使用)
  if 'history' not in st.session_state:
        st.session_state.history = []

  def gacha():
    """
    ガチャを引く関数
    """
    random_int = random.randint(1, 1000)
    #random_int = 1
    
    
    # レアリティ判定
    if random_int == 1:
        random_int2 = random.randint(1, 100)
        #random_int2 = 1
        if(random_int2 == 1):
            result = "LR(甜瓜黒黒)"
            st.markdown("<p style='color: red;'>LR</p>", unsafe_allow_html=True)
            st.write("甜瓜黒黒")
            st.image("app_242110/kurokuro.png",width=50)  
        elif(random_int2 < 12):
            result = "UR(銀太郎)"
            st.markdown("<p style='color: magenta;'>UR</p>", unsafe_allow_html=True)
            st.write("銀太郎")
            st.image("app_242110/gintaro.png",width=50)    
        else:
            result = "SSR(虎の守護霊太郎)"
            st.markdown("<p style='color: purple;'>SSR</p>", unsafe_allow_html=True)
            st.write("虎の守護霊太郎")
            st.image("app_242110/tora.png",width=50)
    elif random_int < 12:
        result = "SR(亀島太郎)"
        st.markdown("<p style='color: gold;'>SR</p>", unsafe_allow_html=True)
        st.write("亀島太郎")
        st.image("app_242110/kameshima.png" , width=50)
    elif random_int < 112:
        result = "R(蟹蟹太)"
        st.markdown("<p style='color: silver;'>R</p>", unsafe_allow_html=True)
        st.write("蟹蟹太")
        st.image("app_242110/kani.png" , width=50)
    else:
        result = "N"
        # Nの処理 (複数のNがある場合は、ここでさらに条件分岐)
        random_int2 = random.randint(1, 3)
        st.markdown("<p style='color: blue;'>N</p>", unsafe_allow_html=True)
        if random_int2 == 1:
            result += " (蟻星人)"
            st.write("蟻星人")
            st.image("app_242110/ari.png" , width=50)
        elif random_int2 == 2:
            result += " (フェイクブック)"
            st.write("フェイクブック")
            st.image("app_242110/book.png" , width=50)
        else:
            result += " (スライム人)"
            st.write("スライム人")
            st.image("app_242110/suraimu.png" , width=50)
            

    # 結果を履歴に追加
    st.session_state.history.append(result)
    return result
  def gacha_10x():
        results = []
        for _ in range(10):
            result = gacha()
            results.append(result)
        return results
    
  def gacha_100x():
        results = []
        for _ in range(100):
            result = gacha()
            results.append(result)
        return results

  def show_history():
        st.write("ガチャ履歴")
        for result in st.session_state.history:
            st.write(result)
  def save_history():
        with open('gacha_history.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(st.session_state.history)

  # ストリームリットのタイトルを設定
  st.title('ガチャシミュレーター')

  # ガチャを引くボタン
  if st.button("ガチャを引く", key="gacha_button"):  # key="gacha_button" を追加
    result = gacha()
    #st.write(result)
    # 画像を表示したり、処理を行う
  # ガチャを引くボタン
  if st.button("10連ガチャを引く", key="gacha_10x_button"):
    results = gacha_10x()
        #for result in results:
            #st.write(result)
            
  if st.button("100連ガチャを引く", key="gacha_100x_button"):
    results = gacha_100x()

  # 履歴を表示するボタン
  if st.button("履歴を見る", key="history_button"):
    show_history()

# main関数を実行
if __name__ == "__main__":
  main()