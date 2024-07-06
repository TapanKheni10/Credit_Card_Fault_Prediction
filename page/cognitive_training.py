import streamlit as st
import subprocess

def run():
    with st.sidebar:

        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.markdown("""
        <div style="padding: 10px; border: 2px solid #ffffff; border-radius: 15px; background-color: #0E1117; color: #ffffff;">
        Train the Model 🤖 by Yourself
        </div>
        """, unsafe_allow_html=True)

    st.header("Credit Card Fault Model Trainer", divider="rainbow")
    st.write("""
        Initiate the model training process by clicking the 'Start' button. 
        Please be aware that the duration of this training may vary, depending on the performance specifications of your device.
        
        Generally speaking, the training process may take up to 20 to 25 minutes. 
        
        Thank you for your patience..
    """)

    if st.button("Start"):
        st.write("Magic is happening.......")

        with st.spinner("🧠 Training the model..."):
            subprocess.run(["python","main.py"])

            st.success("Model training completed.")