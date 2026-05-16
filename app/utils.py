import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv('data/campaigns.csv', parse_dates=['date'])
    return df

def filter_data(df, start_date, end_date, channels, regions):
    mask = (
        (df['date'] >= pd.Timestamp(start_date)) &
        (df['date'] <= pd.Timestamp(end_date)) &
        (df['channel'].isin(channels)) &
        (df['region'].isin(regions))
    )
    return df[mask]

def calculate_kpis(df):
    total_spend = df['spend'].sum()
    total_revenue = df['revenue'].sum()
    total_leads = df['leads'].sum()
    return {
        'total_spend': round(total_spend, 2),
        'total_revenue': round(total_revenue, 2),
        'roas': round(total_revenue / total_spend, 2) if total_spend > 0 else 0,
        'total_mqls': int(df['MQLs'].sum()),
        'cpl': round(total_spend / total_leads, 2) if total_leads > 0 else 0,
        'total_conversions': int(df['conversions'].sum())
    }
