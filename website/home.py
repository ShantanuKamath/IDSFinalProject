from IPython.core.display import publish_display_data
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import ipywidgets as widgets
import IPython.display
from IPython.display import display, clear_output
from datetime import date, datetime
from PIL import Image


def home():
    st.header("Covid 19: The New Normal")

    st.text("")

    st.subheader("Introduction")

    st.markdown("""2020-2021 has been a difficult period. We came across and battled a deadly pandemic - COVID-19. This pandemic led to a dramatic loss of human life worldwide, millions of individuals lost of their jobs, industries shut down, and lockdowns, quarantines, masks and WFH became the new norm.""")

    col1, col2, col3 = st.columns([10,10,10])    
    image1 = Image.open('website/artifacts/home_covid3.jpeg')
    image2 = Image.open('website/artifacts/home_covid2.jpeg')
    image3 = Image.open('website/artifacts/home_covid4.jpeg')

    with col1:
        st.image(image1)
    with col2:
        st.image(image2)
    with col3:
        st.image(image3)

    st.text("")

    st.markdown("""However, not all hope was lost! With the introduction of the various vaccines- Pfizer, J&J etc, the number of covid cases started getting curbed, lockdowns started getting lifted and a certain sense of normalcy returned to life.""")

    col1, col2, col3 = st.columns([10,10,10])     
    image1 = Image.open('website/artifacts/home_vaccine1.jpeg')
    image2 = Image.open('website/artifacts/home_vaccine2.png')
    image3 = Image.open('website/artifacts/home_vaccine3.jpeg')

    with col1:
        st.image(image1)
    with col2:
        st.image(image2)
    with col3:
        st.image(image3)

    st.text("")

    st.markdown("""In this project, we turn to the stock market to study the socio-economic effects of the deadly covid-19 pandemic, as well as the impact of the vaccine distribution.""")

    col1, col2, col3 = st.columns([10,10,10])     
    image1 = Image.open('website/artifacts/home_stocks1.jpeg')

    with col1:
        st.write("")
    with col2:
        st.image(image1)
    with col3:
        st.write("")

    st.markdown("""More specifically, we want to understand:   
- If all industries were impacted equally by covid? 
- Which were the industries that were impacted the most?
- Were there industries which boomed during this period?
- Were any of the industries able to recover their losses post the vaccine distribution?""")
    st.markdown("""In this study, we look to find the answers to the above questions, and study the impact covid had across various industries like Transportation, Hospitality, e-Commerce, Online Services, Airlines, etc.""")

    st.text("")
    st.text("")


    st.subheader("Project Overview")
    st.markdown("""Our project covers the following sections: 
- Dataset:
A brief description of the datasets used in our study, as well as any pre-processing carried out on them. 
Our project makes use of 3 datasets- Covid cases data, Covid vaccination data, Stocks data, to understand the progression of covid in the US, the impact that the vaccines had on this, as well as the impact both covid and vaccines had on the stock market.
    
- Visualisations:
In this section, we analyze the data further to understand the trends and correlations existing in the dataset and thus connecting it to our story. We also provide a few interactive visualizations to serve the purpose. 
    
- Game:
This is where we give you a chance to become the Wolf of Wall Street! Given $100 dollars and an idea of the stock market trend, can you figure out the best time to buy and sell your stocks so as to maximise your profits?""")

    st.text("")
    st.text("")

    st.subheader("Code")
    st.markdown("""Our project is hosted on Streamlit and the code for this can be found in the [following Github repository](https://github.com/ShantanuKamath/IDSFinalProject)""")

    st.text("")
    st.text("")

    st.subheader("Video")
    st.markdown("""The video presentation for our project can be found [here](https://youtu.be/Ro7mddMkD8w)""")

    st.text("")
    st.text("")

    st.subheader("Team")
    st.markdown("""This project was completed by Group 9:    
- Kunal Dhawan
- Kushagra Mahajan
- Shantanu Kamath
- Shubham Phal
- Nidhi Dhar""")


if __name__ == "__main__":
    home()