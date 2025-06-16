
import streamlit as st 
import random
st.title('  数字を引くだけ! sreamlit run app.py   ')
st.text('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
st.write('★サイドバーからコンテンツを選んでください★')
st.text('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
def main():
    page = st.sidebar.selectbox('pikup',['ひく','ひかない'])
    p = st.sidebar.selectbox('level',['0','1','2'])
    k = st.sidebar.selectbox('level',['0','1','2','3','4','5'])
    o = st.sidebar.selectbox('何連？',['0','10'])
    if o=='10':
        if page == 'ひく':
            st.title('数字')
    st.subheader('単発')
    ko =['★1','★2','★3']
    ji =['1','253','25253','25232','142414','14124']
    j2=['52551','14124','0619','12211','99716','1212111']
    j3=['1211','22233','987761','1  287 ','1129','2323233']
    st.write('★引く番号を選んでください★')
    ir=random.randint(0,3)
    ko=random.randint(0,5)
    
    if ir== 0:
         st.write('★1')
         st.write(ji[ko])
            
    if ir== 1:
        st.write('★2')
        st.write(j2[ko])
        i=i+1
           
    if ir== 2:
        st.write('★3')
        st.write(j3[ko])
        i=1+1
            
    if page=='引かない':
        st.write('甘えてんなよ？')
        i=i+1
    if o=='0':
        if page == 'ひく':
            st.title('漢字')
            st.subheader('単発')
            ko =['★1','★2','★3']
            ji =['鏡','焦','無','黑','諦','良']
            j2=['頑','自','小','見','荘','分']
            j3=['厳','歯','有','知','髪','云']
            st.write('★引く番号を選んでください★')
            ir=random.randint(0,3)
            ko=random.randint(0,5)
            if ir== 0:
                st.write('★1')
                st.write(ji[ko])
                i=i+1
                
            if ir== 1:
                st.write('★2')
                st.write(j2[ko])
                i=i+1
               
            if ir== 2:
                st.write('★3')
                st.write(j3[ko])
                i=1+1
                
            if page=='引かない':
                st.write('甘えてんなよ？')
                i=i+1
        
    
    
