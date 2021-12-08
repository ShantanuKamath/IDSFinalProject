import streamlit as st
from datetime import datetime 
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

company_to_ticker = {}
company_to_ticker['United Airlines'] = 'UAL'
company_to_ticker['Visa'] =  'V'
company_to_ticker['Lyft'] =  'LYFT'
company_to_ticker['Costco'] =  'COST'
company_to_ticker['Airbnb'] =  'ABNB'
company_to_ticker['Amazon'] =  'AMZN'
company_to_ticker['Coursera'] =  'COUR'
company_to_ticker['Uber'] =  'UBER'
company_to_ticker['American Express'] = 'AXP'
company_to_ticker['Marriot'] =  'MAR'
company_to_ticker['Twitter'] =  'TWTR'
company_to_ticker['Netflix'] =  'NFLX'
company_to_ticker['American Airlines'] = 'AAL'
company_to_ticker['Zoom'] =  'ZM'
company_to_ticker['Delta Airlines'] = 'DAL'
company_to_ticker['Mastercard'] =  'MA'
company_to_ticker['Hilton'] =  'HLT'
company_to_ticker['Walmart'] =  'WMT'
ticker_to_company = {}
ticker_to_company['UAL'] = 'United Airlines'
ticker_to_company['V'] = 'Visa'
ticker_to_company['LYFT'] = 'Lyft'
ticker_to_company['COST'] = 'Costco'
ticker_to_company['ABNB'] = 'Airbnb'
ticker_to_company['AMZN'] = 'Amazon'
ticker_to_company['COUR'] = 'Coursera'
ticker_to_company['UBER'] = 'Uber'
ticker_to_company['AXP'] = 'American Express'
ticker_to_company['MAR'] = 'Marriot'
ticker_to_company['TWTR'] = 'Twitter'
ticker_to_company['NFLX'] = 'Netflix'
ticker_to_company['AAL'] = 'American Airlines'
ticker_to_company['ZM'] = 'Zoom'
ticker_to_company['DAL'] = 'Delta Airlines'
ticker_to_company['MA'] = 'Mastercard'
ticker_to_company['HLT'] = 'Hilton'
ticker_to_company['WMT'] = 'Walmart'

def init_game():
    st.title("The Game")
    username = st.text_input("Enter nickname", )
    selected_stocks = None

    if username:
        st.subheader(f"Okay {username}, Do you wanna make some money?")
        cols = st.columns(3)
        cols[1].markdown("![Alt Text](https://media4.giphy.com/media/lSlqrcXKrdLRg8Zq5G/giphy.gif?cid=ecf05e47ykug7vv6n9pqqfktd4s4wit5ur69uunqbsysf6i8&rid=giphy.gif&ct=g)")

        selected_stocks = st.multiselect("Select the stocks you want to build your portfolio with:", company_to_ticker.keys(), ['Amazon', 'Visa', 'Netflix', 'Marriot'])

    if selected_stocks:
        st.subheader("You have 100 dollars, use it wisely.")
        cols = st.columns(3)
        cols[1].image("website/artifacts/dollarbill.png")
        cols = st.columns(len(selected_stocks))
        amounts = []
        for i in range(len(selected_stocks)):
            amounts.append(cols[i].text_input(selected_stocks[i]))
        total_rem = 100 
        if amounts[0] != "": 
            total_rem = 100 
            for amount in amounts:
                if amount != "":
                    total_rem -= int(amount)
        if total_rem > 0:
            st.subheader(f"You still have ${total_rem} remaining")
        elif total_rem < 0:
            st.subheader("You have exceed the amount!")
        else:
            dates = st.slider(
            "Choose your buy and sell date.",
            min_value = datetime(2019, 12, 31),
            max_value = datetime(2021, 11, 17),
            value=(datetime(2020, 8, 4), datetime(2021, 2, 17)),
            format="YY-MM-DD")
            show_stocks_trend(selected_stocks)
            cols = st.columns(7)
            if cols[3].button("Show results"):
                amounts = list(map(int, amounts))
                compute_results(username, selected_stocks, dates, amounts)


