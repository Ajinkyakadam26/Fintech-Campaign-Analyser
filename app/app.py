import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, filter_data, calculate_kpis

# ─── Page Config ───────────────────────────────
st.set_page_config(
    page_title="NovaPay Campaign Analyser",
    page_icon="💳",
    layout="wide"
)

# ─── Load Data ─────────────────────────────────
df = load_data()

# ─── Sidebar Filters ───────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/bank-card-front-side.png", width=60)
st.sidebar.title("NovaPay Analytics")
st.sidebar.markdown("---")

start_date = st.sidebar.date_input("Start Date", df['date'].min())
end_date = st.sidebar.date_input("End Date", df['date'].max())

channels = st.sidebar.multiselect(
    "Channel",
    options=df['channel'].unique().tolist(),
    default=df['channel'].unique().tolist()
)

regions = st.sidebar.multiselect(
    "Region",
    options=df['region'].unique().tolist(),
    default=df['region'].unique().tolist()
)

# ─── Filter Data ───────────────────────────────
filtered = filter_data(df, start_date, end_date, channels, regions)

# ─── Title ─────────────────────────────────────
st.title("💳 NovaPay — Campaign Analytics Dashboard")
st.markdown("Tracking MQL, CPL, ROAS and Funnel Performance across 500K+ campaigns")
st.markdown("---")

# ─── KPI Cards ─────────────────────────────────
kpis = calculate_kpis(filtered)
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("💰 Total Spend", f"₹{kpis['total_spend']:,.0f}")
k2.metric("📈 Total Revenue", f"₹{kpis['total_revenue']:,.0f}")
k3.metric("🚀 ROAS", f"{kpis['roas']:.2f}x")
k4.metric("🎯 Total MQLs", f"{kpis['total_mqls']:,}")
k5.metric("💡 CPL", f"₹{kpis['cpl']:,.0f}")
st.markdown("---")

# ─── Funnel Chart ──────────────────────────────
st.subheader("📉 Campaign Funnel")
funnel_data = dict(
    number=[
        filtered['impressions'].sum(),
        filtered['clicks'].sum(),
        filtered['leads'].sum(),
        filtered['MQLs'].sum(),
        filtered['SQLs'].sum(),
        filtered['conversions'].sum()
    ],
    stage=["Impressions", "Clicks", "Leads", "MQLs", "SQLs", "Conversions"]
)
fig_funnel = go.Figure(go.Funnel(
    y=funnel_data['stage'],
    x=funnel_data['number'],
    textinfo="value+percent initial",
    marker=dict(color=["#4361ee","#3a86ff","#48cae4","#52b788","#f77f00","#e63946"])
))
fig_funnel.update_layout(height=400)
st.plotly_chart(fig_funnel, use_container_width=True)
st.markdown("---")

# ─── MoM Trend Line ────────────────────────────
st.subheader("📆 Month-over-Month Trends")
monthly = filtered.copy()
monthly['month'] = monthly['date'].dt.to_period('M').astype(str)
monthly_grp = monthly.groupby('month').agg(
    ROAS=('revenue', 'sum'),
    Spend=('spend', 'sum'),
    MQLs=('MQLs', 'sum'),
    CPL=('spend', 'sum')
).reset_index()
monthly_grp['ROAS'] = (monthly_grp['ROAS'] / monthly_grp['Spend']).round(2)
monthly_grp['CPL'] = (monthly_grp['CPL'] / filtered.groupby(
    filtered['date'].dt.to_period('M').astype(str))['leads'].sum().values).round(2)

fig_trend = px.line(
    monthly_grp, x='month',
    y=['ROAS', 'MQLs'],
    markers=True,
    color_discrete_sequence=["#4361ee", "#f77f00"]
)
fig_trend.update_layout(height=350)
st.plotly_chart(fig_trend, use_container_width=True)
st.markdown("---")

# ─── Channel Bar Chart ─────────────────────────
st.subheader("📊 Performance by Channel")
channel_grp = filtered.groupby('channel').agg(
    ROAS=('revenue', 'sum'),
    Spend=('spend', 'sum'),
    MQLs=('MQLs', 'sum')
).reset_index()
channel_grp['ROAS'] = (channel_grp['ROAS'] / channel_grp['Spend']).round(2)
fig_bar = px.bar(
    channel_grp, x='channel', y='ROAS',
    color='channel', text='ROAS',
    color_discrete_sequence=px.colors.qualitative.Bold
)
fig_bar.update_layout(height=350, showlegend=False)
st.plotly_chart(fig_bar, use_container_width=True)
st.markdown("---")

# ─── Top 10 Campaigns Table ────────────────────
st.subheader("🏆 Top 10 Campaigns by ROAS")
top10 = filtered.groupby(['campaign_id','campaign_name','channel','region']).agg(
    Spend=('spend','sum'),
    Revenue=('revenue','sum'),
    Conversions=('conversions','sum')
).reset_index()
top10['ROAS'] = (top10['Revenue'] / top10['Spend']).round(2)
top10 = top10.sort_values('ROAS', ascending=False).head(10)
st.dataframe(top10.reset_index(drop=True), use_container_width=True)
st.markdown("---")

# ─── Region x Channel Heatmap ──────────────────
st.subheader("🗺️ Region × Channel ROAS Heatmap")
heat = filtered.groupby(['region','channel']).agg(
    Revenue=('revenue','sum'),
    Spend=('spend','sum')
).reset_index()
heat['ROAS'] = (heat['Revenue'] / heat['Spend']).round(2)
heat_pivot = heat.pivot(index='region', columns='channel', values='ROAS')
fig_heat = px.imshow(
    heat_pivot,
    color_continuous_scale='RdYlGn',
    text_auto=True,
    aspect='auto'
)
fig_heat.update_layout(height=400)
st.plotly_chart(fig_heat, use_container_width=True)