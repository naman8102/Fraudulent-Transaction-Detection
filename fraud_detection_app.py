import streamlit as st
import pandas as pd
import joblib
import warnings
from PIL import Image

warnings.filterwarnings("ignore")

# Load your trained model
clf = joblib.load('fraud_detection_model.pkl')

# Set up the page configuration
st.set_page_config(page_title="Fraud Detection System", page_icon="💳", layout="centered")

# Header and description
st.title("💳 Fraud Detection System")
st.markdown("""
    Welcome to the Fraud Detection System! This tool helps identify potentially fraudulent transactions based on inputted transaction data. 
    Fill in the transaction details below, and the system will classify it as **Fraudulent** or **Not Fraudulent**.
    """)

# Optional image or logo
st.image("newImage2.jpg", use_column_width=True)  

# Divider for aesthetics
st.markdown("---")

# Example data section
st.subheader("Example Data")
st.markdown("""
- **Step**: Sequential ID for transaction steps (e.g., `1`, `10`, `50`)
- **Transaction Type**: Select the type of transaction, such as *Cash In*, *Cash Out*, *Debit*, etc.
- **Amount**: Total transaction amount in USD (e.g., `2000.0`, `50000.0`, `12000.0`)
- **Old Balance (Original Account)**: The original balance before the transaction in the account initiating the transaction (e.g., `10000.0`, `200000.0`, `5000.0`)
- **New Balance (Original Account)**: The balance after the transaction in the account initiating the transaction (e.g., `8000.0`, `150000.0`, `3000.0`)
- **Old Balance (Destination Account)**: The original balance before the transaction in the destination account (e.g., `5000.0`, `0.0`, `7000.0`)
- **New Balance (Destination Account)**: The balance after the transaction in the destination account (e.g., `7000.0`, `50000.0`, `10000.0`)
""")

# Divider
st.markdown("---")

# Input form for transaction details
st.subheader("Enter Transaction Details")

# Create input fields for each feature with placeholders
step = st.number_input("🔢 Transaction Step:", min_value=0, help="Step in the transaction timeline (e.g., 1, 10, 50)")
type_val = st.selectbox("🔄 Transaction Type", options=["Cash In", "Cash Out", "Debit", "Payment", "Transfer"], help="Type of transaction")
amount = st.number_input("💰 Amount (USD):", min_value=0.0, help="Total transaction amount in USD (e.g., 2000, 50000)")
oldbalanceOrg = st.number_input("💼 Old Balance (Original Account):", min_value=0.0, help="Original balance before the transaction (e.g., 10000, 200000)")
newbalanceOrig = st.number_input("📉 New Balance (Original Account):", min_value=0.0, help="New balance after the transaction (e.g., 8000, 150000)")
oldbalanceDest = st.number_input("🏦 Old Balance (Destination Account):", min_value=0.0, help="Destination account balance before the transaction (e.g., 5000, 0)")
newbalanceDest = st.number_input("📈 New Balance (Destination Account):", min_value=0.0, help="Destination account balance after the transaction (e.g., 7000, 50000)")

# Map transaction type to numerical values
type_mapping = {"Cash In": 0, "Cash Out": 1, "Debit": 2, "Payment": 3, "Transfer": 4}
type_encoded = type_mapping[type_val]

# Prediction button
if st.button("🔍 Predict Fraud"):
    # Create a DataFrame with the input values
    input_data = pd.DataFrame({
        'step': [step],
        'type': [type_encoded],
        'amount': [amount],
        'oldbalanceOrg': [oldbalanceOrg],
        'newbalanceOrig': [newbalanceOrig],
        'oldbalanceDest': [oldbalanceDest],
        'newbalanceDest': [newbalanceDest]
    })

    # Make a prediction
    prediction = clf.predict(input_data)[0]

    # Display the result with icons and colors
    st.markdown("---")
    st.subheader("Prediction Result")
    if prediction == 1:
        st.error("🚨 The transaction is classified as **Fraudulent**.")

        st.markdown("""
    ### Analysis:
    - **Large Transaction Amount** combined with **low transaction history**.
    - **Transaction Type** such as cash-out ot transfer, common in fraudulent schemes.
    - **Abnormal balance changes** between source and destination accounts.
    """)
        
        st.markdown("""
    ### Preventive Measures:
    - **Enable two-step authentication (2FA)** on all accounts to add an extra layer of security.
    - **Monitor account balance and transaction history** regularly for any unusual activity.
    - **Avoid sharing account details** and ensure that account access credentials are kept secure.
    - **Set alerts for high-values transactions** to quickly spot unauthorized activities.
    """)
        
    else:
        st.success("✅ The transaction is classified as **Not Fraudulent**.")

        st.markdown("""
    ### Analysis:
    Based on the input values, the transaction follows a typical pattern, with no major red flags indicating fraud. Normal behavior is observed in:
    
    - **Transaction Amount** and **balance history** compatibility.
    - **Expected transaction type** that matches the user's profile.
    """)

# Footer with additional information
st.markdown("---")

