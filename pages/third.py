import streamlit as st
import pandas as pd

#blabla

def app():
    st.title('What are your thoughts about this tweet ?')
    st.image('./most_com.png')
    st.caption(' Most commented tweet of 2020') #plus à gauche
    with st.form(key='my_form'):
            first_input = st.text_input(label='Comment')
            submit_button = st.form_submit_button(label='Publish')
