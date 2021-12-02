import streamlit as st
import pandas as pd

def app():
    st.title('Who are you ?')
    st.text('Please take your time and give us a few words about yourself and what you like')

    with st.form(key='my_form'):
            first_input = st.text_input(label='I am...')
            submit_button = st.form_submit_button(label='Submit')
