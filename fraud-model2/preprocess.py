import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Step 1: Define Required Features (MUST Match Training Features)
FEATURES = ['step', 'type', 'amount', 'oldbalanceorg', 'newbalanceorg', 'oldbalancedest', 'newbalancedest', 'isFraud']

def load_and_preprocess_data(file_path="C:/Users/bgbry/OneDrive/Documents/COMP 496/New/fraud-model2/organized_fraud_dataset.csv"):
    """
    Load data, preprocess it, and return X (features), y (labels), and fitted scaler.
    """
    # Step 2: Load Data with Correct Column Names
    raw_data = pd.read_csv(file_path)
    
    # Step 3: Rename Columns to Match Model Training
    rename_columns = {
        'oldbalanceOrg': 'oldbalanceorg',
        'newbalanceOrig': 'newbalanceorg',
        'oldbalanceDest': 'oldbalancedest',
        'newbalanceDest': 'newbalancedest'
    }
    raw_data.rename(columns=rename_columns, inplace=True)

    # Step 4: Select Only Required Columns
    missing_columns = [col for col in FEATURES if col not in raw_data.columns]
    if missing_columns:
        raise ValueError(f"❌ Missing columns in dataset: {missing_columns}")

    data = raw_data[FEATURES]

    # Step 5: Convert 'type' Column to Numeric Codes
    if 'type' in data.columns:
        data['type'] = data['type'].astype('category').cat.codes  

    # Step 6: Separate Features (X) and Target Variable (y)
    X = data.drop(columns=['isFraud'])
    y = data['isFraud']

    # Step 7: Scale Numerical Features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Step 8: Save the fitted scaler using `joblib`
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(models_dir, exist_ok=True)
    scaler_path = os.path.join(models_dir, 'scaler.sav')
    joblib.dump(scaler, scaler_path)
    
    print(f"✅ Scaler successfully saved at: {scaler_path}")

    return X_scaled, y, scaler


def preprocess_data(data, scaler):
    """
    Preprocess new data before prediction.
    :param data: New transaction data.
    :param scaler: Pre-trained StandardScaler instance.
    :return: Scaled numerical data.
    """
    
    # Define required features in the same order as training
    required_columns = ['step', 'type', 'amount', 'oldbalanceorg', 'newbalanceorg', 'oldbalancedest', 'newbalancedest']
    
    # Reorder columns to match training data**
    data = data.loc[:, required_columns]

    # Convert 'type' column to numeric codes
    if 'type' in data.columns:
        data.loc[:, 'type'] = data['type'].astype('category').cat.codes  

    # Apply scaling
    data_scaled = scaler.transform(data)

    return data_scaled
