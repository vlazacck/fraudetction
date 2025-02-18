from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import sys

app = Flask(__name__)

# Load the Random Forest model
try:
    model = joblib.load("../fraud_detection_api/fraud_detection_rf2.pkl")
    print("Random Forest model loaded successfully.", file=sys.stdout)
except Exception as e:
    print(f"Error loading model: {e}", file=sys.stderr)
    sys.exit(1)

# Load the fraud dataset
try:
    fraud_data = pd.read_csv('../data/Fraud_Data_Processed.csv')  # Replace with your dataset path
    print("Fraud dataset loaded successfully.", file=sys.stdout)
except Exception as e:
    print(f"Error loading dataset: {e}", file=sys.stderr)
    sys.exit(1)

# Add 'country' column if missing (using ip_address mapping)
def get_country(ip_address, ip_mapping):
    if pd.isnull(ip_address) or not isinstance(ip_address, str):  # Handle missing or invalid IPs
        return 'Unknown'
    try:
        octets = list(map(int, ip_address.split('.')))
        if len(octets) != 4:
            return 'Unknown'
        ip_int = (octets[0] * 256**3) + (octets[1] * 256**2) + (octets[2] * 256) + octets[3]
        match = ip_mapping[
            (ip_mapping['lower_bound_ip_address'] <= ip_int) &
            (ip_mapping['upper_bound_ip_address'] >= ip_int)
        ]
        return match.iloc[0]['country'] if not match.empty else 'Unknown'
    except Exception as e:
        print(f"Error processing IP address '{ip_address}': {e}", file=sys.stderr)
        return 'Unknown'

# Load IP-to-Country mapping file
try:
    ip_address_data = pd.read_csv('IpAddress_to_Country.csv')  # Replace with your mapping file path
    if 'country' not in fraud_data.columns:
        fraud_data['country'] = fraud_data['ip_address'].apply(lambda x: get_country(x, ip_address_data))
    fraud_data.drop(columns=['ip_address'], inplace=True, errors='ignore')
except Exception as e:
    print(f"Error loading IP-to-Country mapping file: {e}", file=sys.stderr)

# Frequency encode 'country'
if 'country_freq' not in fraud_data.columns and 'country' in fraud_data.columns:
    country_freq = fraud_data['country'].map(fraud_data['country'].value_counts(normalize=True)).fillna(0)
    fraud_data['country_freq'] = country_freq
fraud_data.drop(columns=['country'], inplace=True, errors='ignore')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse input data from JSON
        data = request.json
        features = pd.DataFrame(data, index=[0])

        # Ensure the feature set matches the model's expectations
        expected_features = model.feature_names_in_
        for feature in expected_features:
            if feature not in features.columns:
                features[feature] = 0  # Add missing features with default value 0

        # Remove extra columns not expected by the model
        extra_cols = [col for col in features.columns if col not in expected_features]
        features.drop(columns=extra_cols, inplace=True, errors='ignore')

        # Make predictions
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[:, 1][0]

        # Return response as JSON
        return jsonify({
            'prediction': int(prediction),
            'probability': float(probability)
        })

    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 400


@app.route('/summary', methods=['GET'])
def get_summary():
    try:
        # Calculate summary statistics
        total_transactions = len(fraud_data)
        fraud_cases = fraud_data['class'].sum()
        fraud_percentage = (fraud_cases / total_transactions) * 100

        # Log summary statistics
        print(f"Summary Statistics - Total Transactions: {total_transactions}, Fraud Cases: {fraud_cases}, Fraud Percentage: {fraud_percentage}%", file=sys.stdout)

        # Return summary as JSON
        return jsonify({
            'total_transactions': int(total_transactions),
            'fraud_cases': int(fraud_cases),
            'fraud_percentage': float(fraud_percentage)
        })

    except Exception as e:
        app.logger.error(f"Error fetching summary: {e}")
        return jsonify({'error': str(e)}), 500


