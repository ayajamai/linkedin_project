import streamlit as st
import pandas as pd
from pages import second

def app():

    st.title('What is your personality ?')
    st.header('Let us guess your personality in a few words blabla')

    st.subheader('The concept :')

    st.text("""Our project aims to evaluate your personality type within a few words
    of yours thanks to machine learning""")

    st.image('./mbti_types_pic.png')
    st.caption(' MBTI personality types') #plus à gauche


    df = pd.DataFrame({
    'Personality type': ['INTJ', 'INTP', 'ENTJ', 'ENTP', 'INFJ', 'INFP', 'ENFJ', 'ENFP', 'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ', 'ISTP','ISFP', 'ESTP', 'ESFP'],
    'Percentage': [2.1, 3.3, 1.8, 3.2, 1.5, 4.4, 2.5, 8.1, 11.6, 13.8, 8.7, 12, 5.4, 8.8, 4.3, 8.5]
    })

    df

    option = st.selectbox(
        'Take a guess about your personality type before the test :',
        df['Personality type'])
