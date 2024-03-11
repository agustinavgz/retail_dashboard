import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import plotly.graph_objects as go
from app_plots import *

months_dict = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

st.set_page_config(
    page_title="Retail Dashboard",
    page_icon="cbox.png",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

payments_data = pd.read_csv('payments_dataset.csv')
camera_data = pd.read_csv('camera_dataset.csv')

with st.sidebar:
    st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 200px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
    )
    st.title(':bar_chart: Retail Dashboard')
    
    year_list = list(payments_data.Year.unique())[::-1]
    
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    df_selected_year = payments_data[payments_data.Year == selected_year]
    df_selected_year_sorted = df_selected_year#.sort_values()#by="population", ascending=False)

    month_list = list(months_dict.values())

    selected_month_string = st.selectbox('Select a month', month_list, index=len(month_list)-1)
    selected_month = [key for key, value in months_dict.items() if value == selected_month_string][0]

    # month_list = list(df_selected_year.Month.unique())[::-1]
    # selected_month = st.selectbox('Select a month', month_list, index=len(month_list)-1)

col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    df_year_agg, df_month_agg = get_agg(camera_data, payments_data)
    # st.markdown('#### Gains/Losses')
    df_cr = calculate_difference(df_month_agg, selected_year, 'ConversionRate', selected_month)
    cr_value = df_cr['ConversionRate'].values[0]
    cr_delta = round(df_cr['difference'].values[0],3)
    st.metric(label=f'Conversion Rate', value=f'{cr_value}%', delta=cr_delta)

    df_occ = calculate_difference(df_month_agg, selected_year, 'Occupation', selected_month)
    occ_value = round(df_occ['Occupation'].values[0]/1000,3)
    occ_delta = round(df_occ['difference'].values[0]/1000,3)
    st.metric(label=f'Occupation', value=f'{occ_value}k', delta=occ_delta)

    df_occ_time = calculate_difference(df_month_agg, selected_year, 'OccupationTime', selected_month)
    occ_time_value = df_occ_time['OccupationTime'].values[0]
    occ_time_delta = round(df_occ_time['difference'].values[0],3)
    st.metric(label=f'Avg Occupation Time', value=f'{occ_time_value}m', delta=occ_time_delta)

    st.write()
    fig = percentage_per_paymentm(payments_data, selected_year, selected_month)
    st.plotly_chart(fig, use_container_width=True)


with col[1]:
    fig = get_profit_per_year(payments_data, selected_year)
    st.plotly_chart(fig, use_container_width=True)
    fig2 = get_profit_per_cat(payments_data, selected_year, selected_month)
    st.plotly_chart(fig2, use_container_width=True)

    
with col[2]:
    fig = get_amount_per_month(payments_data, selected_year, selected_month)
    st.plotly_chart(fig, use_container_width=False)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.image('heatmap.jpeg', caption='Heatmap of the store', 
             width=400)


