import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# Set page config
st.set_page_config(page_title="Wealth Growth Analysis", layout="wide")

# Create the data
data = {
    'Date': [
        # 2022
        '2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01', '2022-06-01',
        '2022-07-01', '2022-08-01', '2022-09-01', '2022-10-01', '2022-11-01', '2022-12-01',
        # 2023
        '2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01', '2023-06-01',
        '2023-07-01', '2023-08-01', '2023-09-01', '2023-10-01', '2023-11-01', '2023-12-01',
        # 2024
        '2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01', '2024-06-01',
        '2024-07-01', '2024-08-01', '2024-09-01', '2024-10-01'
    ],
    'Wealth': [
        # 2022
        6433.58, 8723.75, 10523.75, 13403.21, 14918.87, 15703.09,
        17634.65, 19378.63, 19811.92, 21196.34, 21245.29, 20169.40,
        # 2023
        24133.65, 25701.00, 27163.20, 30203.87, 31421.26, 32454.36,
        33763.75, 35879.15, 38059.47, 41101.12, 44492.48, 50422.58,
        # 2024
        55240.27, 62480.65, 71089.29, 74834.25, 79675.65, 82596.85,
        86737.92, 83915.65, 90446.03, 98554.79
    ]
}

# Create DataFrame
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

# Calculate projections for Nov and Dec 2024
last_6_months = df.tail(6)
average_growth = last_6_months['Wealth'].diff().mean()

projected_dates = pd.date_range(start='2024-11-01', end='2024-12-01', freq='MS')
projected_wealth = [
    df['Wealth'].iloc[-1] + average_growth,
    df['Wealth'].iloc[-1] + (average_growth * 2)
]

projection_df = pd.DataFrame({
    'Date': projected_dates,
    'Wealth': projected_wealth
})

# Combine actual and projected data
full_df = pd.concat([df, projection_df])
full_df['Type'] = ['Actual'] * len(df) + ['Projected'] * len(projection_df)

# Create the Streamlit app
st.title("Wealth Growth Analysis Dashboard")

# Add description
st.markdown("""
This dashboard shows the wealth growth from January 2022 to December 2024,
with projections for November and December 2024 based on recent trends.
""")

# Create tabs
tab1, tab2 = st.tabs(["📈 Visualization", "📊 Data Analysis"])

with tab1:
    # Main chart
    fig = px.line(full_df,
                  x='Date',
                  y='Wealth',
                  color='Type',
                  title='Wealth Growth Over Time',
                  labels={'Wealth': 'Wealth ($)', 'Date': 'Date'},
                  template='plotly_white')

    fig.update_traces(line=dict(width=2))
    fig.update_layout(
        hovermode='x unified',
        yaxis_tickprefix='$',
        yaxis_tickformat=',.2f',
        legend_title_text=''
    )

    st.plotly_chart(fig, use_container_width=True)

    # Key metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Current Wealth",
            f"${df['Wealth'].iloc[-1]:,.2f}",
            f"{(df['Wealth'].iloc[-1] - df['Wealth'].iloc[-2]):,.2f}"
        )

    with col2:
        projected_nov = projected_wealth[0]
        st.metric(
            "Projected November 2024",
            f"${projected_nov:,.2f}",
            f"{(projected_nov - df['Wealth'].iloc[-1]):,.2f}"
        )

    with col3:
        projected_dec = projected_wealth[1]
        st.metric(
            "Projected December 2024",
            f"${projected_dec:,.2f}",
            f"{(projected_dec - projected_nov):,.2f}"
        )

with tab2:
    # Yearly statistics
    st.subheader("Yearly Statistics")

    yearly_stats = df.set_index('Date').resample('Y')['Wealth'].agg([
        ('Average', 'mean'),
        ('Minimum', 'min'),
        ('Maximum', 'max'),
        ('Growth', lambda x: x.iloc[-1] - x.iloc[0])
    ]).round(2)

    yearly_stats.index = yearly_stats.index.year
    st.dataframe(yearly_stats.style.format("${:,.2f}"))

    # Monthly growth rates
    st.subheader("Recent Monthly Growth Rates")

    monthly_growth = df.set_index('Date')['Wealth'].pct_change() * 100
    recent_growth = monthly_growth.tail(6)

    fig_growth = px.bar(
        recent_growth,
        title='Last 6 Months Growth Rate (%)',
        labels={'value': 'Growth Rate (%)', 'Date': 'Month'}
    )

    st.plotly_chart(fig_growth, use_container_width=True)

# Add download capability
st.download_button(
    label="Download Data as CSV",
    data=full_df.to_csv(index=False).encode('utf-8'),
    file_name='wealth_data.csv',
    mime='text/csv'
)