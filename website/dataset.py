import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
from PIL import Image

def dataset():

    st.title('Dataset')

    st.markdown("""
    In this project, we explore the effect of COVID-19 cases and vaccination on the Stock market. Hence, we work with 3 different datasets:

    1. Stocks data (Yahoo! Finance)  
    2. Covid cases data (official CDC website)  
    3. Covid vaccination data (official CDC website)  


    All the 3 datasets were scraped, explored, cleaned and then appropiately merged so that their interaction with each other could be studied. 

    In this section, we will explore the above mentioned datasets one by one and highlight how they were transformed into usable information.
    """)

    st.markdown('## 1. Stocks Data')

    st.markdown('### 1.1 Data source and collection')
    
    st.markdown("""
    To ensure accurate and un-altered data, stock information was directly taken from [Yahoo! Finance](https://finance.yahoo.com/).
    Yahoo! Finance provides an easy interface to download stock information as a CSV based on basic parameters like Time period and frequency. A snippet of the webpage used for download process is shown in the figure below.
    """)

    newsize = (500, 330)

    col1, col2, col3 = st.columns([2,6,1])

    with col1:
        st.write("")

    with col2:
        image = Image.open('website/artifacts/yfinance.png')
        st.image(image, caption='How data was procured from Yahoo! Finance, see red box.')

    with col3:
        st.write("")

    st.markdown("""

    For downloading the data, we considered the time period from `2019-01-02` to `2021-11-18` so that the effect of covid could be clearly examined. Further, we take the ***Closing Price*** of the stocks as the representative value for the day.

    Now that we have a way to download stock information, we move on to the next step - deciding which all stocks to consider :)

    As we wanted to explore the effect of Covid on various industries, we selected ***6*** broad categories-

    - Transport  
    - Hospitality  
    - Consumer spending  
    - Commerce  
    - Online services  
    - Airlines  

    Further, we also wanted to study how different companies in the same industry were affected by covid. To carry out this analysis, we selected the following companies in each industry-


    | Industry    | Company |
    | :-: | :-: |
    | Transport      | Uber, Lyft       |
    | Hospitality   | AirBnB, Marriot, Hilton        |
    | Consumer Spending   | Visa, American Express, Mastercard        |
    | Commerce   | Amazon, Walmart, Costco        |
    | Online Services   | Coursera, Zoom, Twitter, Netflix        |
    |Airlines| United Airlines, Delta Airlines, American Airlines|
    """)
    st.text("")


    
    st.markdown("""
    Next, let's explore and clean this data.

    """)

    col1, col2, col3 = st.columns([2,6,1])

    with col1:
        st.write("")

    with col2:
        image = Image.open('website/artifacts/stock_market_1.jpeg')
        # image = image.resize(newsize)
        st.image(image, caption='Covid had a huge impact on the stock market. But were all sectors equally affected?')

    with col3:
        st.write("")

    st.markdown('### 1.2 Dataset description and cleaning')

    st.markdown("""

    The data consists of the closing stock prices (in U.S. $) of the 18 companies considered for the time duration `2019-01-02` to `2021-11-18`. 
    Let's have a look at the average statistics of the data-

    |       |      AXP |      UAL |     COST |      UBER |      WMT |     ABNB |        V |    NFLX |      COUR |      HLT |       MA |      DAL |     LYFT |      MAR |       AAL |     TWTR |      ZM |     AMZN | 
    |:------|---------:|---------:|---------:|----------:|---------:|---------:|---------:|--------:|----------:|---------:|---------:|---------:|---------:|---------:|----------:|---------:|--------:|---------:|
    | count | 728      | 728      | 728      | 639       | 728      | 238      | 728      | 728     | 163       | 728      | 728      | 728      | 668      | 728      | 728       | 728      | 654     |  728     |
    | mean  | 124.345  |  60.2622 | 329.085  |  40.4821  | 125.965  | 165.729  | 193.784  | 437.618 |  38.8583  | 100.85   | 306.434  |  44.6133 |  46.503  | 125.025  |  22.3287  |  44.2367 | 237.124 | 2570.91  |
    | std   |  25.9136 |  22.5993 |  69.0888 |   9.55978 |  16.5384 |  20.8198 |  27.2254 | 103.88  |   5.17739 |  20.3228 |  49.5678 |  11.2803 |  12.2703 |  22.1833 |   7.71048 |  13.5416 | 137.589 |  712.315 |
    | min   |  68.96   |  19.92   | 200.42   |  14.82    |  92.86   | 124.8    | 128.13   | 254.59  |  30.49    |  55.94   | 181.18   |  19.19   |  16.05   |  59.08   |   9.04    |  22      |  62     | 1500.28  |
    | 25%   | 104.948  |  41.6375 | 288.448  |  32.61    | 114.572  | 148.385  | 175.508  | 351.237 |  35.495   |  86.4675 | 270.948  |  38.3575 |  36.36   | 109.675  |  15.53    |  33.12   |  91.64  | 1835.26  |
    | 50%   | 119.39   |  53.455  | 312.48   |  39.96    | 124.97   | 166.48   | 195.195  | 445.32  |  38       |  96.71   | 308.695  |  45.625  |  47.945  | 130.175  |  21.57    |  39.78   | 257.265 | 2586.77  |
    | 75%   | 139.41   |  84.695  | 372.738  |  47.59    | 141.028  | 179.908  | 212.717  | 516.705 |  41.335   | 119.36   | 346.783  |  55.3225 |  56.1825 | 141.713  |  28.7325  |  54.4075 | 352.575 | 3247.42  |
    | max   | 187.08   |  95.28   | 529.37   |  63.18    | 152.79   | 216.84   | 250.93   | 691.69  |  58       | 151.84   | 395.65   |  63.16   |  78.29   | 168.39   |  36.93    |  77.63   | 568.34  | 3731.41  |

    """)
    st.text("")

    st.markdown("""

    From above, we can see Lyft (`LYFT`), Uber (`UBER`), AirBnb (`ABNB`), Zoom (`ZM`) have some missing values. These missing values can be attributed to the fact that the company wasn't listed on the market before 1st Jan 2019.

    |Company| IPO Date|
    |:-:|:--:|
    |Lyft  | March 29, 2019|
    |Zoom  | April 18, 2019 | 
    |Uber | May 10, 2019|
    |AirBnb  | December 10, 2020|
    |Coursera| March 31, 2021|

    """)
    st.text("")

    st.markdown("""
    We also verified that for each company, the data didn't have any missing values after their IPO date. We choose not to fill in these missing values by any form of imputation as they carry important information. Thus, there are propogated as NaN to allow for better visualisations in the next sections.
    """)




    st.markdown('## 2. Covid Cases Data')

    st.markdown('### 2.1 Data source and collection')
    st.markdown("""
    For this project, we are analysing the progression of covid cases in the US and its effect on the stock market, right from when the initial cases started getting reported in early January, 2020 till date. 

    This covid data for the US was fetched from the [official CDC website](https://data.cdc.gov/Case-Surveillance/United-States-COVID-19-Cases-and-Deaths-by-State-o/9mfq-cb36). This was prefered over other sources (which provide processed and cleaned data) because of it's accountability. We wanted to choose the most reliable source so that our analysis reflects the actual ground situation.
    """)

    st.write("")
    st.write("")

    col1, col2, col3, col4 = st.columns([1, 5, 5, 1])
    
    st.write("")

    with col1:
        st.write("")

    with col2:
        image = Image.open('website/artifacts/covid_cases_4.jpg')
        image = image.resize(newsize)
        st.image(image, caption='Covid testing and isolation was the only way forward')
        
    with col3:
        image = Image.open('website/artifacts/covid_cases.png')
        image = image.resize(newsize)
        # st.write("")
        # st.write("")
        st.image(image, caption='Many people lost their near and dear ones to covid')
        
    with col4:
        st.write("")

    st.write("")
        
    st.markdown('### 2.2 Data description')
    st.markdown("""

    The data consists of covid cases reported at a daily granularity, and is collected on a per state basis from 22nd January, 2020 to 21st November, 2021. 

    Since we were only interested in anaylsing how many new covid cases were reported per day, we extracted the following fields from the downloaded dataset:

    - Date: This represents the date for which the covid cases are recorded  
    - State: This reresents which US state for which the data was recorded  
    - Total Cases: A running total of how many positive covid cases have been recorded till date  
    - Daily New Cases: The total number of new covid cases recorded for a particular state on a particular date  
        
    """)

    st.write("")
    st.write("")
    
    col1, col2, col3, col4 = st.columns([1, 5, 5, 1])

    st.write("")
    

    with col1:
        st.write("")

    with col2:
        image = Image.open('website/artifacts/covid_cases_1.jpg')
        image = image.resize((500, 352))
        # st.write("")
        # st.write("")
        st.image(image, caption='Masks became a new norm')

    with col3:
        image = Image.open('website/artifacts/covid_cases_2.jpg')
        image = image.resize(newsize)
        st.image(image, caption='Lockdown was necessary to curb the spread of covid, but that had unpredicted implications.')
        
    with col4:
        st.write("")

    st.markdown('### 2.3 Data Cleaning ')

    st.markdown("""
    In order to preprocess this data, we -

    1. Extracted the relevant fields from the data. Since we were only interested in anaylsing how many new covid cases were reported per day, we extracted the 4 columns 'Date', 'State', 'Total Cases', and 'Daily New Cases' (as described in section 2.2.) from the downloaded dataset.  
    2. We convert the format of the Date column, to a more standardised datetime format  
    3. We then check if there are any NaN or negative values reported. Since there are no NaN/negative values, there is no special handling to be done.  
    4. The downloaded data also had covid statistics for different districts and federated territories of the US. Since we wanted to analyse the data of only the 50 states of the US, we removed all the rows from the data for the districts/federeated territories of American Samoa, Guam, Northern Marina Islands, Puerto Rico, US Virgin Islands, District of Columbia and Palau.  
    5. We also aggregate the daily per state covid cases reported, so as to get the total number of covid cases reported all across the US. This aggregated data is to help us study the covid trend at a national level in the US.  


    """)


    st.markdown('## 3. Covid Vaccination Data')

    st.markdown('### 3.1 Data source and collection')
    
    st.markdown("""

    The data was collected from the official United States Centers for Disease Control and Prevention (CDC) website, which can be accessed [here](https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-Jurisdi/unsk-b7fc/data).
    Like with covid cases data, this was prefered over other sources (like Kaggle, which is much easier to access) because of it's reliability. 
    """)

    st.write("")
    st.write("")
    
    col1, col2, col3, col4 = st.columns([1, 5, 5, 1])
    st.write("")
    
    with col1:
        st.write("")

    with col2:
        image = Image.open('website/artifacts/vaccine1.webp')
        image = image.resize(newsize)
        # st.write("")
        # st.write("")
        st.image(image, caption='Vaccination camps were set-up to ensure rapid coverage of people.')
        
    with col3:
        image = Image.open('website/artifacts/vaccine2.webp')
        image = image.resize((500, 330))
        st.image(image, caption='US was amongst the first countries to start the vaccination process.')
        
    with col4:
        st.write("")

    st.markdown('### 3.2 Data description and cleaning')
    st.markdown("""
    For our analysis, we consider data from 13 December, 2020 till 20 November, 2021 across all states, territories and federal units in the United States. 

    In pre-processing, we removed data for dates outside the set interval. 

    It should be noted that for states which started the vaccination process late, their vaccination data was set to 0 for the earlier dates. 

    Apart from that, not much data cleaning was required since the data is well populated and does not have any anomalies like NaN or Null values.
    """)
    st.write("")
    st.write("")
    
    col1, col2, col3, col4 = st.columns([1, 5, 5, 1])
    st.write("")
    
    with col1:
        st.write("")

    with col2:
        image = Image.open('website/artifacts/vaccine3.webp')
        image = image.resize(newsize)
        st.image(image, caption='Innovative ideas like drive-through vaccination were implemented to reach out to more people')
        
    with col3:
        image = Image.open('website/artifacts/vaccine_4.jpg')
        image = image.resize((500, 353))
        # st.write("")
        # st.write("")
        st.image(image, caption='But not all citizens were ready to take the vaccine.')
        
    with col4:
        st.write("")


    st.markdown('## Ensuring Data Quality')
    st.markdown("""
    To ensure that we have proper and high standard data for our anlysis, we followed the 4 C's of quality. The are discussed below:
    """)

    st.markdown('#### 1. Data Completeness ')
    st.markdown("""
    Data completeness is important to ensure that we don't miss any data point and also that we don't make any inferences from partial data. This was taken care of for all the 3 datasets before proceeding. We have also highlighted how  missing data was handled for the stocks and covid vaccine datasets in the respective sections.
    """)

    st.markdown('#### 2. Data Coherency ')
    st.markdown("""
    We plotted and ran an exploratory analysis on all the individual datasets to ensure that the information was consistent.
    """)

    st.markdown('#### 3. Data Correctness ')
    st.markdown("""
    As we are working with real-life data, it was essential to check that the data is accurate. This is why a reliable source like Yahoo! Finance for stocks and CDC for covid related information were chosen over other sources on the internet. The values were also manually cross-checked for a few dates to ensure the correctness of the data.
    """)

    st.markdown('#### 4. Data Accountability ')
    st.markdown("""
    The stock data was collected from [Yahoo! Finance](https://finance.yahoo.com/), which is an online source well regarded for it's reliability and integrity. Similarly, Covid related data was taken from the official (CDC)[https://data.cdc.gov] website.
    Also, as noted earlier, no modifications were made to the raw data to ensure that we don't color the subsequent analysis and inferences.
    """)
    
 
if __name__ == "__main__":
    dataset()