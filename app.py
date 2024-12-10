import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(page_title="Flood Prediction", page_icon="🌊", layout="wide")

# Add custom CSS to hide the GitHub icon specifically
hide_github_icon_css = """
<style>
    /* Hide the GitHub icon */
    .stToolbarActionButton[data-testid="stToolbarActionButton"] {
        display: none;
    }
</style>
"""
st.markdown(hide_github_icon_css, unsafe_allow_html=True)

# App description - Explain functionalities in an expander box
with st.expander('About this app'):
    st.markdown('**What can this app do?**')
    st.info('This app provides insights into rainfall data for different states and helps predict flood risks using historical rainfall data.')
    st.markdown('**How to use the app?**')
    st.warning(
        '1. Select a state and a specific month from the sidebar to view rainfall trends.\n'
        '2. Choose a period to analyze cumulative rainfall across the years.\n'
        '3. Explore interactive charts for trends and averages in the Rainfall Charts tab.'
    )

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data/rainfall.csv")

data = load_data()

# Sidebar for user input
st.sidebar.title("Flood Prediction")
state = st.sidebar.selectbox("Select State", data['SUBDIVISION'].unique())
month = st.sidebar.selectbox("Select Month", data.columns[2:14])  # Skip 'SUBDIVISION' and 'YEAR'

# Period selection
period = st.sidebar.radio(
    "Select Period", ["Annual", "Jan-Feb", "Mar-May", "Jun-Sep", "Oct-Dec"]
)

# Define columns for each period
period_columns = {
    "Annual": data.iloc[:, 2:14].sum(axis=1),  # All months
    "Jan-Feb": data.iloc[:, 2:4].sum(axis=1),  # Jan, Feb
    "Mar-May": data.iloc[:, 4:7].sum(axis=1),  # Mar, Apr, May
    "Jun-Sep": data.iloc[:, 7:11].sum(axis=1),  # Jun, Jul, Aug, Sep
    "Oct-Dec": data.iloc[:, 11:14].sum(axis=1)  # Oct, Nov, Dec
}

# Add a new column for the selected period in the dataset
data[period] = period_columns[period]

# Filter data for the selected state
state_data = data[data['SUBDIVISION'] == state]

# Calculate statistics for the selected month
avg_rainfall = state_data[month].mean()
total_rainfall = state_data[month].sum()
max_rainfall = state_data[month].max()
min_rainfall = state_data[month].min()

# Tabs for Dashboard and Charts
tabs = st.tabs(["Home", "Rainfall Trends"])

# Tab 1: Dashboard
with tabs[0]:
    st.title("Flood Prediction Dashboard")
    st.write(f"### Average Rainfall in {state} for {month}: {avg_rainfall:.2f} mm")
    st.write(f"Total Rainfall in {state} for {month}: {total_rainfall:.2f} mm")
    st.write(f"Maximum Rainfall in {state} for {month}: {max_rainfall:.2f} mm")
    st.write(f"Minimum Rainfall in {state} for {month}: {min_rainfall:.2f} mm")

    # Prediction Model (Threshold-Based Example)
    if avg_rainfall > 300:
        st.error("Flood Risk: High")
    elif avg_rainfall > 150:
        st.warning("Flood Risk: Medium")
    else:
        st.success("Flood Risk: Low")

# Tab 2: Rainfall Charts
with tabs[1]:
    st.title("Rainfall Charts")
    
    # Rainfall Trends Over the Years (Interactive)
    st.write("### Rainfall Trends Over the Years")
    fig1 = px.line(state_data, x="YEAR", y=month, title=f"Monthly Rainfall in {state} for {month} (Over the Years)")
    fig1.update_layout(
        xaxis_title="Year",
        yaxis_title="Rainfall (mm)",
        template="plotly_dark"  # Dark theme for a cool look
    )
    st.plotly_chart(fig1)

    # Average Monthly Rainfall Across Years
    st.write(f"### Monthly Average Rainfall in {state} (Across All Years)")
    monthly_avg_rainfall = state_data.iloc[:, 2:14].mean()
    fig2 = px.bar(
        x=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        y=monthly_avg_rainfall,
        labels={"x": "Month", "y": "Rainfall (mm)"},
        title=f"Monthly Average Rainfall in {state} (Across All Years)",
        color=monthly_avg_rainfall,  # Color the bars based on the rainfall values
        color_continuous_scale="Blues"  # Set the color scale to a nice blue gradient
    )
    fig2.update_layout(
        xaxis_title="Month",
        yaxis_title="Rainfall (mm)",
        template="plotly_dark",  # Dark theme for a cool look
        xaxis_tickmode="array",  # Show month names
        xaxis_tickvals=list(range(12)),  # Month indices
        xaxis_ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        coloraxis_showscale=False  # Hide color scale legend
    )
    st.plotly_chart(fig2)

    # Cumulative Rainfall for Selected Period Chart
    st.write("### Cumulative Rainfall Over the Years for Selected Period")
    fig3 = px.bar(
        state_data,
        x="YEAR",
        y=period,
        title=f"Cumulative Rainfall in {state} for {period} Over the Years",
        labels={"x": "Year", "y": "Rainfall (mm)"},
        color=state_data[period],
        color_continuous_scale="Viridis"
    )
    fig3.update_layout(
        xaxis_title="Year",
        yaxis_title="Cumulative Rainfall (mm)",
        template="plotly_dark"  # Dark theme
    )
    st.plotly_chart(fig3)
    
    # Cumulative Rainfall for Selected Period
    rainfall_period = state_data[period].sum()
    st.write(f"### Cumulative Rainfall for {period}: {rainfall_period:.2f} mm")

