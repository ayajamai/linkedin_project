import streamlit as st
import pandas as pd
import numpy as np

from multipage import MultiPage
from pages import first, second, third, fourth, result # import your pages here

#blabla
# Create an instance of the app
app = MultiPage()

# Title of the main page
st.title("Magic personality guess")

# Add all your applications (pages) here
app.add_page("Presentation", first.app)
app.add_page("First step", second.app)
# app.add_page("Second step", third.app)
# app.add_page("Third step",fourth.app)
# app.add_page("Result",result.app)

# The main app
app.run()

print(app)
