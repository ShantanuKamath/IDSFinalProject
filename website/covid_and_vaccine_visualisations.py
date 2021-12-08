import hydralit as hy
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import ipywidgets as widgets
import IPython.display
from IPython.display import display, clear_output
from datetime import date, datetime


def covid_and_vaccine_visualisations():

    hy.header("Covid Cases Data")

    country_df = pd.read_csv('website/../Data/usa_national_level_daily_new_covid_cases.csv')
    state_df = pd.read_csv('website/../Data/usa_state_level_daily_new_covid_cases.csv')

    hy.subheader("Progression of covid cases with time across the US")
    fig = px.line(country_df, x="Date", y="Daily New Cases", title="Covid cases reported across the US")
    hy.write(fig)

    hy.subheader("Statewise analysis of covid cases")
    state_cumulative = state_df.groupby(['State']).agg({'Daily New Cases':'sum'}).reset_index()
    state_cumulative = state_cumulative.rename(columns={"Daily New Cases": "Total Cases"})
    state_cumulative.sort_values('Total Cases', axis=0, ascending=True, inplace=True)
    fig = px.bar(state_cumulative, x='State', y='Total Cases')
    hy.write(fig)

    hy.subheader("Two State Comparison")
    states = np.unique(state_df['State'].values)
    dropdown_state = hy.selectbox('Enter a primary state',states, index=0)
    dropdown_comp_state = hy.selectbox('Enter a secondary state for comparison',states, index=1)


    sorted_df = state_df.copy()

    if(dropdown_comp_state is None):
        sorted_df["order"] = sorted_df["State"].map({dropdown_state: 1}).fillna(2)
    else:
        sorted_df["order"] = sorted_df["State"].map({dropdown_state: 1, dropdown_comp_state: 2}).fillna(3)
    sorted_df.sort_values(by=["order", "Date"], ascending=False, inplace=True)

    fig = px.line(sorted_df, 
            x="Date", 
            y="Daily New Cases", 
            color="State", 
            labels={
                "Date": "Reported Date",
                "Daily New Cases": "Number of new covid cases recorded"
            }, 
            width=800, height=600,
            title="Number of covid cases recorded Across Various Regions in the US")

    fig.update_traces({"line":{"color":"lightgrey", "width":2}})

    fig.update_traces(patch={"line":{"color":"blue", "width":3}}, 
                    selector={"legendgroup":dropdown_state})

    if(dropdown_comp_state is not None):
        fig.update_traces(patch={"line":{"color":"red", "width":3}}, 
                        selector={"legendgroup":dropdown_comp_state})

    fig.update_layout(title_text='Number of covid cases recorded Across Various Regions in the US', title_x=0.5,
                    showlegend=True,
                    yaxis_range=[0,61017],
                    yaxis={"visible":True})

    hy.write(fig)


    #########################################################################################

    hy.header("Covid Vaccination Data")

    hy.subheader("Analysis of vaccine distribution across the US")
    df1 = pd.read_csv('website/../Data/covid19_vaccination_data_US_full.csv')

    df1 = df1[df1.Location != "US"]
    province_list = np.unique(df1['Location'].values)

    prov = hy.selectbox('Enter a primary state',province_list, index=0)
    comp_prov = hy.selectbox('Enter a secondary state for comparison',province_list, index=1)


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

    hy.write(fig)

    hy.subheader("Analysis of Vaccine Distribution and Administration Across States")
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
    hy.write(fig)

if __name__ == "__main__":
    covid_and_vaccine_visualisations()