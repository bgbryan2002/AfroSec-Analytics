import pandas as pd
import joblib
from preprocess import preprocess_data  
from sklearn.metrics import classification_report, accuracy_score

# Color codes
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Load model & scaler
model = joblib.load(r"C:\Users\bgbry\OneDrive\Documents\COMP 496\New\fraud-model2\models\fraud_model.sav")
scaler = joblib.load(r"C:\Users\bgbry\OneDrive\Documents\COMP 496\New\fraud-model2\models\scaler.sav")

# Load dataset
new_data = pd.read_csv(r"C:\Users\bgbry\OneDrive\Documents\COMP 496\New\fraud-model2\organized_fraud_dataset.csv")
print(f"✅ Loaded dataset with {len(new_data)} transactions.")

# Rename for consistency
new_data.rename(columns={
    'oldbalanceOrg': 'oldbalanceorg',
    'newbalanceOrig': 'newbalanceorg',
    'oldbalanceDest': 'oldbalancedest',
    'newbalanceDest': 'newbalancedest'
}, inplace=True)

# Preprocess
new_data_scaled = preprocess_data(new_data, scaler)
predictions = model.predict(new_data_scaled)
new_data["PredictedFraud"] = predictions

# Terminal Output (First 100)
print("\n✅ First 100 Transactions:")
print(f"{'Index':<6}{'Type':<12}{'Origin':<18}{'Dest':<18}{'Status':<10}")
print("=" * 70)

for i, (index, row) in enumerate(new_data.iterrows()):
    if i >= 100:
        break
    is_fraud = row["PredictedFraud"]
    color = RED if is_fraud == 1 else GREEN
    status = "Fraud" if is_fraud == 1 else "Not Fraud"
    print(f"{index+1:<6}{row['type']:<12}{row['origin_account']:<18}{row['destination_account']:<18}{color}{status}{RESET}")

# Summary
total_fraud = new_data["PredictedFraud"].sum()
total_amount = new_data.loc[new_data["PredictedFraud"] == 1, "amount"].sum()

print(f"\n🚨 Total Fraud Transactions: {RED}{total_fraud}{RESET}")
print(f"💰 Total Fraudulent Transaction Amount: {RED}${total_amount:,.2f}{RESET}")
new_data.to_csv("all_transactions.csv", index=False)
print("✅ Saved to all_transactions.csv")

# Evaluation
fraud_label = 'isFraud' if 'isFraud' in new_data.columns else 'isfraud'
if fraud_label in new_data.columns:
    print("\n✅ Model Accuracy:", accuracy_score(new_data[fraud_label], predictions))
    print("\nClassification Report:\n", classification_report(new_data[fraud_label], predictions))

# Launch UI
from ui_display import show_fraud_summary
if __name__ == "__main__":
    print("🚀 Launching SentinelPay UI...")
    show_fraud_summary()


