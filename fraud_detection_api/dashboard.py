from dash import Dash, html, dcc
import requests
import pandas as pd
import plotly.express as px

app = Dash(__name__)

# Fetch summary statistics
try:
    response = requests.get('http://localhost:5000/summary')
    if response.status_code == 200:
        summary_data = response.json()
    else:
        summary_data = {}
except Exception as e:
    print(f"Error fetching summary: {e}")
    summary_data = {}

# Summary Boxes
summary_boxes = html.Div([
    html.Div([
        html.H3("Total Transactions"),
        html.P(summary_data.get('total_transactions', 'N/A'))
    ], style={'width': '30%', 'display': 'inline-block', 'margin': '20px'}),
    html.Div([
        html.H3("Fraud Cases"),
        html.P(summary_data.get('fraud_cases', 'N/A'))
    ], style={'width': '30%', 'display': 'inline-block', 'margin': '20px'}),
    html.Div([
        html.H3("Fraud Percentage (%)"),
        html.P(summary_data.get('fraud_percentage', 'N/A'))
    ], style={'width': '30%', 'display': 'inline-block', 'margin': '20px'})
])

# Fetch fraud trends over time
try:
    response = requests.get('http://localhost:5000/fraud-trends')
    if response.status_code == 200:
        fraud_trends_data = pd.DataFrame(response.json())
    else:
        fraud_trends_data = pd.DataFrame()
except Exception as e:
    print(f"Error fetching fraud trends: {e}")
    fraud_trends_data = pd.DataFrame()

# Fraud Trends Chart
if fraud_trends_data.empty:
    fig_fraud_trends = html.Div("No meaningful fraud trends data available.")
else:
    fig_fraud_trends = px.line(
        fraud_trends_data,
        x='time_range',
        y='class',
        title="Fraud Cases Over Time Ranges",
        labels={'class': 'Number of Fraud Cases'}
    )

# Fetch device-browser fraud data
# try:
#     response = requests.get('http://localhost:5000/device-browser-fraud')
#     if response.status_code == 200:
#         device_browser_fraud_data = pd.DataFrame(response.json())
#     else:
#         device_browser_fraud_data = pd.DataFrame()
# except Exception as e:
#     print(f"Error fetching device-browser fraud data: {e}")
#     device_browser_fraud_data = pd.DataFrame()

# # Device-Browser Fraud Chart
# if device_browser_fraud_data.empty:
#     fig_device_browser_fraud = html.Div("No meaningful device-browser fraud data available.")
# else:
#     fig_device_browser_fraud = px.bar(
#         device_browser_fraud_data,
#         x='browser',
#         y='fraud_count',
#         color='source',
#         title="Fraud Cases by Device and Browser",
#         labels={'fraud_count': 'Number of Fraud Cases'}
#     )

# Fetch geographic fraud data
try:
    response = requests.get('http://localhost:5000/geographic-fraud')
    if response.status_code == 200:
        geographic_fraud_data = pd.DataFrame(response.json())
    else:
        geographic_fraud_data = pd.DataFrame()
except Exception as e:
    print(f"Error fetching geographic fraud data: {e}")
    geographic_fraud_data = pd.DataFrame()

# Geographic Fraud Chart
if geographic_fraud_data.empty:
    fig_geographic_fraud = html.Div("No meaningful geographic fraud data available.")
else:
    fig_geographic_fraud = px.bar(
        geographic_fraud_data,
        x='country_freq_range',
        y='fraud_count',
        title="Geographic Distribution of Fraud Cases",
        labels={'fraud_count': 'Number of Fraud Cases'}
    )

# Define layout
app.layout = html.Div([
    html.H1("Fraud Detection Dashboard", style={'text-align': 'center'}),

    # Summary Boxes
    summary_boxes,

    # Fraud Trends Chart
    dcc.Graph(id='fraud-trends', figure=fig_fraud_trends),

    # Device-Browser Fraud Chart
    dcc.Graph(id='device-browser-fraud', figure=fig_device_browser_fraud),

    # Geographic Fraud Chart
    dcc.Graph(id='geographic-fraud', figure=fig_geographic_fraud)
])

# Run Dash app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)