import streamlit as st
import pandas as pd
import numpy as np

from multipage import MultiPage
from pages import first, second, third, fourth, result # import your pages here

# Create an instance of the app
app = MultiPage()

# Title of the main page
st.title("Magic personality guess")

# Add all your applications (pages) here
app.add_page("Presentation", first.app)
app.add_page("First step", second.app)
app.add_page("Second step", third.app)
app.add_page("Third step",fourth.app)
app.add_page("Result",result.app)

# The main app
app.run()

print(app)
# if True == True :
#     first.app()
# else :
#     st.text_input("Your name", key="name")



#st.text_input("Your name", key="name")

# You can access the value at any point with:
# st.session_state.name

# df = pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
#     })

# option = st.selectbox(
#     'Which number do you like best?',
#      df['first column'])

# 'You selected: ', option

# # Add a selectbox to the sidebar:
# add_selectbox = st.sidebar.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone')
# )

# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )



# left_column, right_column = st.columns(2)
# # You can use a column just like st.sidebar:
# left_column.button('Press me!')

# # Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")

# st.title('What is your personality ?')

# st.write("""
# # Let us guess your personality in a few keyboard types
# """)

# st.header('My header')


# pickup_date = st.date_input('pickup datetime', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
# pickup_time = st.time_input('pickup datetime', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
# pickup_datetime = f'{pickup_date} {pickup_time}'
# pickup_longitude = st.number_input('pickup longitude', value=40.7614327)
# pickup_latitude = st.number_input('pickup latitude', value=-73.9798156)
# dropoff_longitude = st.number_input('dropoff longitude', value=40.6413111)
# dropoff_latitude = st.number_input('dropoff latitude', value=-73.7803331)
# passenger_count = st.number_input('passenger_count', min_value=1, max_value=8, step=1, value=1)

# enter here the address of your flask api
# url = 'https://taxifare.lewagon.ai/predict'

# params = dict(
#     pickup_datetime=pickup_datetime,
#     pickup_longitude=pickup_longitude,
#     pickup_latitude=pickup_latitude,
#     dropoff_longitude=dropoff_longitude,
#     dropoff_latitude=dropoff_latitude,
#     passenger_count=passenger_count)

# response = requests.get(url, params=params)

# prediction = response.json()

# pred = prediction['prediction']

# pred
