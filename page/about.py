import streamlit as st

def run():
    with st.sidebar:

        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.markdown("""
        <div style="padding: 10px; border: 2px solid #ffffff; border-radius: 15px; background-color: #0E1117; color: #ffffff;">
        <p style="text-align: justify; margin: 0 0 15px 0; word-spacing: 3px">
            We welcome your feedback and inquiries! 💡 💬 We're here to help! 🤝
        </p>
        <p style="text-align: justify, margin: 0; word-spacing: 4.5px">
            📬 Don't hesitate to get in touch if you need clarification or have any thoughts to share.🤔
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.header("About Us", divider="rainbow")

    st.write("This is an AI-powered application desinged to help identify whether a particular credit card holder default or not and the transaction is fraudulent or not, to help the lenderers. Our main goal is to leverage the power of machine learning and data analysis to do it.")
    st.write("Our team consists of data scientists and software engineers who are passionate about using technology to make positive impact in the industry.")

    st.subheader("Contact us")
    st.write("For more information or inquiries, please contact us at:")
    st.markdown("""
    <div style="padding: 10px; border: 2px solid #ffffff; border-radius: 5px; background-color: #0E1117; color: #ffffff; width: fit-content;">
    📧 <a href="mailto:tapankheni10304@gmail.com" style="text-decoration: none; color: #ffffff;">tapankheni10304@gmail.com</a>
    </div>
    """, unsafe_allow_html=True)
    st.write("\n")

    st.markdown("""
    <div style="padding: 10px; border: 2px solid #ffffff; border-radius: 5px; background-color: #0E1117; color: #ffffff; width: fit-content;">
    📞 +91 6354541592
    </div>
    """, unsafe_allow_html=True)
    st.write("\n")

    st.subheader("Connect with us")

    st.markdown("""
        <div style='display: flex; justify-content: left; align-items: center;'>
            <a href="https://www.linkedin.com/in/tapan-kheni-145286238/" target="_blank" style="margin-right: 10px;">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/linkedin.svg" alt="LinkedIn" width="32" height="32" style="filter: invert(1)">
            </a>
            <a href="https://twitter.com/tapan_kheni" target="_blank" style="margin-right: 10px;">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/twitter.svg" alt="Twitter" width="32" height="32" style="filter: invert(1)">
            </a>
            <a href="https://github.com/TapanKheni10" target="_blank" style="margin-right: 10px;">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/github.svg" alt="GitHub" width="32" height="32" style="filter: invert(1)">
            </a>
            <a href="https://www.instagram.com/tapan_kheni?igsh=d2dldHp2d3Fuemhr" target="_blank" style="margin-right: 10px;">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/instagram.svg" alt="Instagram" width="32" height="32" style="filter: invert(1)">
            </a>
        </div>
        """, unsafe_allow_html=True)