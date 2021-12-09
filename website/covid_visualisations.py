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

def covid_visualisations():

    hy.header("Progression of Covid in the US")

    hy.markdown("""Before we begin studying the effect that covid had on the stock market, we perform a preliminary analysis to understand the progression of covid cases in the US right from when the initial cases started getting reported in early January, 2020 till date.""")
    hy.markdown("Having an understanding of the severity of the covid cases in the US, helps us reason about any changes in the stock market that we may observe.")


    country_df = pd.read_csv('../Data/usa_national_level_daily_new_covid_cases.csv')
    state_df = pd.read_csv('../Data/usa_state_level_daily_new_covid_cases.csv')

    hy.subheader("How severe was the pandemic anyway?")
    hy.markdown("""In order to see how badly the United States was affected by covid, we plotted a progression of covid cases with time arcoss the US""")
    fig = px.line(country_df, x="Date", y="Daily New Cases", title="Covid cases reported across the US")
    hy.write(fig)
    hy.markdown("""From this graph we were able to clearly visualise that there were 2 waves of covid that had hit the US. 
    
- The first wave starts its upward trend around 12th October, 2020. It is in its peak from 20th November 2020 to 22nd January 2021, and subsides by 18th February, 2021.
- The second wave starts its upward trend around 20th July, 2021. It is in its peak from 18th August 2021 to 16th September 2021, and subsides by 18th October, 2021.

We identify these as our time durations of interest and use them subsequently to understand how the stock market performed during these two peaks""")

    hy.subheader("Which were the most notorious states when it comes to covid?")
    hy.markdown("""Once we had seen a high level view of the covid trend in the US, we wanted to how covid affected each state. We wanted to identify which states were the worst affected by covid, and which states were the least affected.
For this we plotted a bar chart to visualise the total covid cases per state.""")
    state_cumulative = state_df.groupby(['State']).agg({'Daily New Cases':'sum'}).reset_index()
    state_cumulative = state_cumulative.rename(columns={"Daily New Cases": "Total Cases"})
    state_cumulative.sort_values('Total Cases', axis=0, ascending=True, inplace=True)
    fig = px.bar(state_cumulative, x='State', y='Total Cases')
    hy.write(fig)
    hy.markdown("""From this barchart we were able to see that the state with the most number of covid cases was California, with 4.83 million cases. And the state with the least number of covid cases was Vermont with 43K cases.""")

    hy.subheader("Did all states peak at the same time?")
    hy.markdown("""Once we had a high level view of how each US state was affected by Covid, we decided to dig a little deeper and scrutanise the covid trends at a state level.
    We created an interactive plot which would help us compare the covid trends between 2 states. We use this as a means to analyse how the trends compare from one state to another, and if the states peaked at the same time or not""")
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
    hy.markdown("""From this visualisation we were able to see that the covid trends were pretty uniform across the different states. While their timelines were
    almost the same, some states were affected more than others. """)

if __name__ == "__main__":
    covid_visualisations()