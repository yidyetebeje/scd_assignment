import pandas as pd
import numpy as np
import streamlit as st
import Preprocessor
import time

st.set_page_config(page_title="Sales Dashboard", page_icon='./donut-chart.ico', layout='wide')
# Reading the data
df = pd.read_csv("data.csv")

# Creatiing time features
df = Preprocessor.fetch_time_features(df)

# sidebar
st.sidebar.title("Filters")

selected_year = Preprocessor.multiselect('Select Year', df['Financial_Year'].unique())

selected_retailer = Preprocessor.multiselect('Select Retailer', df['Retailer'].unique())

selected_company = Preprocessor.multiselect('Select Company', df['Company'].unique())

selected_month = Preprocessor.multiselect('Select Month', df['Financial_Month'].unique())

selected_chart = st.sidebar.radio('Select Chart Type',['Line Chart','Area Chart','Bar Chart'])

if (len(selected_company) == 0 or len(selected_year) == 0 or len(selected_month)==0 or len(selected_retailer)==0):
    st.error('Please provide all available inputs!')

else:

    filtered_df = df[(df['Financial_Year'].isin(selected_year)& df['Retailer'].isin(selected_retailer) & df['Company'].isin(selected_company) & df['Financial_Month'].isin(selected_month))]

    st.title('Sales Dashboard')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label= 'Total Sales', value= int(filtered_df['Amount'].sum()))
    with col2:
        st.metric(label= 'Total Margin', value= int(filtered_df['Margin'].sum()))
    with col3:
        st.metric(label= 'Total Transactions', value= len(filtered_df['Margin']))
    with col4:
        st.metric(label= 'Margin Percentage (in %)', value= int((filtered_df['Margin'].sum()/filtered_df['Amount'].sum())*100))

    yearly_sales = filtered_df[['Financial_Year', 'Financial_Month','Amount']].groupby(['Financial_Year', 'Financial_Month']).sum().reset_index().pivot(index = 'Financial_Month', columns = 'Financial_Year', values = 'Amount')

    if selected_chart== 'Line Chart':
        st.line_chart(yearly_sales, x_label = 'Financial Month', y_label= 'Total Sales')
        st.toast("Here's your Line Chart!", icon="\U0001F60D")
        time.sleep(.1)
    elif selected_chart== 'Area Chart':
        st.area_chart(yearly_sales, x_label = 'Financial Month', y_label= 'Total Sales')
        st.toast("Here's your Area Chart!", icon="🥳")
        time.sleep(.1)
    elif selected_chart== 'Bar Chart':
        st.bar_chart(yearly_sales, x_label = 'Financial Month', y_label= 'Total Sales')
        st.toast("Here's your Bar Chart!", icon="🤔")
        time.sleep(.1)

    col5, col6 = st.columns(2)

    with col5:
        st.title('Retailers by Revenue %')
        retailer_count = Preprocessor.fetch_top_revenue_retailers(filtered_df)
        retailer_count.set_index('Percentage Revenue', inplace=True)
        st.bar_chart(retailer_count,x_label='Percentage Revenue', y_label='Retailer Count')    
    with col6:
        st.title('Companies by Revenue %')
        retailer_count = Preprocessor.fetch_top_revenue_companies(filtered_df)
        retailer_count.set_index('Percentage Revenue', inplace=True)
        st.bar_chart(retailer_count,x_label='Percentage Revenue', y_label='Company Count')    


footer="""<style>
a:link , a:visited{
color: red;
background-color: transparent;
text-decoration: solid;
height : 18px
}

a:hover,  a:active {
color: blue;
background-color: transparent;
text-decoration: solid;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Sales_Dashboard <a style='display: block; text-align: center;' href="https://www.linkedin.com/in/dattasnehendu/" target="_blank"></a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)