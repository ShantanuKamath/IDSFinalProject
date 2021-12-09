import os
import hydralit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from functools import reduce
from PIL import Image

def stock_tab_main():

    dict_stock_to_company = {}
    dict_stock_to_company['UAL'] = 'United Airlines'
    dict_stock_to_company['V'] = 'Visa'
    dict_stock_to_company['LYFT'] = 'Lyft'
    dict_stock_to_company['COST'] = 'Costco'
    dict_stock_to_company['ABNB'] = 'Airbnb'
    dict_stock_to_company['AMZN'] = 'Amazon'
    dict_stock_to_company['COUR'] = 'Coursera'
    dict_stock_to_company['UBER'] = 'Uber'
    dict_stock_to_company['AXP'] = 'American Express'
    dict_stock_to_company['MAR'] = 'Marriot'
    dict_stock_to_company['TWTR'] = 'Twitter'
    dict_stock_to_company['NFLX'] = 'Netflix'
    dict_stock_to_company['AAL'] = 'American Airlines'
    dict_stock_to_company['ZM'] = 'Zoom'
    dict_stock_to_company['DAL'] = 'Delta Airlines'
    dict_stock_to_company['MA'] = 'Mastercard'
    dict_stock_to_company['HLT'] = 'Hilton'
    dict_stock_to_company['WMT'] = 'Walmart'

    dict_industry_to_stock = {}
    dict_industry_to_stock['Transport'] = ['UBER', 'LYFT']
    dict_industry_to_stock['Hospitality'] = ['ABNB', 'MAR', 'HLT']
    dict_industry_to_stock['Consumer Spending'] = ['V', 'AXP', 'MA']
    dict_industry_to_stock['Commerce'] = ['AMZN', 'WMT', 'COST']
    dict_industry_to_stock['Online Services'] = ['COUR', 'ZM', 'TWTR', 'NFLX']
    dict_industry_to_stock['Airlines'] = ['UAL', 'DAL', 'AAL']



    df_stock = pd.read_csv("website/../Data/DailyStockData.csv")
    df_covid_vaccine = pd.read_csv('website/../Data/raw_vaccination/cleaned_vaccination_data.csv')
    df_covid_infection = pd.read_csv('website/../Data/usa_national_level_daily_new_covid_cases.csv')




    # Merging data to align time

    df_covid_infection = df_covid_infection[["Date", "Daily New Cases"]]
    df_covid_vaccine = df_covid_vaccine[['date', 'daily_vaccinations']].rename(columns={"date": "Date", "daily_vaccinations": "Number of People Vaccinated Daily"})
    df_stock.set_index('Date', inplace=True)
    df_covid_vaccine.set_index('Date', inplace=True)
    df_covid_infection.set_index('Date', inplace=True)
    merged_data = df_stock.merge(df_covid_vaccine, how='outer', left_index=True, right_index=True)
    merged_data = merged_data.merge(df_covid_infection, how='outer', left_index=True, right_index=True).reset_index()




    # st.sidebar.title('Jump to the sector...')
    # options = st.sidebar.radio('Select the sector:', 
    #     ['Transport', 'Hospitality', 'Consumer Spending', 'E-Commerce', 'Online Services', 'Airlines'])

    # if(options == 'Transport'):


    ## Beginning stock page images


    image = Image.open('website/artifacts/covid_stock_teaser.jpeg')

    st.image(image, use_column_width='always', caption='How the stock market plummeted due to covid.')




    ## Adding basic stock performance

    st.markdown('#')
    st.markdown('<h2><span style="color:#083CA5">Stock Performance in Covid Times</span></h2>',unsafe_allow_html=True)

    stocks = []
    companies = []
    import glob
    for file in glob.glob("website/../Companies/*"):
        company_name = os.path.basename(file).split(".")[0]
        companies.append(company_name)
        stock = pd.read_csv(file)
        stock = stock[["Date", "Close"]]
        stock.rename(columns={"Close": company_name}, inplace=True)
        stock.set_index(["Date"],inplace=True)
        stocks.append(stock)
        
    stocks_df = reduce(lambda left,right: pd.merge(left,right, how='outer', left_index=True, right_index=True), stocks)
    stocks_df = stocks_df.drop(labels="2021-11-19", axis=0) # Incomplete data for yesterday

    fig = make_subplots(rows=3, cols=1, subplot_titles=('Stock price comparison for considered companies',  'Daily New Cases', 'Number of People Vaccinated Daily'), row_width=[0.3, 0.3, 0.7])

    df_temp = pd.melt(stocks_df.reset_index(), id_vars=['Date'], value_vars=dict_stock_to_company.keys()).rename(columns={"variable": "Company", "value": "Stock Price"}).replace({"Company": dict_stock_to_company})
    fig1 = px.line(df_temp, x="Date", y="Stock Price", color='Company', title="Stock price for considered companies")
    fig2 = px.bar(merged_data, x="Date", y="Daily New Cases")
    fig2.update_traces(marker_color="brown", marker_line_width = 0.05)
    fig3 = px.bar(merged_data, x="Date", y='Number of People Vaccinated Daily')
    fig3.update_traces(marker_color="black", marker_line_width = 0.05)

    for tmp in fig1.data:
        fig.append_trace(tmp, row=1, col=1)
    fig.append_trace(fig2.data[0], row=2, col=1)
    fig.append_trace(fig3.data[0], row=3, col=1)


    fig.update_layout(height=700, width=900)
    # fig.show()
    st.write(fig)


    st.markdown(""" * Amazon stock values operate at a much higher scale than the rest of the stocks.


    * Better to look at normalized values to visualize the trends for all the companies in a single plot.


    <b><span style="font-size: 125%">Log transforming to capture the relative scale and stock price variations</span></b>

    """, unsafe_allow_html=True)


    mean_norm_df = (stocks_df-stocks_df.mean())/stocks_df.std()
    inc_df = stocks_df.diff(axis=0)/stocks_df
    min_df = stocks_df-stocks_df.min()
    max_df = stocks_df-stocks_df.max()
    log_df = np.log(stocks_df)

    fig = make_subplots(rows=3, cols=1, subplot_titles=('Stock price comparison for considered companies',  'Daily New Cases', 'Number of People Vaccinated Daily'), row_width=[0.3, 0.3, 0.7])

    df_temp = pd.melt(log_df.reset_index(), id_vars=['Date'], value_vars=dict_stock_to_company.keys()).rename(columns={"variable": "Company", "value": "Stock Price"}).replace({"Company": dict_stock_to_company})
    fig1 = px.line(df_temp, x="Date", y="Stock Price", color='Company', title="Stock price comparison for considered companies")
    fig2 = px.bar(merged_data, x="Date", y="Daily New Cases")
    fig2.update_traces(marker_color="brown", marker_line_width = 0.05)
    fig3 = px.bar(merged_data, x="Date", y='Number of People Vaccinated Daily')
    fig3.update_traces(marker_color="black", marker_line_width = 0.05)

    for tmp in fig1.data:
        fig.append_trace(tmp, row=1, col=1)
    fig.append_trace(fig2.data[0], row=2, col=1)
    fig.append_trace(fig3.data[0], row=3, col=1)


    fig.update_layout(height=700, width=900)
    # fig.show()
    st.write(fig)

    st.markdown(""" * Its easy to quickly realize that almost all of the stocks, that is the market, fell during the week of March 2nd, 2020.

    """, unsafe_allow_html=True)




    st.markdown('#')
    st.markdown('<h2><span style="color:#083CA5">Transport Sector</span></h2>',unsafe_allow_html=True)
    image = Image.open('website/artifacts/covid_transport_image.jpeg')
    
    st.markdown('#')

    col1, col2, col3 = st.columns([2,6,1])

    with col1:
        st.write("")

    with col2:
        st.image(image, caption='Empty roads due to covid lockdowns.')

    with col3:
        st.write("")


    industry = 'Transport'

    fig = make_subplots(rows=3, cols=1, subplot_titles=(industry + ' Industry stock prices',  'Daily New Cases', 'Number of People Vaccinated Daily'), row_width=[0.3, 0.3, 0.7])

    df_required = merged_data[['Date'] + dict_industry_to_stock[industry]]
    df_temp = pd.melt(df_required, id_vars=['Date'], value_vars=dict_industry_to_stock[industry]).rename(columns={"variable": "Company", "value": "Stock Price"}).replace({"Company": dict_stock_to_company})

    fig1 = px.line(df_temp, x="Date", y="Stock Price", color='Company', title="Stock price for " + str(industry) +  ' industry ')
    fig2 = px.bar(merged_data, x="Date", y="Daily New Cases")
    fig2.update_traces(marker_color="brown", marker_line_width = 0.05)
    fig3 = px.bar(merged_data, x="Date", y='Number of People Vaccinated Daily')
    fig3.update_traces(marker_color="black", marker_line_width = 0.05)

    for tmp in fig1.data:
        fig.append_trace(tmp, row=1, col=1)
    fig.append_trace(fig2.data[0], row=2, col=1)
    fig.append_trace(fig3.data[0], row=3, col=1)


    fig.update_layout(height=700, width=900)
    # fig.show()
    st.write(fig)

    st.markdown('#### How has the transport industry reponsed to Covid-19?')
    st.markdown("""
      As soon as covid cases become prevalent in the United states, the stock price for the transport industry fell.
    - Due to the sentiment that people will not want step out or restrictive quarantine laws.
    - This lead to lesser rides and cutt a  majority share of revenue for these companies


    Surprisingly, when the covid cases were at their peak:
    - Stocks begin to rise mostly due to vaccines beings rolled out to the general public.
    - This boosts the sentiment that people will be up and about again.

    Waves:
    - Both the waves seemed to cause the transport industry to remain almost plateau'd.
        - Before the first wave, the industry had already fallen, and there was no change until vaccine rollout.
        - Before the second wave, just as the industry was picking up again, the wave plateau'd the prices. 
        
    Overall the transport industry hasn't yet fully recovered from the impact but is on track to be right where it was when it began, almost two years later.

    """)

    st.markdown("""
      <b><span style="font-size: 115%; color:#D71806">Interesting Articles:</span></b> <br>

      <div class="image123">
      <a href="https://www.forbes.com/sites/teradata/2020/10/06/after-covid-is-the-transport-and-logistics-industry-an-open-goal-for-dominance-by-data-giants/?sh=1b7643ec71f3">
        <div style="float:left;margin-right:50px;margin-left:20px">
            <img src="https://ggsc.s3.amazonaws.com/images/uploads/How_to_Be_Deliberate_About_Consuming_Coronavirus_News.jpg" width="70" height="70">
            <p style="text-align:center;">Forbes</p>
        </div>
      </a>
      </div>

      """, unsafe_allow_html=True)



    st.markdown('#')
    st.markdown('<h2><span style="color:#083CA5">Hospitality Sector</span></h2>',unsafe_allow_html=True)
    image = Image.open('website/artifacts/covid_hospitality_image.jpeg')
    
    st.markdown('#')

    col1, col2, col3 = st.columns([2,6,1])

    with col1:
        st.write("")

    with col2:
        st.image(image, caption='Empty restaurant due to covid fear and restrictions.')

    with col3:
        st.write("")

    industry = 'Hospitality'

    fig = make_subplots(rows=3, cols=1, subplot_titles=(industry + ' Industry stock prices',  'Daily New Cases', 'Number of People Vaccinated Daily'), row_width=[0.3, 0.3, 0.7])

    df_required = merged_data[['Date'] + dict_industry_to_stock[industry]]
    df_temp = pd.melt(df_required, id_vars=['Date'], value_vars=dict_industry_to_stock[industry]).rename(columns={"variable": "Company", "value": "Stock Price"}).replace({"Company": dict_stock_to_company})

    fig1 = px.line(df_temp, x="Date", y="Stock Price", color='Company', title="Stock price for " + str(industry) +  ' industry ')
    fig2 = px.bar(merged_data, x="Date", y="Daily New Cases")
    fig2.update_traces(marker_color="brown", marker_line_width = 0.05)
    fig3 = px.bar(merged_data, x="Date", y='Number of People Vaccinated Daily')
    fig3.update_traces(marker_color="black", marker_line_width = 0.05)

    for tmp in fig1.data:
        fig.append_trace(tmp, row=1, col=1)
    fig.append_trace(fig2.data[0], row=2, col=1)
    fig.append_trace(fig3.data[0], row=3, col=1)


    fig.update_layout(height=700, width=900)
    # fig.show()
    st.write(fig)

    st.markdown('#### The pandemic meant that people couldn\'t move out of their homes...This must have hurt the hospitality sector really badly :(')

    st.markdown(""" For the hospitality industry we can see that once the first few cases of covid were reported in the US in early January 2020, the stock price of the hospitality industry fell because:

  *  There was a negative sentiment amongst the people because of all the uncertainty around covid.
  *  There were lockdowns enforced in different parts of the country because of which people were not travelling, and subsequently not staying in any hotels/Airbnbs.

#### What prompted recovery at a time when people were forced to stay at home?

Towards the end of the first wave in February 2021, we can see that the stock prices increase once again. This is because lockdowns and travel restrictions started getting lifted across the US. People started travelling more, and staying in hotels/Airbnbs.
    An interesting trend that we note here is that the stock prices of Airbnb increased more that the stock prices of hotels like Marriott and Hilton. We hypothesise that this could be because of the following reasons: 

- Airbnb had just IPO'd hence their stock price was high because of the positive sentiments towards it.
- Also, this was at a time when most companies had switched to a remote work from home policy. As a result a lot of individuals started travelling to different places, and started working remotely while staying in airbnbs.

During the second wave the stock prices dipped again due to the fact that lockdowns and quarantine rules were enforced once again, leading to lesser travel and stay in hotels. Once again, once the second wave subsided, and lockdowns were lifted allowing to people to travel and stay in hotels, the stock prices increased.
    """)
    st.markdown("""
      <b><span style="font-size: 115%; color:#D71806">Interesting Articles:</span></b> <br>

      <div class="image123">
      <a href="https://www.mckinsey.com/industries/travel-logistics-and-infrastructure/our-insights/hospitality-and-covid-19-how-long-until-no-vacancy-for-us-hotels">
        <div style="float:left;margin-right:50px;margin-left:20px">
            <img src="https://ggsc.s3.amazonaws.com/images/uploads/How_to_Be_Deliberate_About_Consuming_Coronavirus_News.jpg" width="70" height="70">
            <p style="text-align:center;">McKinsey</p>
        </div>
      </a>
      <a href="https://www.nbcnews.com/news/us-news/covid-hit-hotel-industry-hard-data-shows-it-s-still-n1280061">
        <div style="float:left;margin-right:5px;">
            <img src="https://i.guim.co.uk/img/media/7af5513c2f737babab0e27441d163a54ee477ed2/902_0_2730_1638/master/2730.jpg?width=1200&quality=85&auto=format&fit=max&s=44355715ee04094d1a9689bac70ab4ed" width="70" height="70">
            <p style="text-align:center;">NBC News</p>
        </div>
      </a>
      </div>

      """, unsafe_allow_html=True)



    st.markdown('#')
    


    st.markdown('#')
    st.markdown('<h2><span style="color:#083CA5">Consumer Spending</span></h2>',unsafe_allow_html=True)

    image = Image.open('website/artifacts/covid_closed_image.jpg')
    st.markdown('#')

    col1, col2, col3 = st.columns([2,6,1])

    with col1:
        st.write("")

    with col2:
        st.image(image, caption='How covid led to businesses shutting down.')

    with col3:
        st.write("")

    industry = 'Consumer Spending'

    fig = make_subplots(rows=3, cols=1, subplot_titles=(industry + ' Industry stock prices',  'Daily New Cases', 'Number of People Vaccinated Daily'), row_width=[0.3, 0.3, 0.7])

    df_required = merged_data[['Date'] + dict_industry_to_stock[industry]]
    df_temp = pd.melt(df_required, id_vars=['Date'], value_vars=dict_industry_to_stock[industry]).rename(columns={"variable": "Company", "value": "Stock Price"}).replace({"Company": dict_stock_to_company})

    fig1 = px.line(df_temp, x="Date", y="Stock Price", color='Company', title="Stock price for " + str(industry) +  ' industry ')
    fig2 = px.bar(merged_data, x="Date", y="Daily New Cases")
    fig2.update_traces(marker_color="brown", marker_line_width = 0.05)
    fig3 = px.bar(merged_data, x="Date", y='Number of People Vaccinated Daily')
    fig3.update_traces(marker_color="black", marker_line_width = 0.05)

    for tmp in fig1.data:
        fig.append_trace(tmp, row=1, col=1)
    fig.append_trace(fig2.data[0], row=2, col=1)
    fig.append_trace(fig3.data[0], row=3, col=1)


    fig.update_layout(height=700, width=900)
    # fig.show()
    st.write(fig)

    st.markdown('#### How was spending impacted due to Covid, and how is it shaping up with vaccination and the gradual decrease in cases?')

    st.markdown(""" * The stock prices drop from around the 20th February 2020, when news of Covid-19 began to spread, and the first cases of Covid-19 were reported. The stock prices plummet and hit their lowest values around 23rd March 2020.


* Due to the lockdown in the US, the consumer and corporate spending was largely very low. This is reflected in the stock prices recovering very slowly from the initial drop.


* We see that the stocks begin to rise as the lockdown eased in July 2020. People and businesses started spending more and there was an increase in the econonmic activity.


* When the first wave began around end of October 2020, stock prices for these companies fell suddenly. Businesses were forced to shut down or slow down, and consumers were forced to stay at home. Through the first wave, the stock prices remain relatively stagnant.

#### Did vaccination and the subsequent waves have a similar detrimental impact on business and spending?

* As vaccination picks up starting February 2021, the stock prices continue to rise. Thus, vaccination instilled confidence in people, who began moving back to their pre-covid spending behavour.


* With the second wave starting around July 2021, the stock prices again began to drop for Visa and Mastercard, though not to the same extent as the initial hyteria and the first wave, reflecting the spending slowdown by consumers and corporates.
    """)




    st.markdown('#')
    st.markdown('<h2><span style="color:#083CA5">E-Commerce Sector</span></h2>',unsafe_allow_html=True)
    image = Image.open('website/artifacts/covid_ecommerce_image.jpeg')
    
    st.markdown('#')

    col1, col2, col3 = st.columns([2,6,1])

    with col1:
        st.write("")

    with col2:
        st.image(image, caption='Booming E-Commerce platforms during covid.')

    with col3:
        st.write("")

    industry = 'Commerce'

    fig = make_subplots(rows=4, cols=1, subplot_titles=(industry + ' Industry stock prices', industry + ' Industry stock prices (log)',  'Daily New Cases', 'Number of People Vaccinated Daily'), row_width=[0.3, 0.3, 0.7, 0.7])

    df_required = merged_data[['Date'] + dict_industry_to_stock[industry]]
    df_temp1 = pd.melt(df_required, id_vars=['Date'], value_vars=dict_industry_to_stock[industry]).rename(columns={"variable": "Company", "value": "Stock Price"}).replace({"Company": dict_stock_to_company})

    df_required[dict_industry_to_stock[industry]] = np.log(df_required[dict_industry_to_stock[industry]])
    df_temp = pd.melt(df_required, id_vars=['Date'], value_vars=dict_industry_to_stock[industry]).rename(columns={"variable": "Company", "value": "Stock Price"}).replace({"Company": dict_stock_to_company})

    fig0 = px.line(df_temp1, x="Date", y="Stock Price", color='Company', title="Stock price for " + str(industry) +  ' industry ')
    fig1 = px.line(df_temp, x="Date", y="Stock Price", color='Company', title="Stock price for " + str(industry) +  ' industry ')
    fig2 = px.bar(merged_data, x="Date", y="Daily New Cases")
    fig2.update_traces(marker_color="brown", marker_line_width = 0.05)
    fig3 = px.bar(merged_data, x="Date", y='Number of People Vaccinated Daily')
    fig3.update_traces(marker_color="black", marker_line_width = 0.05)

    for tmp in fig0.data:
        fig.append_trace(tmp, row=1, col=1)
    for tmp in fig1.data:
        fig.append_trace(tmp, row=2, col=1)
    fig.append_trace(fig2.data[0], row=3, col=1)
    fig.append_trace(fig3.data[0], row=4, col=1)


    fig.update_layout(height=900, width=900)
    # fig.show()
    st.write(fig)

    st.markdown('#### With people stuck at home, the e-commerce industry should have proliferated during Covid. Did that actually happen?')

    # st.markdown("""* An analysis of the plots reveal a visible dip in the stock prices of E-commerce giants during the months of March 2020. Historical analysis of the events indicate that this was the time when around 10 states confirmed their first cases including New York. Also interestingly during the week from March 9-15 the stock markets plummeted 7.79%. This explains the sudden dip observed during this time frame.

    # <b>Source</b>: https://abcnews.go.com/Health/year-covid-19-us-march-2020/story?id=76204691

    # * Yet another such dip is observed in March 2021. This could be due to the increasing speculation of lockdown across states.

    # <b>Source</b>: https://www.usatoday.com/storytelling/coronavirus-reopening-america-map/

    # * Some other interesting observations to note are that the e-commerce industry experienced a slight boom during the covid era, however the changes are not very significant. This is contrary to our intuition in which we expected a  positive investor outlook and subsequently a massive increase in e-commerce stocks as lockdowns and other restrictions would cause people to rely on e-commerce more.
    # * Also there seems to be no impact of vaccination on the changes in e-commerce stock prices """, unsafe_allow_html=True)

    st.markdown("""* An analysis of the plots reveal a visible dip in the stock prices of E-commerce giants during the months of March 2020. Historical analysis of the events indicate that this was the time when around 10 states confirmed their first cases including New York. Also interestingly during the week from March 9-15 the stock markets plummeted 7.79%. This explains the sudden dip observed during this time frame.

* Yet another such dip is observed in March 2021. This could be due to the increasing speculation of lockdown across states.

* Some other interesting observations to note are that the e-commerce industry experienced a slight boom during the covid era, however the changes are not very significant. This is contrary to our intuition in which we expected a  positive investor outlook and subsequently a massive increase in e-commerce stocks as lockdowns and other restrictions would cause people to rely on e-commerce more.
* Also there seems to be no impact of vaccination on the changes in e-commerce stock prices """, unsafe_allow_html=True)

    st.markdown("""
      <b><span style="font-size: 115%; color:#D71806">Interesting Articles:</span></b> <br>

      <div class="image123">
      <a href="https://abcnews.go.com/Health/year-covid-19-us-march-2020/story?id=76204691">
        <div style="float:left;margin-right:50px;margin-left:20px">
            <img src="https://ggsc.s3.amazonaws.com/images/uploads/How_to_Be_Deliberate_About_Consuming_Coronavirus_News.jpg" width="70" height="70">
            <p style="text-align:center;">ABC News</p>
        </div>
      </a>
      <a href="https://www.usatoday.com/storytelling/coronavirus-reopening-america-map/">
        <div style="float:left;margin-right:5px;">
            <img src="https://i.guim.co.uk/img/media/7af5513c2f737babab0e27441d163a54ee477ed2/902_0_2730_1638/master/2730.jpg?width=1200&quality=85&auto=format&fit=max&s=44355715ee04094d1a9689bac70ab4ed" width="70" height="70">
            <p style="text-align:center;">USA Today</p>
        </div>
      </a>
      </div>

      """, unsafe_allow_html=True)


    # <iframe src="https://giphy.com/embed/UUsOy6IWmzw6mmeOpQ" width="70" height="70" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/virus-covid19-covid-19-UUsOy6IWmzw6mmeOpQ"></a></p>
            

    st.markdown('#')
    
    image = Image.open('website/artifacts/covid_online_image.jpeg')

    # st.image(image, use_column_width=True, caption='How covid shifted everything online, from learning to interaction etc.')

    

    st.markdown('#')
    st.markdown('<h2><span style="color:#083CA5">Online Services Sector</span></h2>',unsafe_allow_html=True)

    st.markdown('#')

    col1, col2, col3 = st.columns([2,6,1])

    with col1:
        st.write("")

    with col2:
        st.image(image, caption='How covid shifted everything online, from learning to interaction etc.')

    with col3:
        st.write("")


    industry = 'Online Services'

    fig = make_subplots(rows=3, cols=1, subplot_titles=(industry + ' Industry stock prices',  'Daily New Cases', 'Number of People Vaccinated Daily'), row_width=[0.3, 0.3, 0.7])

    df_required = merged_data[['Date'] + dict_industry_to_stock[industry]]
    df_temp = pd.melt(df_required, id_vars=['Date'], value_vars=dict_industry_to_stock[industry]).rename(columns={"variable": "Company", "value": "Stock Price"}).replace({"Company": dict_stock_to_company})

    fig1 = px.line(df_temp, x="Date", y="Stock Price", color='Company', title="Stock price for " + str(industry) +  ' industry ')
    fig2 = px.bar(merged_data, x="Date", y="Daily New Cases")
    fig2.update_traces(marker_color="brown", marker_line_width = 0.05)
    fig3 = px.bar(merged_data, x="Date", y='Number of People Vaccinated Daily')
    fig3.update_traces(marker_color="black", marker_line_width = 0.05)

    for tmp in fig1.data:
        fig.append_trace(tmp, row=1, col=1)
    fig.append_trace(fig2.data[0], row=2, col=1)
    fig.append_trace(fig3.data[0], row=3, col=1)


    fig.update_layout(height=700, width=900)
    # fig.show()
    st.write(fig)

    st.markdown('#### The pandemic shifted our entire world online. Online services must have made big money. Lets see how...')

    st.markdown("""Since there is insufficient data for Coursera, we will be ignoring it in our analysis. Log transforming the data to show the data on a better scale.

With rise of covid cases in United States, Online Services stock value started rising significantly:

   * All three of them provide great stock market boosts. As people spent more time at home (less travel time, more idle time), they turned to online platforms for entertainment as well as social interaction.
   * Zoom especially became one of the go to video conferencing platforms adopted by educational institutes as well as corporates.
   * Twitter played its role in providing a platform to share covid news and voice out opinions.
   * Netflix provided a quick and fun way to take away boredom.

With the rollout of vaccines:

   * Twitter and Netflix were able to plateau or atleast rise a little.
   * Zoom started showing a downward trend probably due to companies and people going back to making things in person.

Yet, overall the online services have greatly increased their overall value compared to precovid times. There was a consistent rise in value through out the start and end of various waves of covid.
 """)



    st.markdown('#')
    
    image = Image.open('website/artifacts/covid_airline_image.jpeg')

    # st.image(image, use_column_width=True, caption='How the airline industry crashed due to covid.')


    st.markdown('#')
    st.markdown('<h2><span style="color:#083CA5">Airlines Sector</span></h2>',unsafe_allow_html=True)

    st.markdown('#')

    col1, col2, col3 = st.columns([2,6,1])

    with col1:
        st.write("")

    with col2:
        st.image(image, caption='How the airline industry crashed due to covid.')

    with col3:
        st.write("")

    industry = 'Airlines'

    fig = make_subplots(rows=3, cols=1, subplot_titles=(industry + ' Industry stock prices',  'Daily New Cases', 'Number of People Vaccinated Daily'), row_width=[0.3, 0.3, 0.7])

    df_required = merged_data[['Date'] + dict_industry_to_stock[industry]]
    df_temp = pd.melt(df_required, id_vars=['Date'], value_vars=dict_industry_to_stock[industry]).rename(columns={"variable": "Company", "value": "Stock Price"}).replace({"Company": dict_stock_to_company})

    fig1 = px.line(df_temp, x="Date", y="Stock Price", color='Company', title="Stock price for " + str(industry) +  ' industry ')
    fig2 = px.bar(merged_data, x="Date", y="Daily New Cases")
    fig2.update_traces(marker_color="brown", marker_line_width = 0.05)
    fig3 = px.bar(merged_data, x="Date", y='Number of People Vaccinated Daily')
    fig3.update_traces(marker_color="black", marker_line_width = 0.05)

    for tmp in fig1.data:
        fig.append_trace(tmp, row=1, col=1)
    fig.append_trace(fig2.data[0], row=2, col=1)
    fig.append_trace(fig3.data[0], row=3, col=1)


    fig.update_layout(height=700, width=900)
    # fig.show()
    st.write(fig)

    st.markdown('#### With countries imposing travel restrictions, have airlines recovered till date?')

    st.markdown("""Undoubtedly, the Airlines industry was hit the worst because of covid. Lockdowns, flight restrictions, travel bans meant people were not using airlines anymore, hence naturally their stock prices were expected to come down. Lets do a drill down of the above plot and note our observations:

   * We can see that ALL airlines stocks had a major fall in February 2020, and they have not been able to recover to their original glory since

#### Has vaccine rollout led to some sort of recovery for the industry?

   * We oberve that the stock prices started picking up pace around December 2020 -  January 2021, this can be accredited to the increase in vaccination (we see that the curve uphill begins around January 2021). Vaccination restored hope amongsts people that we might be able to fight off covid, hence deeply hit industries started to pick up again.

   * All 3 - United Airlines, American Airlines, and Delta Airlines showed a similar trend, though in absolute terms the drop in United shares was the maximum.  """)


    st.markdown("""
      <b><span style="font-size: 115%; color:#D71806">Interesting Articles:</span></b> <br>

      <div class="image123">
      <a href="https://www.nytimes.com/2021/04/22/business/airlines-recovery-american-southwest.html">
        <div style="float:left;margin-right:50px;margin-left:20px">
            <img src="https://ggsc.s3.amazonaws.com/images/uploads/How_to_Be_Deliberate_About_Consuming_Coronavirus_News.jpg" width="70" height="70">
            <p style="text-align:center;">NY Times</p>
        </div>
      </a>
      </div>

      """, unsafe_allow_html=True)


    #### Interesting articles

    # https://www.mckinsey.com/industries/travel-logistics-and-infrastructure/our-insights/hospitality-and-covid-19-how-long-until-no-vacancy-for-us-hotels
    # https://news.un.org/en/story/2021/05/1091182
    # https://www.trade.gov/impact-covid-pandemic-ecommerce
    # https://www.nytimes.com/2021/04/22/business/airlines-recovery-american-southwest.html

if __name__ == "__main__":
  stock_tab_main()