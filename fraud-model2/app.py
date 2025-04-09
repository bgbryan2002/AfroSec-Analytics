import pandas as pd
from fastapi import FastAPI
import gradio as gr
import joblib
import os

# Load trained model and scaler
model = joblib.load('models/fraud_model.sav')
scaler = joblib.load('models/scaler.sav')

# Prediction Function
def predict_fraud(file):
    data = pd.read_csv(file)

    # Rename to match training feature names
    rename_columns = {
        'oldbalanceOrg': 'oldbalanceorg',
        'newbalanceOrig': 'newbalanceorg',
        'oldbalanceDest': 'oldbalancedest',
        'newbalanceDest': 'newbalancedest'
    }
    data.rename(columns=rename_columns, inplace=True)

    expected_columns = ['step', 'type', 'amount', 'oldbalanceorg', 'newbalanceorg', 'oldbalancedest', 'newbalancedest']
    missing_columns = [col for col in expected_columns if col not in data.columns]
    if missing_columns:
        return pd.DataFrame({"Error": [f"Missing columns: {missing_columns}"]})

    data = data[expected_columns]

    if 'type' in data.columns:
        data['type'] = data['type'].astype('category').cat.codes  

    scaled_data = scaler.transform(data)
    predictions = model.predict(scaled_data)

    data['Fraud Prediction'] = predictions
    data['Fraud Prediction'] = data['Fraud Prediction'].apply(
        lambda x: 'Fraud' if x == 1 else 'Not Fraud'
    )
    return data

# FastAPI app base
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Fraud Detection API"}

# Gradio Blocks UI
with gr.Blocks() as demo:
    gr.Markdown("## Fraud Detection System")
    gr.Markdown("Upload a CSV file to detect fraudulent transactions based on patterns in the data.")

    # Transaction legend
    gr.Markdown("### Transaction Type Legend")
    gr.Markdown(
        "- 1 = PAYMENT  \n"
        "- 2 = TRANSFER  \n"
        "- 3 = CASH_IN  \n"
        "- 4 = DEBIT  \n"
        "- 5 = CASH_OUT"
    )

    file_input = gr.File(label="Upload CSV File")
    output_df = gr.Dataframe(render=True, wrap=True, label="Prediction Results")

    file_input.change(fn=predict_fraud, inputs=file_input, outputs=output_df)

    # Feature Importance
    gr.Markdown("### Feature Importance Chart")
    gr.Image("Screenshot 2025-04-03 145251.png", label="Feature Importance")
    gr.Markdown(
        "This chart visualizes which features the model relied on most when predicting fraud. "
        "`Amount` was the most impactful, followed by `newbalanceorg`, `oldbalanceorg`, and others."
    )

    # Confusion Matrix
    gr.Markdown("### Confusion Matrix")
    gr.Image("Screenshot 2025-04-03 142607.png", label="Confusion Matrix")
    gr.Markdown(
        "This matrix shows how well the model performed. \n\n"
        "- Top-left: True Negatives (correctly predicted non-fraud)\n"
        "- Bottom-right: True Positives (correctly predicted fraud)\n"
        "- Top-right: False Positives (non-fraud flagged as fraud)\n"
        "- Bottom-left: False Negatives (fraud missed by the model)"
    )

# Launch server
demo.launch(server_name="0.0.0.0", server_port=7860)