if __name__ == "__main__":
    init_game()

def show_stocks_trend(stocks, dates=None):
    tickers = list(map(company_to_ticker.get, stocks))
    df_stock = pd.read_csv('website/../Data/DailyStockData.csv')
    df_covid_vaccine = pd.read_csv('website/../Data/raw_vaccination/cleaned_vaccination_data.csv')
    df_covid_infection = pd.read_csv('website/../Data/usa_national_level_daily_new_covid_cases.csv')
    # Merging data to align time

    df_covid_infection = df_covid_infection[["Date", "Daily New Cases"]]
    df_covid_vaccine = df_covid_vaccine[['date', 'daily_vaccinations']].rename(columns={"date": "Date", "daily_vaccinations": "Number of People Vaccinated Daily"})
    df_stock.set_index('Date', inplace=True)
    df_covid_vaccine.set_index('Date', inplace=True)
    df_covid_infection.set_index('Date', inplace=True)
    merged_data = df_stock.merge(df_covid_vaccine, how='outer', left_index=True, right_index=True)
    merged_data = merged_data.tail(569)
    merged_data = merged_data.merge(df_covid_infection, how='outer', left_index=True, right_index=True).reset_index()
    # if dates:
        # do subset
    fig = make_subplots(rows=3, cols=1, subplot_titles=('Industry stock prices',  'Daily New Cases', 'Number of People Vaccinated Daily'), row_width=[0.3,0.3, 0.7])

    df_required = merged_data[['Date'] + tickers]
    df_temp = pd.melt(df_required, id_vars=['Date'], value_vars=tickers).rename(columns={"variable": "Company", "value": "Stock Price"}).replace({"Company": ticker_to_company})

    fig1 = px.line(df_temp, x="Date", y="Stock Price", color='Company', title="Stock price")
    fig2 = px.bar(merged_data, x="Date", y="Daily New Cases")
    fig2.update_traces(marker_color="brown", marker_line_width = 0.05)
    fig3 = px.bar(merged_data, x="Date", y='Number of People Vaccinated Daily')
    fig3.update_traces(marker_color="black", marker_line_width = 0.05)
    fig.update_layout(showlegend=False, hovermode='x')

    for tmp in fig1.data:
        fig.append_trace(tmp, row=1, col=1)
    fig.append_trace(fig2.data[0], row=2, col=1)
    fig.append_trace(fig3.data[0], row=3, col=1)


    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def compute_results(username, stocks, dates, amounts):
    st.balloons()
    profits = []
    tickers_start = [100,200,300,400]
    tickers_end = [120,210,240,230]
    
    st.title("Individual outcomes")
    cols = st.columns(len(stocks))
    for i in range(len(stocks)):
        cols[i].subheader(stocks[i])
        cols[i].metric(label="Stock Closing Price", value="{:.2f}".format(tickers_end[i]), delta="{:.2f} %".format((tickers_end[i]-tickers_start[i])*100/tickers_start[i]))
        unit_share = amounts[i]/tickers_start[i]
        cols[i].metric(label="No. of Shares", value="{:.3f}".format(unit_share))
        cols[i].metric(label="Your Cost Price", value="{:.2f}".format(tickers_start[i]*unit_share))
        profits.append(tickers_end[i]*unit_share-amounts[i])
        cols[i].metric(label="Your Sell Price", value="{:.2f}".format(tickers_end[i]*unit_share), delta="{:.2f}".format(profits[i]))
    cols = st.columns(7)
    total_profit = sum(profits)
    cols[3].metric(label="Total Profit", value="{}".format(total_profit))
    rank, percentile = get_leaderboard_info(username, total_profit)
    st.subheader("You did better than {:.2f} % other gamers!".format(percentile))
    st.subheader("This gives you a rank of {} on the leader board!".format(rank))
    cols = st.columns(7)
     
    display_leaderboard()

def get_leaderboard_info(username, profit):
    return 2, 85
    
def display_leaderboard():
    df = pd.DataFrame(np.random.randn(10, 5),columns=('col %d' % i for i in range(5)))
    st.table(df)