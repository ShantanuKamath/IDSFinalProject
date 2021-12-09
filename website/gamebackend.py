import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

class StockGame:
    def __init__(self):
        self.stock_data = pd.read_csv('website/../Data/DailyStockData.csv')

        #self.stock_data = self.stock_data[self.stock_data ['Date'].between(99, 101)]
        self.company_to_ticker = {}
        self.company_to_ticker['United Airlines'] = 'UAL'
        self.company_to_ticker['Visa'] =  'V'
        self.company_to_ticker['Lyft'] =  'LYFT'
        self.company_to_ticker['Costco'] =  'COST'
        self.company_to_ticker['Airbnb'] =  'ABNB'
        self.company_to_ticker['Amazon'] =  'AMZN'
        self.company_to_ticker['Coursera'] =  'COUR'
        self.company_to_ticker['Uber'] =  'UBER'
        self.company_to_ticker['American Express'] = 'AXP'
        self.company_to_ticker['Marriot'] =  'MAR'
        self.company_to_ticker['Twitter'] =  'TWTR'
        self.company_to_ticker['Netflix'] =  'NFLX'
        self.company_to_ticker['American Airlines'] = 'AAL'
        self.company_to_ticker['Zoom'] =  'ZM'
        self.company_to_ticker['Delta Airlines'] = 'DAL'
        self.company_to_ticker['Mastercard'] =  'MA'
        self.company_to_ticker['Hilton'] =  'HLT'
        self.company_to_ticker['Walmart'] =  'WMT'
        self.min_value = datetime(2019, 12, 31).strftime("%Y-%m-%d")
        self.max_value = datetime(2021, 11, 17).strftime("%Y-%m-%d")
        self.stock_data = self.stock_data[self.stock_data ['Date'].between(self.min_value, self.max_value)]



    def compute_optimal_profits(self,stocks,amounts):
        column_names = list(map(lambda stock: self.company_to_ticker[stock], stocks))
        self.stock_data[column_names]
        stocks = self.stock_data[column_names].values.tolist()
        time_range = len(stocks)
        weights = np.array(amounts)
        minimal_stock_prices = np.array(stocks[0],dtype=np.float32)
        maximal_stock_prices = np.array(stocks[0],dtype=np.float32)
        min_price_buy = np.sum(minimal_stock_prices*weights)
        max_profit = 0
        point_at_max_profit = -1
        point_at_min_profit = 0
        for i in range(1,time_range):
            profit = np.sum(np.divide((np.array(stocks[i])-minimal_stock_prices),minimal_stock_prices)*weights)
            if  profit > max_profit:
                maximal_stock_prices = np.array(stocks[i])
                max_profit = profit
                point_at_max_profit = i
        
            weighted_value = np.sum(np.array(stocks[i])*(weights))
            if weighted_value < min_price_buy:
                min_price_buy = weighted_value
                minimal_stock_prices = np.array(stocks[i])
                point_at_min_profit = i
        
        buy_date = self.stock_data['Date'].iloc[point_at_min_profit]
        sell_date = self.stock_data['Date'].iloc[point_at_max_profit]

       

        return maximal_stock_prices, minimal_stock_prices, buy_date, sell_date, max_profit

    

    def day_before(self,date):
        day = timedelta(days=1)
        new_date = date - day
        return new_date


    def compute_user_outcomes(self,stocks,dates):
        buy_date , sell_date = dates
        buy_date_str = buy_date.strftime("%Y-%m-%d")
        sell_date_str = sell_date.strftime("%Y-%m-%d")

        temp = buy_date
        while buy_date_str not in self.stock_data['Date'].values.tolist():
            new_date = self.day_before(temp)
            buy_date_str = new_date.strftime("%Y-%m-%d")
            temp = new_date

        
        temp = sell_date
        while sell_date_str not in self.stock_data['Date'].values.tolist():
            new_date = self.day_before(temp)
            sell_date_str = new_date.strftime("%Y-%m-%d")
            temp = new_date

        buy_value = self.stock_data.loc[self.stock_data['Date'] == buy_date_str]
        sell_value = self.stock_data.loc[self.stock_data['Date'] == sell_date_str]
        column_names = list(map(lambda stock: self.company_to_ticker[stock], stocks))
        
        buy_prices = buy_value[column_names].values.tolist()[0]
        sell_prices = sell_value[column_names].values.tolist()[0]
        return buy_prices, sell_prices


    




# game = StockGame()
# print(game.stock_data) 


