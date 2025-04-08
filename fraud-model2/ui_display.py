import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import winsound
import random

# Load dataset
csv_file = "all_transactions.csv"
df = pd.read_csv(csv_file)

# Main UI function
def show_fraud_summary():
    window = tk.Tk()
    window.title("SentinelPay - Live Fraud Detection")
    window.geometry("1200x700")
    window.configure(bg="#FFFFFF")

    # Logo
    try:
        image = Image.open("sentinelpay_logo.png")
        image = image.resize((320, 140), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        img_label = tk.Label(window, image=photo, bg="#FFFFFF", bd=5, relief="ridge")
        img_label.image = photo
        img_label.pack(pady=10)
    except Exception as e:
        print(f"⚠️ Error loading image: {e}")

    # Title
    title = tk.Label(window, text="SentinelPay - AI Fraud Detection",
                     font=("Orbitron", 22, "bold"), bg="#FFFFFF", fg="black")
    title.pack(pady=5)

    # Live stats
    fraud_count_var = tk.StringVar()
    total_amount_var = tk.StringVar()
    fraud_count_var.set(f"🚨 Total Fraud Transactions: 0")
    total_amount_var.set(f"💰 Fraudulent Transaction Amount: $0.00")

    fraud_count_label = tk.Label(window, textvariable=fraud_count_var,
                                 font=("Orbitron", 14, "bold"),
                                 bg="white", fg="black", padx=20, pady=10,
                                 relief="solid", borderwidth=2, highlightbackground="#007BFF")
    fraud_count_label.pack(pady=5)

    total_amount_label = tk.Label(window, textvariable=total_amount_var,
                                  font=("Orbitron", 14, "bold"),
                                  bg="white", fg="black", padx=20, pady=10,
                                  relief="solid", borderwidth=2, highlightbackground="#007BFF")
    total_amount_label.pack(pady=5)

    # Table setup
    frame = tk.Frame(window, bg="#FFFFFF", padx=10, pady=10)
    frame.pack(pady=10, fill="both", expand=True)

    columns = ("ID", "Type", "Origin", "Destination", "Amount", "Fraud")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

    tree.column("ID", width=60, anchor="center")
    tree.column("Type", width=100, anchor="center")
    tree.column("Origin", width=160, anchor="center")
    tree.column("Destination", width=160, anchor="center")
    tree.column("Amount", width=140, anchor="center")
    tree.column("Fraud", width=100, anchor="center")

    tree.heading("ID", text="ID")
    tree.heading("Type", text="Type")
    tree.heading("Origin", text="Origin Account")
    tree.heading("Destination", text="Destination Account")
    tree.heading("Amount", text="Amount ($)")
    tree.heading("Fraud", text="Fraudulent?")

    tree.pack(fill="both", expand=True)

    # Styling
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Orbitron", 14, "bold"))
    style.configure("Treeview", rowheight=25, borderwidth=1, relief="ridge",
                    highlightthickness=1, highlightbackground="black", highlightcolor="black")

    tree.tag_configure("fraud", background="red", foreground="white")
    tree.tag_configure("normal", background="white", foreground="black")

    # Initial transactions
    displayed_transactions = []
    for index, row in df.head(20).iterrows():
        is_fraud = "Fraud" if row["PredictedFraud"] == 1 else "Not Fraud"
        fraud_tag = "fraud" if is_fraud == "Fraud" else "normal"

        tree.insert("", "end", values=(
            index + 1,
            row["type"],
            row["origin_account"],
            row["destination_account"],
            f"${row['amount']:,.2f}",
            is_fraud
        ), tags=(fraud_tag,))
        displayed_transactions.append(row)

    # Beep on fraud
    def play_alert_sound():
        winsound.Beep(1500, 500)

    # Dynamic updates
    def update_transactions():
        nonlocal displayed_transactions
        new_rows = random.randint(1, 4)

        for _ in range(new_rows):
            if len(displayed_transactions) < len(df):
                row = df.iloc[len(displayed_transactions)]
                is_fraud = "Fraud" if row["PredictedFraud"] == 1 else "Not Fraud"
                fraud_tag = "fraud" if is_fraud == "Fraud" else "normal"

                tree.insert("", "end", values=(
                    len(displayed_transactions) + 1,
                    row["type"],
                    row["origin_account"],
                    row["destination_account"],
                    f"${row['amount']:,.2f}",
                    is_fraud
                ), tags=(fraud_tag,))

                if is_fraud == "Fraud":
                    play_alert_sound()

                displayed_transactions.append(row)

        # Update stats
        visible = df.iloc[:len(displayed_transactions)]
        visible_fraud = visible[visible["PredictedFraud"] == 1]
        fraud_count_var.set(f"🚨 Total Fraud Transactions: {len(visible_fraud)}")
        total_amount_var.set(f"💰 Fraudulent Transaction Amount: ${visible_fraud['amount'].sum():,.2f}")

        window.after(random.randint(3000, 5000), update_transactions)

    update_transactions()
    window.mainloop()

# Run if standalone
if __name__ == "__main__":
    show_fraud_summary()
