# Flood Prediction App 🌊

A web application that predicts flood risks based on historical rainfall data across various states. Users can visualize trends, analyze rainfall data by month and period, and receive flood risk predictions.

## Description

This web application provides insights into rainfall data from different states and helps predict the risk of floods based on historical rainfall patterns. Using interactive charts, users can explore rainfall trends, monthly and cumulative rainfall statistics, and assess flood risks.

## Features

- **Interactive Charts**: Visualize rainfall trends over the years with Plotly.
- **Monthly Statistics**: View average, total, max, and min rainfall for any month.
- **Flood Risk Prediction**: Predict the likelihood of floods based on rainfall thresholds.
- **Period Analysis**: Analyze rainfall for different periods like Jan-Feb, Mar-May, Jun-Sep, and Oct-Dec.

## Usage

- **Select a State**: From the sidebar, choose a state to analyze.
- **Select a Month**: Choose a month to see rainfall data for that month.
- **Choose a Period**: Select from "Annual", "Jan-Feb", "Mar-May", "Jun-Sep", or "Oct-Dec" to analyze cumulative rainfall data across the years.
- **View Flood Risk**: Based on the rainfall data, the app will predict the flood risk (Low, Medium, High) for the selected month.

The app provides two tabs:
1. **Home**: Shows key statistics like average, total, max, and min rainfall, along with the flood risk prediction.
2. **Rainfall Trends**: Displays interactive charts showing rainfall trends and comparisons across years.

## Acknowledgements

- **Streamlit**: For providing an easy-to-use framework for building interactive web apps.
- **Plotly**: For the interactive charts that make visualizing the data more intuitive.
- **Pandas**: For data manipulation and analysis.
