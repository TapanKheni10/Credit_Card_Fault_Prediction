import streamlit as st  
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def default_payment_by_credit_limit():
    df = pd.read_csv('artifacts/data_ingestion/default.csv')
    data = df[["LIMIT_BAL", "AGE", "default.payment.next.month"]]

    bins = [0, 50000, 100000, 150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000, 550000, 600000, 650000, 700000, 
            750000, 800000, 850000, 900000, 950000, 1000000]
    labels = ["0-50K", "50K-100K", "100K-150K", "150K-200K", "200K-250K", "250K-300K", "300K-350K", "350K-400K", "400K-450K", 
              "450K-500K", "500K-550K", "550K-600K", "600K-650K", "650K-700K", "700K-750K", "750K-800K", "800K-850K", "850K-900K", "900K-950K", "950K-1M"]
    
    data["LIMIT_BAL_RANGE"] = pd.cut(data["LIMIT_BAL"], bins=bins, labels=labels)

    default_counts = data[data["default.payment.next.month"] == 1]["LIMIT_BAL_RANGE"].value_counts().sort_index()
    total_default_count = data[data["default.payment.next.month"] == 1]["default.payment.next.month"].value_counts()
    
    for x in range(len(default_counts)):
        answer = default_counts[x] / total_default_count
        default_counts[x] = answer
        

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(default_counts.index, default_counts.values, color='skyblue')
    plt.xlabel('LIMIT_BAL Range', fontsize=14)
    plt.ylabel('Number of Defaults', fontsize=14)
    plt.title('Number of Defaults by LIMIT_BAL Range', fontsize=16)
    plt.xticks(rotation=45, ha='right', fontsize=6)
  
    ax.axis('tight')
    plt.show()

    st.subheader('Default Payment by Credit Limit')
    
    st.markdown("""
        The graph shows the relationship between default on payment based on different range of balance limit for credit card users. 
                
        **Observation:** The highest bar is for the 0-50K range, with just over 0.35 defaults and Very few defaults are observed for ranges above 400K-450K.
                
        **Trend:** There's a clear downward trend in the number of defaults as the credit limit increases.
        
        The relationship appears to be inverse and non-linear, with a sharp drop-off in defaults as credit limits increase.
    """)

    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')  

    st.pyplot(fig)

def default_payment_by_age():
    df = pd.read_csv('artifacts/data_ingestion/default.csv')
    data = df[["LIMIT_BAL", "AGE", "default.payment.next.month"]]

    bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
    labels = ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30", "30-35", "35-40", "40-45", "45-50",
              "50-55", "55-60", "60-65", "65-70", "70-75", "75-80"]
    
    data["AGE_RANGE"] = pd.cut(data["AGE"], bins=bins, labels=labels)

    default_counts = data[data["default.payment.next.month"] == 1]["AGE_RANGE"].value_counts().sort_index()
    total_default_count = data[data["default.payment.next.month"] == 1]["default.payment.next.month"].value_counts()
    
    for x in range(len(default_counts)):
        answer = default_counts[x] / total_default_count
        default_counts[x] = answer

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(default_counts.index, default_counts.values, color='skyblue')
    plt.xlabel('AGE Range', fontsize=14)
    plt.ylabel('Number of Defaults', fontsize=14)
    plt.title('Number of Defaults by AGE Range', fontsize=16)
    plt.xticks(rotation=45, ha='right', fontsize=6)
  
    ax.axis('tight')
    plt.show()

    st.subheader('Default Payment by Age')
    
    st.markdown("""
        The graph shows the relationship between default on payment based on different range for the age of credit card users. 
                
        **Observation:** 
        
        - The highest number of defaults (around 0.22) occurs in the 25-30 age group. 
        - There's a sharp increase in defaults from the 20-25 to the 25-30 age group. 
        - After the peak, there's a gradual decrease in defaults as age increases.
        - Very low numbers of defaults are observed for age groups above 60.
        - No data is shown for age groups below 20, suggesting either no defaults or no customers in these younger age ranges.
                
        **Trend:** The number of defaults appears to peak in the 25-30 age range and then generally decreases as age increases.
                
        This graph suggests that younger adults, particularly those in their late 20s, have the highest rate of defaults, while older individuals tend to have fewer defaults. This could imply that financial stability generally improves with age, or that lending practices differ for different age groups.
    """)

    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')  

    st.pyplot(fig)

def run():
    with st.sidebar:

        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.markdown("""
        <div style="padding: 10px; border: 2px solid #ffffff; border-radius: 15px; background-color: #0E1117; color: #ffffff;">
        Get useful information about some common trends and patterns of data 📊
        </div>
        """, unsafe_allow_html=True)

    st.header('Insights')  
    tab1, tab2 = st.tabs(['Default Payment by Credit Limit', 'Default Payment by Age'])

    with tab1:  
        default_payment_by_credit_limit()

    with tab2:
        default_payment_by_age()
    