import streamlit as st

def main():
    st.title("電卓")

    
    st.write("### 数値を入力:")
    num1 = st.number_input("数値1", value=0, step=1)
    num2 = st.number_input("数値2", value=0, step=1)

    
    st.write("### 演算子を選択:")
    operation = st.selectbox("演算子", ["+", "-", "*", "/"])

    
    if st.button("Enter"):
        try:
            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                if num2 == 0:
                    st.error("0で割ることはできません☺")
                    return
                result = num1 / num2

            st.success(f"結果: {result}")
        except Exception as e:
            st.error(f"error: {e}")

if __name__ == "__main__":
    main()
