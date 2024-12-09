import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#page Title
st.set_page_config(page_title="Flood Prediction", page_icon="🌊", layout="wide")
# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data/rainfall.csv")

data = load_data()

# Sidebar for user input
st.sidebar.title("Flood Prediction")
state = st.sidebar.selectbox("Select State", data['SUBDIVISION'].unique())
month = st.sidebar.selectbox("Select Month", data.columns[2:14])  # Skip 'SUBDIVISION' and 'YEAR'

# Filter data for the selected state
state_data = data[data['SUBDIVISION'] == state]

# Handle case if multiple years are present
avg_rainfall = state_data[month].mean()

# Display Data
st.title("Flood Prediction Dashboard")
st.write(f"Average Rainfall in {state} for {month}: {avg_rainfall:.2f} mm")

# Prediction Model (Threshold-Based Example)
if avg_rainfall > 300:
    st.error("Flood Risk: High")
elif avg_rainfall > 150:
    st.warning("Flood Risk: Medium")
else:
    st.success("Flood Risk: Low")

# Visualization
st.write("Rainfall Trends")
fig, ax = plt.subplots()
state_data.iloc[:, 2:14].mean().plot(kind="bar", ax=ax)
plt.title(f"Monthly Rainfall in {state} (Average Across Years)")
plt.ylabel("Rainfall (mm)")
plt.xlabel("Month")
st.pyplot(fig)
