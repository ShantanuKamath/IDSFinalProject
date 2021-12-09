import streamlit as st
import hydralit_components as hc
import datetime
import game
import stock_tab
import dataset
import covid_visualisations
import vaccine_visualisations
import home

#make it look nice from the start
st.set_page_config(layout='wide',initial_sidebar_state='collapsed')

# specify the primary menu definition
menu_data = [
    {'id':'home','icon': "fas fa-home", 'label':"Home"},
    {'id':'dataset','icon':"fas fa-table",'label':"Dataset"},
    {'icon': "fas fa-chart-bar",'label':"Visualizations", 'submenu':[{'id':'covid','icon': "fas fa-virus", 'label':"Covid Cases"},{'id':'vaccine','icon': "fas fa-syringe", 'label':"Vaccine Distribution"},{'id':'stock','icon': "fas fa-chart-line", 'label':"Impact on Stock Market"}]},
    {'id':'game','icon':"fas fa-gamepad",'label':"Game"},
]

over_theme = {'txc_inactive': '#FFFFFF'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    # home_name='home',
    # login_name='Logout',
    hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)

if menu_id ==  'game':
    game.init_game()
elif menu_id ==  'stock':
    stock_tab.stock_tab_main()
elif menu_id ==  'dataset':
    dataset.dataset()
elif menu_id ==  'covid':
    covid_visualisations.covid_visualisations()
elif menu_id ==  'vaccine':
    vaccine_visualisations.vaccine_visualisations()
elif menu_id ==  'home':
    home.home()