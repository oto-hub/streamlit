import streamlit as st

def main():
    # ここから記述
    def base_conversion(number, base_from, base_to):

    # 10進数に変換
        num = int(number, base_from)

        # 10進数から指定の進数に変換
        ret = ''
        moji=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        while num > 0:
            ret=moji[int(num%base_to)]+ret
            num=num//base_to

        return ret

    st.title("進数変換ツール")

    # 入力フォーム
    number_input = st.text_input("変換したい数値を入力してください")
    base_from_input = st.number_input("変換元の進数を入力してください (2～36)", min_value=2, max_value=36, step=1)
    base_to_input = st.number_input("変換先の進数を入力してください (2～36)", min_value=2, max_value=36, step=1)

    # 変換ボタン
    if st.button("変換"):
        try:
            result = base_conversion(number_input, base_from_input, base_to_input)
            st.success(f"変換結果は: {result}")
        except ValueError:
            st.error("入力値が不正です。数値と進数を正しく入力してください。")
            st.image('Gemini_Generated_Image_yjrnt5yjrnt5yjrn.jpg')


main()