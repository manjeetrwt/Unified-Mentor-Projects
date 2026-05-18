import os
import pandas as pd
import streamlit as st
import plotly.express as px

# Set up page layout to use your minimalist aesthetic preference
st.set_page_config(page_title="APL Logistics Margin Intelligence", layout="wide")

# STEP 0: LOAD DATASETS DYNAMICALLY

APP_DIR = os.path.dirname(os.path.abspath(__file__))
CLEANED_DATA_PATH = os.path.abspath(os.path.join(APP_DIR, "..", "data", "APL_Logistics_Cleaned.csv"))
SEGMENTED_DATA_PATH = os.path.abspath(os.path.join(APP_DIR, "..", "data", "APL_Logistics_Segmented.csv"))

@st.cache_data
def load_data():
    df_clean = pd.read_csv(CLEANED_DATA_PATH)
    df_ml = pd.read_csv(SEGMENTED_DATA_PATH)
    return df_clean, df_ml

df, df_customer = load_data()


# STEP 1: SIDEBAR INTERACTIVE FILTERS

st.sidebar.header("Filter Workspace")

# Market Filter
all_markets = sorted(df['Market'].unique())
selected_markets = st.sidebar.multiselect("Select Global Markets", all_markets, default=all_markets)

# Customer Segment Filter
all_segments = sorted(df['Customer Segment'].unique())
selected_segments = st.sidebar.multiselect("Select Customer Segments", all_segments, default=all_segments)

# Apply global sidebar filters to the core transactions dataframe
filtered_df = df[
    (df['Market'].isin(selected_markets)) & 
    (df['Customer Segment'].isin(selected_segments))
]

# STEP 2: APP HEADER UI

st.title("APL Logistics Commercial Intelligence Platform")
st.markdown("Shift operations from volume-focused execution to margin-optimized profitability analytics.")
st.write("---")


# STEP 3: INTERACTIVE TABS LAYOUT

tab1, tab2, tab3 = st.tabs([
    "Executive Overview", 
    "Machine Learning Customer Value", 
    "Product & Discount Optimization"
])


# TAB 1: EXECUTIVE OVERVIEW

with tab1:
    st.subheader("Global Supply Chain Financial Performance")
    
    # Calculate filtered KPIs
    rev = filtered_df['Sales'].sum()
    prof = filtered_df['Order Profit Per Order'].sum()
    margin = (prof / rev) * 100 if rev > 0 else 0
    
    # Layout simple, crisp KPI Metrics Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${rev:,.2f}")
    col2.metric("Net Operational Profit", f"${prof:,.2f}")
    col3.metric("Net Profit Margin (%)", f"{margin:.2f}%")
    
    st.write("---")
    
    # Market Profitability Map Chart
    st.subheader("Regional Margin Contributions")
    market_chart_df = filtered_df.groupby('Market').agg(
        Revenue=('Sales', 'sum'),
        Profit=('Order Profit Per Order', 'sum')
    ).reset_index()
    market_chart_df['Margin_%'] = (market_chart_df['Profit'] / market_chart_df['Revenue']) * 100
    
    fig_market = px.bar(
        market_chart_df, x='Market', y='Revenue', color='Margin_%',
        title="Revenue vs Margin Contributions by Market Segment",
        color_continuous_scale="RdYlGn", text_auto='.2s'
    )
    fig_market.update_layout(template="simple_white")
    st.plotly_chart(fig_market, use_container_width=True)


# TAB 2: ML CUSTOMER VALUE SEGMENATION

with tab2:
    st.subheader("Data-Driven Strategic Clustering (K-Means)")
    st.markdown("Algorithmic customer groupings trained on cumulative revenue and real profitability margins.")
    
    # Filter ML Data based on chosen segments
    filtered_customer = df_customer[df_customer['Customer Segment'].isin(selected_segments)]
    
    # Plotly Scatter Plot displaying the ML Clusters clearly
    fig_scatter = px.scatter(
        filtered_customer, x='Total_Sales', y='Total_Profit', 
        color='Customer_Value_Tier', hover_data=['Customer_Name'],
        title="Algorithmic Customer Boundaries (Sales vs Net Profit Matrix)",
        labels={'Total_Sales': 'Total Historical Sales ($)', 'Total_Profit': 'Total Historical Profit ($)'},
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_scatter.update_traces(marker=dict(size=8, opacity=0.7))
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Customer breakdown table
    st.subheader("High-Risk / Value-Eroding Accounts Detail")
    value_eroding_list = filtered_customer[
        filtered_customer['Customer_Value_Tier'].str.contains("Tier 4")
    ].sort_values(by='Total_Profit').head(10)
    
    st.dataframe(
        value_eroding_list[['Customer Id', 'Customer_Name', 'Total_Sales', 'Total_Profit', 'Order_Count']],
        use_container_width=True, hide_index=True
    )


# TAB 3: PRODUCT & DISCOUNT OPTIMIZATION
with tab3:
    st.subheader("Discount Risk & Profit Leak Diagnostics")
    
    # Category Performance Analyzer
    cat_df = filtered_df.groupby('Category Name').agg(
        Sales=('Sales', 'sum'),
        Profit=('Order Profit Per Order', 'sum')
    ).reset_index()
    cat_df['Margin_%'] = (cat_df['Profit'] / cat_df['Sales']) * 100
    
    fig_cat = px.bar(
        cat_df.sort_values(by='Margin_%'), x='Margin_%', y='Category Name', orientation='h',
        title="Category Profit Margin Ranking (%)",
        color='Margin_%', color_continuous_scale="RdYlGn"
    )
    st.plotly_chart(fig_cat, use_container_width=True)
    
    # What-If Simulation Tool Section
    st.write("---")
    st.subheader("Simulation Engine: Promotional Cap Constraints")
    st.markdown("Model how restricting high discount permissions protects corporate bottom lines.")
    
    # Dynamic Slider for User Capabilities
    discount_slider = st.slider("Set Maximum Corporate Discount Threshold Allowed", 0.0, 0.25, 0.25, step=0.01)
    
    # Simulate Capping the Discount
    simulated_df = filtered_df.copy()
    # Mask to find orders that exceed the user's slider constraint
    exceed_mask = simulated_df['Order Item Discount Rate'] > discount_slider
    
    # If capped, the new discount becomes the cap value, and we recover the lost profit
    # Recalculate order item total and add the difference directly back to profit
    original_discount = simulated_df.loc[exceed_mask, 'Order Item Discount']
    new_discount = simulated_df.loc[exceed_mask, 'Order Item Product Price'] * simulated_df.loc[exceed_mask, 'Order Item Quantity'] * discount_slider
    recovered_cash = original_discount - new_discount
    
    simulated_profit = prof + recovered_cash.sum()
    profit_increase = simulated_profit - prof
    
    # Display simulation output to user using crisp layout metrics
    sim_col1, sim_col2 = st.columns(2)
    sim_col1.metric("Simulated Net Profit", f"${simulated_profit:,.2f}", delta=f"+${profit_increase:,.2f} Recovered")
    sim_col2.metric("Simulated Margin Growth", f"{((simulated_profit / rev) * 100):.2f}%", delta=f"{(((simulated_profit / rev) * 100) - margin):+.2f}% Margin Shift")