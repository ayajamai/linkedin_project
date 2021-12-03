import streamlit as st
import pandas as pd
import requests
from pages import first


#blabla
def app():
    df = pd.DataFrame({
    'Personality type': ['INTJ', 'INTP', 'ENTJ', 'ENTP', 'INFJ', 'INFP', 'ENFJ', 'ENFP', 'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ', 'ISTP','ISFP', 'ESTP', 'ESFP'],
    'Percentage': [2.1, 3.3, 1.8, 3.2, 1.5, 4.4, 2.5, 8.1, 11.6, 13.8, 8.7, 12, 5.4, 8.8, 4.3, 8.5]
    })

    option = st.selectbox(
        'Take a guess about your personality type before the test :',
    df['Personality type'])

    st.title('Who are you ?')
    st.text('Please take your time and give us a few words about yourself and what you like')

    with st.form(key='my_form'):
            first_input = st.text_input(label='I am...')
            submit_button = st.form_submit_button(label='Submit')
            print(first_input)

    st.title('What are your thoughts about this tweet ?')
    st.image('./most_com.png')
    st.caption(' Most commented tweet of 2020') #plus à gauche
    with st.form(key='my_form_2'):
            second_input = st.text_input(label='Comment')
            submit_button = st.form_submit_button(label='Publish')

    st.title('What are your thoughts about this post?')

    with st.form(key='my_form_3'):
        third_input = st.text_input(label='I am...')
        submit_button = st.form_submit_button(label='Submit')

    print(first_input)
    print(second_input)
    print(third_input)

    if len(first_input) >5 and len(second_input)>5 and len(third_input)>5 :
        url = f'https://mbtipredictor-cqagwrgcaq-uc.a.run.app/predict?answers={first_input + second_input + third_input}'
        response = requests.get(url)
        output = response.json()['prediction']
        st.write(f'you guessed {option} and you got {output}')

    return 'nothing'
