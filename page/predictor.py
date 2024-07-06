import streamlit as st
import pandas as pd
import numpy as np
from CreditCardFraudDetection.pipeline.default_prediction_pipeline import DefaultPredictionPipeline
from CreditCardFraudDetection.pipeline.fraudulent_prediction_pipeline import FraudulentPredictionPipeline

def run():
    with st.sidebar:

        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.markdown("""
        <div style="padding: 10px; border: 2px solid #ffffff; border-radius: 15px; background-color: #0E1117; color: #ffffff;">
        <p style="text-align: justify; margin: 0 0 15px 0;">
            🔍 Detect credit card fraud with our advanced AI prediction system.
        </p>
        <p style="text-align: justify; margin: 0;">
            💳 Identify suspicious transactions early to protect your customers.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.header("Credit Card Fraud Risk Assessment", divider="rainbow")
    st.write("""
    Please enter the requested demographic and financial data related to credit card, and
    our service will help you determine the behaviour of transaction or default status of the credit card user.
    """)

    choice = st.radio("**What kind of risk assessment you want to perform?**", ["Transaction Behaviour", "Default Status of Credit Card Holder"],
                    index=None, captions=["This will help you determine whether a transaction is fraudulent or not",
                                            "This will help you determine whether a credit card holder will default or not"])

    if choice == "Transaction Behaviour":
        ## Creating a data collection form for transaction behaviour
        st.subheader("Transaction Behaviour Assessment")
        with st.form("transaction_behaviour_form", clear_on_submit=False, border=True):
            st.write("Please enter the requested information below:")

            V1 = st.number_input("V1", value=None)
            V2 = st.number_input("V2", value=None)
            V3 = st.number_input("V3", value=None)
            V4 = st.number_input("V4", value=None)
            V5 = st.number_input("V5", value=None)
            V6 = st.number_input("V6", value=None)
            V7 = st.number_input("V7", value=None)
            V8 = st.number_input("V8", value=None)
            V9 = st.number_input("V9", value=None)
            V10 = st.number_input("V10", value=None)
            V11 = st.number_input("V11", value=None)
            V12 = st.number_input("V12", value=None)
            V13 = st.number_input("V13", value=None)
            V14 = st.number_input("V14", value=None)
            V15 = st.number_input("V15", value=None)
            V16 = st.number_input("V16", value=None)
            V17 = st.number_input("V17", value=None)
            V18 = st.number_input("V18", value=None)
            V19 = st.number_input("V19", value=None)
            V20 = st.number_input("V20", value=None)
            V21 = st.number_input("V21", value=None)
            V22 = st.number_input("V22", value=None)
            V23 = st.number_input("V23", value=None)
            V24 = st.number_input("V24", value=None)
            V25 = st.number_input("V25", value=None)
            V26 = st.number_input("V26", value=None)
            V27 = st.number_input("V27", value=None)
            V28 = st.number_input("V28", value=None)
            Amount = st.number_input("Amount", value=None)

            submitted = st.form_submit_button("Know the Behaviour")

            if submitted:
                data = {
                    "V1": [V1], "V2": [V2], "V3": [V3], "V4": [V4], "V5": [V5], "V6": [V6], "V7": [V7], "V8": [V8], "V9": [V9], "V10": [V10],
                    "V11": [V11], "V12": [V12], "V13": [V13], "V14": [V14], "V15": [V15], "V16": [V16], "V17": [V17], "V18": [V18], "V19": [V19], "V20": [V20],
                    "V21": [V21], "V22": [V22], "V23": [V23], "V24": [V24], "V25": [V25], "V26": [V26], "V27": [V27], "V28": [V28], "Amount": [Amount]
                }

                data = pd.DataFrame(data)

                obj = FraudulentPredictionPipeline()
                prediction = obj.predict(data)

                if prediction == 1:
                    st.error("This transaction is fraudulent!", icon="🚨")
                else:
                    st.success("This transaction is not fraudulent!", icon="✅")

    if choice == "Default Status of Credit Card Holder":
        ## Creating a data collection form for default status
        st.subheader("Default Status Assessment")
        with st.form("default_status_form", clear_on_submit=False, border=True):
            st.write("Please enter the requested information below:")

            LIMIT_BAL = st.number_input("LIMIT_BAL", value=None, placeholder="Enter the credit limit")
            gender = st.selectbox("select your gender:", ["Male", "Female"], index=None)
            if gender == "Male":
                SEX = 1
            else:
                SEX = 2

            education = st.selectbox("Select your education level:", ["Graduate School", "University", "High School", "Others"], index=None)
            if education == "Graduate School":
                EDUCATION = 1
            elif education == "University":
                EDUCATION = 2
            elif education == "High School":
                EDUCATION = 3
            else:
                EDUCATION = 4

            maritial_status = st.selectbox("Select your marital status:", ["Married", "Single", "Others"], index=None)
            if maritial_status == "Married":
                MARRIAGE = 1
            elif maritial_status == "Single":
                MARRIAGE = 2
            else:
                MARRIAGE = 3

            AGE = st.number_input("AGE", value=None, placeholder="Enter your age")
            PAY_1 = st.number_input("PAY_1", value=None, placeholder="Enter the repayment status in September")
            PAY_2 = st.number_input("PAY_2", value=None, placeholder="Enter the repayment status in August")
            PAY_3 = st.number_input("PAY_3", value=None, placeholder="Enter the repayment status in July")
            PAY_4 = st.number_input("PAY_4", value=None, placeholder="Enter the repayment status in June")
            PAY_5 = st.number_input("PAY_5", value=None, placeholder="Enter the repayment status in May")
            PAY_6 = st.number_input("PAY_6", value=None, placeholder="Enter the repayment status in April")
            BILL_AMT1 = st.number_input("BILL_AMT1", value=None, placeholder="Enter the bill amount in September")

            PAY_AMT1 = st.number_input("PAY_AMT1", value=None, placeholder="Enter the payment amount in September")
            PAY_AMT2 = st.number_input("PAY_AMT2", value=None, placeholder="Enter the payment amount in August")
            PAY_AMT3 = st.number_input("PAY_AMT3", value=None, placeholder="Enter the payment amount in July")
            PAY_AMT4 = st.number_input("PAY_AMT4", value=None, placeholder="Enter the payment amount in June")
            PAY_AMT5 = st.number_input("PAY_AMT5", value=None, placeholder="Enter the payment amount in May")
            PAY_AMT6 = st.number_input("PAY_AMT6", value=None, placeholder="Enter the payment amount in April")

            submitted = st.form_submit_button("Know the Default Status")

            if submitted:
                data = {
                    "LIMIT_BAL": [LIMIT_BAL], "SEX": [SEX], "EDUCATION": [EDUCATION], "MARRIAGE": [MARRIAGE], "AGE": [AGE],
                    "PAY_1": [PAY_1], "PAY_2": [PAY_2], "PAY_3": [PAY_3], "PAY_4": [PAY_4], "PAY_5": [PAY_5], "PAY_6": [PAY_6],
                    "BILL_AMT1": [BILL_AMT1], "PAY_AMT1": [PAY_AMT1], "PAY_AMT2": [PAY_AMT2], "PAY_AMT3": [PAY_AMT3], "PAY_AMT4": [PAY_AMT4],
                    "PAY_AMT5": [PAY_AMT5], "PAY_AMT6": [PAY_AMT6]
                }

                data = pd.DataFrame(data)

                obj = DefaultPredictionPipeline()
                prediction = obj.predict(data)

                if prediction == 1:
                    st.error("The credit card holder will default!", icon="🚨")
                else:
                    st.success("The credit card holder will not default!", icon="✅")

            

            