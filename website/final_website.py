import streamlit as st
import hydralit_components as hc
import datetime
import game
import stock_tab
import dataset
import covid_and_vaccine_visualisations

#make it look nice from the start
st.set_page_config(layout='wide',initial_sidebar_state='collapsed')

# specify the primary menu definition
menu_data = [
    {'id':'home','icon': "far fa-home", 'label':"Home"},
    {'id':'dataset','icon':"fas fa-table",'label':"Dataset"},
    {'id':'visualization','icon':"fas fa-chart-bar",'label':"Visualizations"},
    {'id':'game','icon':"fas fa-gamepad",'label':"Game"},
    {'icon': "fas fa-caret-down",'label':"Visualizations", 'submenu':[{'id':'vacc','icon': "fa fa-paperclip", 'label':"Covid and Vaccines"},{'id':'stock','icon': "💀", 'label':"Impact on Stock Market"},{'id':'subid13','icon': "fa fa-database", 'label':"Sub-item 3"}]},
    # {'icon': "far fa-chart-bar", 'label':"Chart"},#no tooltip message
    # {'id':' Crazy return value 💀','icon': "💀", 'label':"Calendar"},
    # {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"} #can add a tooltip message
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

# if st.button('click me'):
#   st.info('You clicked at: {}'.format(datetime.datetime.now()))


# if st.sidebar.button('click me too'):
#   st.info('You clicked at: {}'.format(datetime.datetime.now()))
# #get the id of the menu item clicked

if menu_id ==  'game':
    game.init_game()
elif menu_id ==  'stock':
    stock_tab.stock_tab_main()
elif menu_id ==  'dataset':
    dataset.dataset()
elif menu_id ==  'vacc':
    covid_and_vaccine_visualisations.covid_and_vaccine_visualisations()