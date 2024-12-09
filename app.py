import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Set Streamlit page configuration - should be the first Streamlit command
st.set_page_config(page_title="Flood Prediction", page_icon="🌊", layout="wide")

st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data/rainfall.csv")

data = load_data()

# Streamlit app layout
# Sidebar for user input
st.sidebar.title("Flood Prediction")
state = st.sidebar.selectbox("Select State", data['SUBDIVISION'].unique())
month = st.sidebar.selectbox("Select Month", data.columns[2:14])  # Skip 'SUBDIVISION' and 'YEAR'

# Filter data for the selected state
state_data = data[data['SUBDIVISION'] == state]

# Calculate statistics for the selected month
avg_rainfall = state_data[month].mean()
total_rainfall = state_data[month].sum()
max_rainfall = state_data[month].max()
min_rainfall = state_data[month].min()

# Display Data
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

# Plotly interactive chart: Rainfall Trends Over the Years
st.write("Rainfall Trends Over the Years (Interactive)")
fig = px.line(state_data, x="YEAR", y=month, title=f"Monthly Rainfall in {state} for {month} (Over the Years)")
fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Rainfall (mm)",
    template="plotly_dark"  # Dark theme for a cool look
)
st.plotly_chart(fig)

# Visualization of average monthly rainfall across years
# st.write(f"Average Monthly Rainfall in {state} (Across All Years)")
monthly_avg_rainfall = state_data.iloc[:, 2:14].mean()

# Create a Plotly bar chart
fig = px.bar(
    x=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    y=monthly_avg_rainfall,
    labels={"x": "Month", "y": "Rainfall (mm)"},
    title=f"Monthly Average Rainfall in {state} (Across All Years)",
    color=monthly_avg_rainfall,  # Color the bars based on the rainfall values
    color_continuous_scale="Blues"  # Set the color scale to a nice blue gradient
)

# Customize the chart layout
fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Rainfall (mm)",
    template="plotly_dark",  # Set the theme to "plotly_dark" for a cool, dark background
    xaxis_tickmode="array",  # Set ticks to show month names
    xaxis_tickvals=list(range(12)),  # Display each month on the x-axis
    xaxis_ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    coloraxis_showscale=False  # Hide the color scale legend
)

# Show the interactive Plotly chart
st.plotly_chart(fig)
