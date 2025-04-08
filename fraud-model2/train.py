import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from preprocess import load_and_preprocess_data

# Clear any lingering figures from previous runs
plt.close('all')

# Load data
X, y, _ = load_and_preprocess_data()  # Scaler is saved inside preprocess.py now

# Convert X to DataFrame to ensure compatibility for `.columns`
if not isinstance(X, pd.DataFrame):
    feature_names = ['step', 'type', 'amount', 'oldbalanceorg', 'newbalanceorg', 'oldbalancedest', 'newbalancedest']
    X = pd.DataFrame(X, columns=feature_names)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Print feature names to verify they match during prediction
print(f"✅ Feature names used for training: {X_train.columns.tolist()}")

# Train model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Classification Report
report = classification_report(y_test, y_pred)
print("\n✅ Classification Report:\n", report)

# Generate and Display Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(conf_matrix, display_labels=["Not Fraud", "Fraud"])
plt.figure(figsize=(6, 6))
disp.plot(cmap="Blues")
plt.title("Confusion Matrix for Fraud Detection Model")
plt.show(block=True)  # ✅ Show confusion matrix

# === FEATURE IMPORTANCE BAR CHART ===
feature_names = ['step', 'type', 'amount', 'oldbalanceorg', 'newbalanceorg', 'oldbalancedest', 'newbalancedest']
importances = model.feature_importances_

plt.figure(figsize=(10, 6))
plt.barh(feature_names, importances, color='skyblue')
plt.title("Feature Importance in Fraud Detection Model")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.tight_layout()
plt.grid(True, axis='x')
plt.show(block=True)  # ✅ Show feature importance

# Ensure models directory exists
models_dir = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(models_dir, exist_ok=True)

# Save model only (scaler is already saved in preprocess.py)
model_path = os.path.join(models_dir, 'fraud_model.sav')
joblib.dump(model, model_path)

print(f"✅ Model saved successfully!\n📁 Model Path: {model_path}")
