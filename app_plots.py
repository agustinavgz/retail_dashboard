import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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

def get_amount_per_month(df, year, month):
    lineQuantity = df[(df['Year'] == year)&(df['Month'] == month)]
    quantity_per_day = lineQuantity.groupby('Order_date')['Amount'].sum().reset_index()
    fig_quantity = px.line(
        quantity_per_day, 
        x='Order_date', 
        y='Amount', 
        title='Amount Sold over the selected Month'
    )
    fig_quantity.update_layout(
        margin_r=100,
        width=450,
        height=350,
    )
    return fig_quantity

def get_profit_per_year(df, year):
    # Quantity for each day
    chosen_year = df[df['Year'] == year]
    amount_per_month = chosen_year.groupby('Month')['Profit'].sum().reset_index()

    # Create a line chart for Quantity over the last month using Plotly
    fig_quantity = px.bar(
        amount_per_month, 
        text_auto='.2s',
        x='Month', 
        y='Profit', 
        title='Profit over the year'
    )
    fig_quantity.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig_quantity.update_layout(
        margin_r=100,
        width=650,
        height=400,
        margin = dict(t=50, l=25, r=25, b=25)
    )
    return fig_quantity

def percentage_per_paymentm(df, year, month):
    chosen_year = df[(df['Year'] == year)&(df['Month'] == month)]
    values = chosen_year.groupby('PaymentMethod').count().iloc[:,0].values
    labels = chosen_year.groupby('PaymentMethod').count().index.tolist()

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)],
                    layout=go.Layout(
                        autosize=False,
                        width=350,
                        height=350,
                        title='Payment Methods'))
    # fig.show()
    return fig

def get_profit_per_cat(df, year, month):
    chosen_year = df[(df['Year'] == year)&(df['Month'] == month)]
    amount_per_month = chosen_year.groupby('ProductCategory')['Profit'].sum().reset_index()
    fig_quantity = px.bar(
        amount_per_month, 
        x='Profit', 
        y='ProductCategory', 
        orientation='h', 
        color='Profit',
        title='Profit over the Product Categories'
    )
    fig_quantity.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig_quantity.update_layout(
        margin_r=100,
        width=650,
        height=400,
        margin = dict(t=50, l=25, r=25, b=25)
    )
    return fig_quantity

def get_agg(camera_df, superSales):
    # agregate by year
    people_per_year = camera_df.groupby(['Year', 'DetectionID'])['NumPeople'].sum().reset_index()
    total_people_per_year = people_per_year.groupby('Year')['NumPeople'].sum().reset_index()
    sales_per_year = superSales.groupby('Year')['TransactionID'].count().reset_index()
    occ_year = camera_df.groupby(['Year', 'DetectionID'])['OccupationTime'].mean().reset_index()
    occ_year = occ_year.groupby('Year')['OccupationTime'].mean().reset_index()
    df_year_agg = pd.merge(total_people_per_year, sales_per_year, on='Year')
    df_year_agg = pd.merge(df_year_agg, occ_year, on='Year')
    df_year_agg['ConversionRate'] = (df_year_agg['TransactionID']/df_year_agg['NumPeople'])*100
    df_year_agg['ConversionRate'] = df_year_agg['ConversionRate'].round(2)
    df_year_agg['OccupationTime'] = df_year_agg['OccupationTime'].round(2)
    df_year_agg = df_year_agg.rename(columns={'NumPeople':'Occupation', 'TransactionID':'Sells'})
    # agregate by month
    people_per_year = camera_df.groupby(['Year', 'Month','DetectionID'])['NumPeople'].sum().reset_index()
    total_people_per_year = people_per_year.groupby(['Year','Month'])['NumPeople'].sum().reset_index()
    sales_per_year = superSales.groupby(['Year','Month'])['TransactionID'].count().reset_index()
    occ_year = camera_df.groupby(['Year', 'Month', 'DetectionID'])['OccupationTime'].mean().reset_index()
    occ_year = occ_year.groupby(['Year', 'Month'])['OccupationTime'].mean().reset_index()
    df_month_agg = pd.merge(total_people_per_year, occ_year, on=['Year','Month'])
    df_month_agg = pd.merge(df_month_agg, sales_per_year, on=['Year','Month'])
    df_month_agg['ConversionRate'] = (df_month_agg['TransactionID']/df_month_agg['NumPeople'])*100
    df_month_agg['ConversionRate'] = df_month_agg['ConversionRate'].round(2)
    df_month_agg['OccupationTime'] = df_month_agg['OccupationTime'].round(2)
    df_month_agg = df_month_agg.rename(columns={'NumPeople':'Occupation', 'TransactionID':'Sells'})
    return df_year_agg, df_month_agg

def calculate_difference(input_df, year, col, month=None):
    if month:
        selected_data = input_df[(input_df['Year'] == year)&(input_df['Month'] == month)].reset_index()
        previous_data = input_df[(input_df['Year'] == year)&(input_df['Month'] == month-1)].reset_index()
        cols = ['Year','Month',col, 'difference']
    else:
        selected_data = input_df[(input_df['Year'] == year)].reset_index()
        previous_data = input_df[(input_df['Year'] == year-1)].reset_index()
        cols = ['Year',col, 'difference']
    selected_data['difference'] = selected_data[col].sub(previous_data[col], fill_value=0)
    return selected_data[cols]