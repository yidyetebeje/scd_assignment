import pandas as pd
import streamlit as st
# Fetching the date features
def fetch_time_features(df):
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    # Financial month
    month_dict = {4:1,5:2,6:3,7:4,8:5,9:6,10:7,11:8,12:9,1:10,2:11,3:12}
    df["Financial_Month"] = df["Month"].map(month_dict)
    # Financial year
    df["Financial_Year"] = df.apply(lambda x: f"{x["Year"]} - {x["Year"]+1}" if x["Month"]>=4 else f"{x["Year"]-1} - {x["Year"]}", axis = 1)
    return df

def multiselect(title, options_list):
    selected = st.sidebar.multiselect(title, options_list)
    select_all = st.sidebar.checkbox('Select All', value = True, key = title)
    if select_all:
        selected_options = options_list
    else: 
        selected_options = selected
    return selected_options

def fetch_top_revenue_retailers(df):
    retailers_revenue = df[['Retailer','Amount']].groupby('Retailer').sum().reset_index().sort_values(by='Amount', ascending=False)
    total_revenue = retailers_revenue['Amount'].sum()
    percentage = [100,90,80,70,60,50,40,30,20,10]
    retailer_count = []

    for i in percentage:
        target_revenue = 0.01 * i * total_revenue
        loop = 1
        while loop<=len(retailers_revenue) and retailers_revenue.iloc[:loop,1].sum()<=target_revenue:
            loop +=1
        retailer_count.append(loop)
    retailers = pd.DataFrame(data={'Percentage Revenue': percentage, 'Retailer Count' : retailer_count})

    return retailers

def fetch_top_revenue_companies(df):
    companies_revenue = df[['Company','Amount']].groupby('Company').sum().reset_index().sort_values(by='Amount', ascending=False)
    total_revenue = companies_revenue['Amount'].sum()
    percentage = [100,90,80,70,60,50,40,30,20,10]
    company_count = []

    for i in percentage:
        target_revenue = 0.01 * i * total_revenue
        loop = 1

        while loop<=len(companies_revenue) and companies_revenue.iloc[:loop,1].sum()<=target_revenue:
            loop +=1
        company_count.append(loop)
    companies = pd.DataFrame(data={'Percentage Revenue': percentage, 'Company Count' : company_count})

    return companies