# @app.route('/fraud-trends', methods=['GET'])
# def get_fraud_trends():
#     try:
#         # Use 'time_since_last_transaction' for trends
#         if 'time_since_last_transaction' not in fraud_data.columns:
#             print("Warning: 'time_since_last_transaction' column not found. Generating dummy fraud trends.", file=sys.stdout)
#             fraud_trends = pd.DataFrame({
#                 'time_range': ['0-100', '101-200', '201-300', '301-400'],
#                 'class': [0, 0, 0, 0]  # Replace with actual fraud data if available
#             })
#         else:
#             # Group fraud cases by time range
#             fraud_data['time_range'] = pd.cut(
#                 fraud_data['time_since_last_transaction'],
#                 bins=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
#                 labels=['0-100', '101-200', '201-300', '301-400', '401-500', '501-600', '601-700', '701-800', '801-900', '>900']
#             )
#             fraud_trends = fraud_data.groupby('time_range')['class'].sum().reset_index()

#         # Convert to dictionary format for JSON response
#         fraud_trends_dict = fraud_trends.to_dict(orient='records')
#         return jsonify(fraud_trends_dict)

    # except Exception as e:
    #     app.logger.error(f"Error fetching fraud trends: {e}")
    #     return jsonify({'error': str(e)}), 500


@app.route('/device-browser-fraud', methods=['GET'])
def get_device_browser_fraud():
    try:
        # Check if one-hot encoded columns exist
        browser_columns = [col for col in fraud_data.columns if col.startswith('browser_')]
        source_columns = [col for col in fraud_data.columns if col.startswith('source_')]

        if not browser_columns or not source_columns:
            print("Warning: 'browser_*' or 'source_*' columns not found. Generating dummy device-browser fraud data.")
            device_browser_fraud = pd.DataFrame({
                'browser': ['Safari', 'Chrome', 'Firefox'],
                'source': ['Direct', 'SEO', 'Direct'],
                'fraud_count': [0, 0, 0]  # Replace with actual fraud data if available
            })
        else:
            # Aggregate fraud cases by browser and source
            fraud_data['browser'] = fraud_data[browser_columns].idxmax(axis=1).str.replace('browser_', '')
            fraud_data['source'] = fraud_data[source_columns].idxmax(axis=1).str.replace('source_', '')

            # Group fraud cases by browser and source
            device_browser_fraud = fraud_data.groupby(['browser', 'source'])['class'].sum().reset_index()

        # Convert to dictionary format for JSON response
        device_browser_fraud_dict = device_browser_fraud.to_dict(orient='records')
        return jsonify(device_browser_fraud_dict)

    except Exception as e:
        app.logger.error(f"Error fetching device-browser fraud data: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/geographic-fraud', methods=['GET'])
def get_geographic_fraud():
    try:
        # Check if 'country_freq' column exists
        if 'country_freq' not in fraud_data.columns:
            print("Warning: 'country_freq' column not found. Generating dummy geographic fraud data.", file=sys.stdout)
            geographic_fraud = pd.DataFrame({
                'country_freq_range': ['Very Low', 'Low', 'Medium', 'High'],
                'fraud_count': [0, 0, 0, 0]  # Replace with actual fraud data if available
            })
        else:
            # Group fraud cases by country frequency ranges
            fraud_data['country_freq_range'] = pd.cut(
                fraud_data['country_freq'],
                bins=[0, 0.01, 0.1, 0.5, 1],
                labels=['Very Low', 'Low', 'Medium', 'High']
            )
            geographic_fraud = fraud_data.groupby('country_freq_range')['class'].sum().reset_index()

        # Convert to dictionary format for JSON response
        geographic_fraud_dict = geographic_fraud.to_dict(orient='records')
        return jsonify(geographic_fraud_dict)

    except Exception as e:
        app.logger.error(f"Error fetching geographic fraud data: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)