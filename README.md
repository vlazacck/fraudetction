README for Fraud Detection Project
Project Overview
This project is a comprehensive fraud detection system that leverages machine learning to identify fraudulent transactions. It includes:

Data Preprocessing : Cleaning and transforming raw transaction data into a format suitable for training.
Model Training : Developing a Random Forest classifier for fraud prediction.
Model Interpretability : Using SHAP and LIME to explain model predictions and gain insights into feature importance.
API Development : Creating a Flask API to serve the trained model and provide real-time predictions.
Dashboard Integration : Building an interactive dashboard using Dash to visualize fraud trends, device-browser fraud patterns, and geographic fraud distribution.
The project demonstrates the end-to-end process of building a production-ready fraud detection system, from data preparation to deployment.

Key Features
High Performance Model : The Random Forest classifier achieves an F1-Score of 0.91 and ROC-AUC Score of 0.99 , showcasing strong predictive power.
Interpretability : Insights into model behavior are provided through SHAP summary plots and LIME local explanations.
Scalable API : A Flask-based RESTful API ensures seamless integration with external systems for real-time predictions.
Interactive Dashboard : A Dash-powered frontend provides visualizations for fraud trends, device-browser fraud patterns, and geographic fraud distribution.
My Contributions
As the developer of this project, my contributions include:

Data Preprocessing :
Cleaned and transformed raw transaction data by handling missing values, encoding categorical variables, and creating new features like time_since_last_transaction and country_freq.
Removed irrelevant or problematic columns (e.g., signup_time, purchase_time, device_id) to ensure compatibility with machine learning models.
Model Development :
Trained a Random Forest classifier on the preprocessed dataset, achieving high accuracy and robust performance.
Optimized hyperparameters (n_estimators=200, max_depth=15, class_weight='balanced') to handle class imbalance effectively.
Model Interpretability :
Implemented SHAP and LIME to interpret model predictions and understand the contribution of each feature.
Generated visualizations to communicate complex model outputs in an accessible manner.
API Development :
Developed a Flask backend (server_model.py) to serve the trained model via API endpoints.
Ensured the API dynamically handles missing or extra features in incoming payloads, maintaining compatibility with the model.
Dashboard Integration :
Built an interactive dashboard using Dash (dashboard.py) to visualize key fraud insights.
Integrated Flask API endpoints into the dashboard to fetch and display data for:
Total transactions, fraud cases, and fraud percentages.
Fraud trends over time.
Device-browser fraud patterns.
Geographic fraud distribution.
Error Handling and Logging :
Added error-handling mechanisms in both Flask and Dash scripts to ensure graceful handling of edge cases.
Integrated logging functionality to track incoming requests, errors, and predictions for continuous monitoring.
Dockerization :
Containerized the Flask API using Docker to ensure consistent deployment across different environments.
