import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, LSTM, Dense, Dropout
from sklearn.metrics import f1_score, roc_auc_score

# Reshape data for RNN/LSTM
X_train_rnn = X_train.values.reshape(X_train.shape[0], 1, X_train.shape[1])
X_test_rnn = X_test.values.reshape(X_test.shape[0], 1, X_test.shape[1])

# === RNN Model ===
# Define RNN model
model_rnn = Sequential([
    SimpleRNN(64, activation='relu', input_shape=(1, X_train.shape[1])),
    Dropout(0.5),  # Add dropout to reduce overfitting
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')  # Binary classification output
])

# Compile RNN model
class_weights = {0: 1, 1: 100}  # Adjust weights based on class distribution
model_rnn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train RNN model
history_rnn = model_rnn.fit(
    X_train_rnn, y_train,
    epochs=10,
    batch_size=64,
    validation_data=(X_test_rnn, y_test),
    class_weight=class_weights
)

# Evaluate RNN model
y_pred_rnn = (model_rnn.predict(X_test_rnn) > 0.5).astype(int).flatten()
f1_rnn = f1_score(y_test, y_pred_rnn)
roc_auc_rnn = roc_auc_score(y_test, model_rnn.predict(X_test_rnn).flatten())

print("RNN Results:")
print("F1-Score:", f1_rnn)
print("ROC-AUC Score:", roc_auc_rnn)

# === LSTM Model ===
# Define LSTM model
model_lstm = Sequential([
    LSTM(64, activation='relu', input_shape=(1, X_train.shape[1])),
    Dropout(0.5),  # Add dropout to reduce overfitting
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')  # Binary classification output
])

# Compile LSTM model
model_lstm.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train LSTM model
history_lstm = model_lstm.fit(
    X_train_rnn, y_train,
    epochs=10,
    batch_size=64,
    validation_data=(X_test_rnn, y_test),
    class_weight=class_weights
)

# Evaluate LSTM model
y_pred_lstm = (model_lstm.predict(X_test_rnn) > 0.5).astype(int).flatten()
f1_lstm = f1_score(y_test, y_pred_lstm)
roc_auc_lstm = roc_auc_score(y_test, model_lstm.predict(X_test_rnn).flatten())

print("LSTM Results:")
print("F1-Score:", f1_lstm)
print("ROC-AUC Score:", roc_auc_lstm)