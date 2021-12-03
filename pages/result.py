import streamlit as st
import pandas as pd
import requests
from pages import second
from pages import third
from pages import fourth


#blabla
#import the input variables

def concat_text(first_input, second_input, third_input) :
    sub_text = str(first_input) + str(second_input) + str(third_input)
    return sub_text

# sub = concat_text(first_input, second_input, third_input)

def app():

    st.title('TADA We guessed')
    # enter here the address of your flask api
    url = 'https://mbtipredictor-cqagwrgcaq-uc.a.run.app/predict?answers='

    # # The idea is to concatenate the 3 inputs and give them to be predicted
    # concatenate to a huge string and a dataframe
    # params = dict()
    sub = concat_text(second.app, third.app, fourth.app)

    print(second.app)
    print(third.app)

    # response = requests.get(url, sub)

    # prediction = response.json()

    # pred = prediction['prediction']

    return sub
