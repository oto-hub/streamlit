import streamlit as st
import importlib
import os

st.set_page_config(
    page_title='streamlitアプリ研究所', 
    page_icon='Bitちゃん02.png',
    initial_sidebar_state='expanded'
)
st.title('🎓 某専門学校講師のstreamlitアプリ研究所')
st.image('Gemini_Generated_Image_qwrzjkqwrzjkqwrz.jpg', use_container_width=True)
st.markdown('---')
st.subheader('📱 サイドバーからアプリを選んでください')
st.write('富山県の某専門学校学生が作成したWebアプリ集')
st.markdown('---')

def main():
    
    # アプリリストを整理
    student_apps = ['', '242101', '242102', '242103', '242104', '242105', '242106', '242107', 
                   '242109', '242110', '242111', '242112', '242113', '242114', '242115', 
                   '242116', '242117', '242119', '242120', '242121', '242123', '242124', 
                   '242125', '242126', '242127', '999900', '999910', '999920', '999930', '999940', '999950']
    
    page = st.sidebar.selectbox(
        '🚀 Webアプリ番号一覧',
        student_apps
    )

    if page:
        st.markdown(f"### 🎯 アプリ {page} を実行中...")
        folder_name = f'app_{page}'
        module_name = folder_name + '.app'

        try:
            # モジュールをインポートしてmain関数を実行
            app_module = importlib.import_module(module_name)
            app_module.main()
        except ModuleNotFoundError:
            st.error(f"❌ モジュール '{module_name}' が見つかりませんでした。")
        except AttributeError:
            st.error(f"❌ モジュール '{module_name}' に 'main()' 関数がありません。")
        except Exception as e:
            st.error(f"❌ 予期しないエラーが発生しました: {e}")
            
if __name__ == '__main__':
    main()
