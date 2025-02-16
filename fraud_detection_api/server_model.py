from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the Random Forest model
model = joblib.load("random_forest_simplified.pkl")

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
        # Log errors and return an error message
        app.logger.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)