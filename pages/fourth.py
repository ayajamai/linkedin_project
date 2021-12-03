import streamlit as st
import pandas as pd

def app():
    st.title('What are your thoughts about this post?')

    with st.form(key='my_form'):
        first_input = st.text_input(label='I am...')
        submit_button = st.form_submit_button(label='Submit')
    return first_input
