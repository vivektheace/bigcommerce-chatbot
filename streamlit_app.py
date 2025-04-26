import streamlit as st
import requests

# API Configuration
API_URL = "http://localhost:8000/ticket"  # Update if your FastAPI is hosted elsewhere
FAKE_JWT_TOKEN = "your_jwt_token_here"    # Replace with a valid token

st.title("BigCommerce Chatbot - Create a Support Ticket")

st.subheader("Enter Ticket Details")

# Form
with st.form("ticket_form"):
    customer_id = st.text_input("Customer ID")
    issue = st.text_area("Describe the Issue")
    priority = st.selectbox("Priority", ["normal", "high", "urgent"])
    
    submitted = st.form_submit_button("Create Ticket")

    if submitted:
        if not customer_id or not issue:
            st.error("Please fill all the required fields.")
        else:
            payload = {
                "customer_id": customer_id,
                "issue": issue,
                "priority": priority
            }
            headers = {
                "Authorization": f"Bearer {FAKE_JWT_TOKEN}"
            }

            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("✅ Ticket Created Successfully!")
                    st.json(response.json())
                else:
                    st.error(f"❌ Failed: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"❌ Error occurred: {e}")
