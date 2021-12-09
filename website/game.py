import streamlit as st
from datetime import datetime 
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from gamebackend import StockGame
from pathlib import Path

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



def insert_entry(leaderboard,nickname,submission_time, profit):
    temp = pd.DataFrame([{'nickname':nickname,'submission time':submission_time,'profit': profit}])
    frames = [leaderboard,temp]
    leaderboard=pd.concat(frames)
    leaderboard.sort_values(by='profit', ascending=False,inplace=True)
    leaderboard.to_csv('leaderboard.csv',index= False)
   


def init_game():
    st.title("The Game")
    my_file = Path("./leaderboard.csv")
    leaderboard = None
    if my_file.is_file():
        leaderboard = pd.read_csv('leaderboard.csv')
    else:
        column_names = ["nickname",'submission time', "profit"]
        leaderboard = pd.DataFrame(columns = column_names)

    username = st.text_input("Enter nickname", )
    selected_stocks = None
    game = StockGame()

    if username:
        st.subheader(f"Okay {username}, Do you wanna make some money?")
        cols = st.columns(3)
        cols[1].markdown("![Alt Text](https://media4.giphy.com/media/lSlqrcXKrdLRg8Zq5G/giphy.gif?cid=ecf05e47ykug7vv6n9pqqfktd4s4wit5ur69uunqbsysf6i8&rid=giphy.gif&ct=g)")

        selected_stocks = st.multiselect("Select the stocks you want to build your portfolio with:", company_to_ticker.keys(), ['Uber', 'Visa', 'Netflix', 'Marriot'])

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
                compute_results(leaderboard, game,username, selected_stocks, dates, amounts)


if __name__ == "__main__":
    init_game()

def show_stocks_trend(stocks, dates=None, st_object=None):
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
    if st_object:
        st_object.plotly_chart(fig,use_container_width=True) 
    else:
        st.plotly_chart(fig, use_container_width=True)


def compute_results(leaderboard, game,username, stocks, dates, amounts):
    st.balloons()
    profits = []
    maximal_stock_price, minimal_stock_price, buy_date, sell_date, max_profit  = game.compute_optimal_profits(stocks,amounts)
    tickers_start, tickers_end = game.compute_user_outcomes(stocks,dates)
    st.title("Your outcome")
    cols = st.columns([1 for _ in stocks]+[len(stocks)])
    for i in range(len(stocks)):
        cols[i].write(stocks[i])
        cols[i].metric(label="Stock Closing Price", value="{:.2f}".format(tickers_end[i]), delta="{:.2f} %".format((tickers_end[i]-tickers_start[i])*100/tickers_start[i]))
        unit_share = amounts[i]/tickers_start[i]
        cols[i].metric(label="No. of Shares", value="{:.3f}".format(unit_share))
        cols[i].metric(label="Your Cost Price", value="{:.2f}".format(tickers_start[i]*unit_share))
        profits.append(tickers_end[i]*unit_share-amounts[i])
        cols[i].metric(label="Your Sell Price", value="{:.2f}".format(tickers_end[i]*unit_share), delta="{:.2f}".format(profits[i]))

    show_stocks_trend(stocks, None, cols[-1])
    cols = st.columns(7)
    user_profit = sum(profits)

    if user_profit>=0:
        cols[3].metric(label="Total Profit", value="{:.2f}$".format(user_profit))
    else:
        cols[3].metric(label="Total Loss", value="{:.2f}$".format(user_profit))

    st.title("Optimal outcome")
    st.subheader("You could have made a profit of  {:.2f}$ if you had bought the stock on ".format(max_profit)+buy_date+" and sold on "+sell_date+" !")
    cols = st.columns([len(stocks)]+[1 for _ in stocks])
    profits = []
    for i in range(len(stocks)):
        cols[i+1].subheader(stocks[i])
        cols[i+1].metric(label="Stock Closing Price", value="{:.2f}".format(maximal_stock_price[i]), delta="{:.2f} %".format((maximal_stock_price[i]-minimal_stock_price[i])*100/minimal_stock_price[i]))
        unit_share = amounts[i]/minimal_stock_price[i]
        cols[i+1].metric(label="No. of Shares", value="{:.3f}".format(unit_share))
        cols[i+1].metric(label="Your Cost Price", value="{:.2f}".format(minimal_stock_price[i]*unit_share))
        profits.append(maximal_stock_price[i]*unit_share-amounts[i])
        cols[i+1].metric(label="Your Sell Price", value="{:.2f}".format(maximal_stock_price[i]*unit_share), delta="{:.2f}".format(profits[i]))
    show_stocks_trend(stocks, None, cols[0])
    cols = st.columns(7)
    total_profit = sum(profits)
    if total_profit>=0:
        cols[3].metric(label="Total Profit", value="{:.2f}$".format(total_profit))
    else:
        cols[3].metric(label="Total Loss", value="{:.2f}$".format(total_profit))
    
    now = datetime.now()
    submission_time = now.strftime("%d/%m/%Y %H:%M:%S")
    insert_entry(leaderboard,username,submission_time, user_profit)    
    rank, percentile = get_leaderboard_info(username,submission_time, total_profit)
    st.subheader("You did better than {:.2f} % other gamers!".format(percentile))
    st.subheader("This gives you a rank of {} on the leader board!".format(rank))
    cols = st.columns(7)

    display_leaderboard()


def get_leaderboard_info(username,submission_time, profit):
    leaderboard = pd.read_csv('leaderboard.csv')
    rank = leaderboard[leaderboard["submission time"]==submission_time].index.values[0]
    total = len(leaderboard["submission time"].values)
    count = total - rank -1
    percentile = count*100//(total-1) if total!=1 else 100
    print(percentile)
    return rank+1, percentile
    
def display_leaderboard():
    my_file = Path("./leaderboard.csv")
    leaderboard = None
    if my_file.is_file():
        leaderboard = pd.read_csv('leaderboard.csv')
        st.table(leaderboard[['nickname','submission time','profit']])