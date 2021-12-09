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

@st.cache
def read_data():
    df1 = pd.read_csv('website/../Data/covid19_vaccination_data_US_full.csv')
    df1 = df1[df1.Location != "US"]
    return df1

@st.cache
def draw_choropleth():
    vaccination_data = pd.read_csv('website/../Data/covid19_vaccination_data_US_full.csv')
    vaccination_data_grouped = vaccination_data.groupby(['Date','Location'],as_index=False).agg({"Admin_Per_100K":"sum","Distributed":"sum","Dist_Per_100K":"sum"})

    data_slider = []
    dates_range = []
    for date in sorted(vaccination_data_grouped['Date'].unique(),key=lambda date: datetime.strptime(date, "%m/%d/%Y")):
        df_split =  vaccination_data_grouped[(vaccination_data_grouped['Date']== date)]
        data_each_date = dict(type='choropleth',locations = df_split['Location'],
                            z=df_split['Admin_Per_100K'],
                            locationmode='USA-states',
                            colorbar= {'title':'Doses Administered per 100K'})
        data_slider.append(data_each_date)
        dates_range.append(date)
            
    steps = []
    for i in range(len(data_slider)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data_slider)],
                    label='Date {}'.format(dates_range[i]))
        step['args'][1][i] = True
        steps.append(step)

    sliders = [dict(active=0, pad={"t": 1}, steps=steps)]
    layout = dict(title ='Vaccination Administration Progress', geo=dict(scope='usa',projection={'type': 'albers usa'}),
                sliders=sliders)
    fig =  go.Figure(data=data_slider, layout=layout)
    return fig

def vaccine_visualisations():
    st.header("Vaccination Distribution")

    cols = st.columns(3)
    cols[1].markdown("![Alt Text](https://media.giphy.com/media/n0KNIKsmIGcXoV3YTw/giphy.gif)")

    st.markdown("""Once we had taken a look at the prgression of covid cases in the US, we decided to analyse the vaccine distribution trends in the US. We wanted to see if the administration of vaccines
    helped reduce the number of covid cases, and subsequently improve the sentiment amongst the people and have a positive impact on the stock market.
    In order to do this we compared between the vaccine administration per 100K population between two states""")

    st.text("")
    st.subheader("Analysis of vaccine distribution across the US")
    df1 = read_data()

    province_list = np.unique(df1['Location'].values)

    prov = st.selectbox('Enter a primary state',province_list, index=0)
    comp_prov = st.selectbox('Enter a secondary state for comparison',province_list, index=1)


    sorted_df = df1.copy()
    sorted_df["Date"] = pd.to_datetime(sorted_df["Date"])
    if(comp_prov is None):
        sorted_df["order"] = sorted_df["Location"].map({prov: 1}).fillna(2)
    else:
        sorted_df["order"] = sorted_df["Location"].map({prov: 1, comp_prov: 2}).fillna(3)
    sorted_df.sort_values(by=["order", "Date"], ascending=False, inplace=True)

    fig = px.line(sorted_df, 
            x="Date", 
            y="Admin_Per_100K", 
            color="Location", 
            labels={
                "Date": "Date Administered",
                "Admin_Per_100K": "Vaccine Doses Administered",
            }, 
            width=800, height=700,
            title="Admininstration of Covid Vaccines per 100K Population Across Various Regions in the US")

    fig.update_traces({"line":{"color":"lightgrey", "width":2}})

    fig.update_traces(patch={"line":{"color":"blue", "width":3}}, 
                    selector={"legendgroup":prov})

    if(comp_prov is not None):
        fig.update_traces(patch={"line":{"color":"red", "width":3}}, 
                        selector={"legendgroup":comp_prov})

    fig.update_layout(title_text='Admininstration of Covid Vaccines per 100K Population Across Various Regions in the US', title_x=0.5,
                    showlegend=True,
                    yaxis_range=[0,200000],
                    yaxis={"visible":True})

    st.plotly_chart(fig, use_container_width=True)   
    st.markdown("""From this plot, we can clearly see that the Republic of Palau (RP) (which falls in the U.S. Pacific Islands) has the highest number of total vaccine doses administered per 100K population, followed by Vermont, and Puerto Rico. Marshall Islands (MH) and Federated States of Micronesia (FM) have the lowest numbers.""")
    st.text("")
    st.subheader("Analysis of Vaccine Administration Progress Across States")
    
    fig = draw_choropleth()
    
    st.plotly_chart(fig, use_container_width=True)   
    st.markdown("""From this visualisation we are able to see that the vaccine administration was far more rapid in states such as Texas and North Dakota initially. A historical analysis reveals that Texas was infact the first state to reach 1 million vaccinations. Over time we see the vaccination rate across other states such as California and New York picking up while the vaccination rate across states that demonstrated early gains deteriorates""")
    st.markdown("""
      <b><span style="font-size: 115%; color:#D71806">Interesting Articles:</span></b> <br>

      <div class="image123">
      <a href="https://www.texastribune.org/2021/01/14/texas-coronavirus-vaccine-one-million/">
        <div style="float:left;margin-right:50px;margin-left:20px">
            <img src="https://ggsc.s3.amazonaws.com/images/uploads/How_to_Be_Deliberate_About_Consuming_Coronavirus_News.jpg" width="70" height="70">
            <p style="text-align:center;">Texas Tribune</p>
        </div>
      </a>
      </div>

      """, unsafe_allow_html=True)

if __name__ == "__main__":
    vaccine_visualisations()
