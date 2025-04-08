import os
import joblib
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from preprocess import load_and_preprocess_data

# Load preprocessed data
X, y, scaler = load_and_preprocess_data()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'models/fraud_model.sav')
model = joblib.load(model_path)

# Predict
y_pred = model.predict(X_test)

# Convert predictions to "Fraud" and "Not Fraud"
label_mapping = {0: "Not Fraud", 1: "Fraud"}
y_pred_labels = [label_mapping[pred] for pred in y_pred]
y_test_labels = [label_mapping[actual] for actual in y_test]

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=["Not Fraud", "Fraud"])

# Print Results
print(f"✅ Model Accuracy: {accuracy:.2f}")
print("\nClassification Report:\n", report)

# Display first 20 Predictions Vertically
print("\n🔍 Sample Predictions (First 20):")
for i in range(20):
    print(f"Transaction {i+1}:  Actual: {y_test_labels[i]}  |  Predicted: {y_pred_labels[i]}")
