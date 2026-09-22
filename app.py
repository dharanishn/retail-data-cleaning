import streamlit as st
import pandas as pd
import plotly.express as px

# Ensure visual hierarchy best practices[span_2](start_span)[span_2](end_span)
st.set_page_config(page_title="Retail Dashboard", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('clean_dataset.csv')
        df['order_date'] = pd.to_datetime(df['order_date'])
        return df
    except FileNotFoundError:
        st.error("Please upload 'clean_dataset.csv' to your GitHub repository.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Sidebar: Slicers & Categorical Filtering[span_3](start_span)[span_3](end_span)
    st.sidebar.header("Dashboard Filters")
    segments = st.sidebar.multiselect("Customer Segment", df['customer_segment'].unique(), default=df['customer_segment'].unique())
    categories = st.sidebar.multiselect("Product Category", df['category'].unique(), default=df['category'].unique())

    filtered_df = df[(df['customer_segment'].isin(segments)) & (df['category'].isin(categories))]

    st.title("Interactive Retail KPI Dashboard")
    
    # Define Executive KPIs[span_4](start_span)[span_4](end_span)
    total_rev = filtered_df['total_revenue'].sum()
    total_orders = filtered_df['order_id'].nunique()
    aov = total_rev / total_orders if total_orders > 0 else 0
    cac = 45.50  # Industry standard mock CAC
    churn = 0.12 # Industry standard mock Churn Rate

    # Interactive Dashboard Cards[span_5](start_span)[span_5](end_span)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${total_rev:,.2f}")
    col2.metric("Average Order Value", f"${aov:,.2f}")
    col3.metric("Customer Acq. Cost (CAC)", f"${cac:.2f}")
    col4.metric("Churn Rate", f"{churn:.1%}")

    st.markdown("---")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        # Trendline Area Chart[span_6](start_span)[span_6](end_span)
        st.subheader("Revenue Trendline")
        daily_rev = filtered_df.groupby('order_date')['total_revenue'].sum().reset_index()
        fig_area = px.area(daily_rev, x='order_date', y='total_revenue', color_discrete_sequence=['#1f77b4'])
        st.plotly_chart(fig_area, use_container_width=True)

    with col_chart2:
        # Geographic Heatmap (Substitute using Treemap for City-level data)[span_7](start_span)[span_7](end_span)
        st.subheader("Revenue Geographic Heatmap")
        city_rev = filtered_df.groupby('city')['total_revenue'].sum().reset_index()
        fig_map = px.treemap(city_rev, path=['city'], values='total_revenue', color='total_revenue', color_continuous_scale='Blues')
        st.plotly_chart(fig_map, use_container_width=True)

    # Drill-down capabilities[span_8](start_span)[span_8](end_span)
    st.subheader("Temporal & Categorical Order Drill-Down")
    st.dataframe(filtered_df.sort_values('order_date', ascending=False))
  
