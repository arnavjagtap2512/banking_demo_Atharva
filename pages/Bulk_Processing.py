import streamlit as st
import pandas as pd
import time
import numpy as np
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="BankTech AI Suite - Bulk Salary Processing",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for styling
def load_css():
    st.markdown("""
    <style>
        /* General styling */
        .main {
            background-color: #f9f9f9;
        }
        
        /* Header styling */
        .header-container {
            background-color: #1e3a8a;
            padding: 1.5rem;
            border-radius: 0.5rem;
            color: white;
            margin-bottom: 1rem;
        }
        
        /* Card styling */
        .card {
            background-color: white;
            border-radius: 0.5rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: #1e3a8a;
            color: white;
            border: none;
            border-radius: 0.25rem;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }
        
        .stButton>button:hover {
            background-color: #2d4eaa;
        }

        /* Table styling */
        .stDataFrame {
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
            overflow: hidden;
        }
        
        /* Success message */
        .success-message {
            background-color: #d1fae5;
            border-left: 4px solid #10b981;
            padding: 1rem;
            border-radius: 0.25rem;
            margin: 1rem 0;
        }
        
        /* Authentication popup */
        .auth-popup {
            background-color: white;
            border-radius: 0.5rem;
            padding: 2rem;
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
            max-width: 500px;
            margin: 0 auto;
            border: 1px solid #e2e8f0;
        }
        
        /* Information banner */
        .info-banner {
            background-color: #e0f2fe;
            border-left: 4px solid #0ea5e9;
            padding: 1rem;
            border-radius: 0.25rem;
            margin: 1rem 0;
        }
        
        /* Checkbox grid */
        .checkbox-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            gap: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Header
st.markdown("""
<div class="header-container">
    <h1>Bulk Salary Processing</h1>
    <p>Upload, verify, and process salary files for multiple employees in one operation</p>
</div>
""", unsafe_allow_html=True)

# Session State Initialization
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'selected_all' not in st.session_state:
    st.session_state.selected_all = False
if 'individual_selections' not in st.session_state:
    st.session_state.individual_selections = {}
if 'auth_required' not in st.session_state:
    st.session_state.auth_required = False
if 'auth_successful' not in st.session_state:
    st.session_state.auth_successful = False
if 'payment_processed' not in st.session_state:
    st.session_state.payment_processed = False
if 'total_amount' not in st.session_state:
    st.session_state.total_amount = 0
if 'total_employees' not in st.session_state:
    st.session_state.total_employees = 0

# File Upload Section
#st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("1. Upload Salary File")
st.markdown("""
Upload a CSV file containing employee salary information. The file should include:
- Employee ID
- Employee Name
- Bank Account Number
- IFSC Code
- Salary Amount
""")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file
    # Read the file
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.session_state.total_amount = df['Salary Amount (INR)'].sum()
        st.session_state.total_employees = len(df)
        # Initialize selections dictionary only if it's empty or size changed
        if len(st.session_state.individual_selections) != len(df):
            st.session_state.individual_selections = {i: False for i in range(len(df))}
        st.success(f"File successfully uploaded with {len(df)} employee records.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
st.markdown('</div>', unsafe_allow_html=True)

# Data Preview Section
if st.session_state.df is not None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("2. Preview Salary Data")
    
    df = st.session_state.df
    
    # Select All option - the only selection method available
    st.checkbox("Select All Records", value=st.session_state.selected_all, key="select_all_master", 
                on_change=lambda: update_all_selections(True if not st.session_state.selected_all else False))
    
    # Function to update all selections when "Select All" is toggled
    def update_all_selections(value):
        st.session_state.selected_all = value
        for i in range(len(df)):
            st.session_state.individual_selections[i] = value
    
    # Apply the "Select All" logic if it's active
    if st.session_state.selected_all:
        for i in range(len(df)):
            st.session_state.individual_selections[i] = True
    
    # Simplify the data display - no need for selection column since we only have "Select All"
    # Add a visual indicator that shows if all records are selected
    if st.session_state.selected_all:
        st.success("All records are selected for processing")
    
    # Display the complete dataframe without selection column
    st.dataframe(df, use_container_width=True, height=600)
    
    # Display metrics about the selection - simplified since we only have "Select All"
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        selected_count = len(df) if st.session_state.selected_all else 0
        st.metric("Selected Records", selected_count)
    with col3:
        selected_amount = df['Salary Amount (INR)'].sum() if st.session_state.selected_all else 0
        st.metric("Total Selected Amount", f"₹{selected_amount:,.2f}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Selection and Processing Section
    #st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("3. Process Payments")
    
    # Remove the individual record selection section entirely
    
    # Process button - simplified since we only have "Select All" option
    process_disabled = not st.session_state.selected_all
    
    if st.session_state.selected_all:
        selected_count = len(df)
        selected_amount = df['Salary Amount (INR)'].sum()
        
        st.markdown(f"""
        <div class="info-banner">
            You are about to process salary payments for <b>{selected_count}</b> employees, 
            totaling <b>₹{selected_amount:,.2f}</b>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-banner">
            Please select all records to continue with payment processing.
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("Process Selected Payments", disabled=process_disabled):
        # Require authentication before processing
        st.session_state.auth_required = True
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Authentication Popup
    if st.session_state.auth_required and not st.session_state.auth_successful:
        #st.markdown('<div class="auth-popup">', unsafe_allow_html=True)
        st.subheader("4. Authentication Required")
        st.markdown(f"""
        <p>You are authorizing a bulk payment of <b>₹{selected_amount:,.2f}</b> to <b>{selected_count}</b> employees.</p>
        <p>Please provide your authentication credentials to proceed.</p>
        """, unsafe_allow_html=True)
        
        auth_username = st.text_input("Username")
        auth_password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Cancel"):
                st.session_state.auth_required = False
                st.rerun()
        
        with col2:
            # In a real application, this would verify credentials against a secure system
            if st.button("Authenticate"):
                if auth_username and auth_password:
                    # Simulate authentication delay
                    with st.spinner("Verifying credentials..."):
                        time.sleep(1.5)
                    st.session_state.auth_successful = True
                    st.session_state.payment_processed = True
                    st.rerun()
                else:
                    st.error("Please fill in all authentication fields")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Payment Confirmation
    if st.session_state.payment_processed:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("5. Payment Confirmation")
        
        # Current date and time
        current_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        transaction_id = "TXN" + datetime.now().strftime("%Y%m%d%H%M%S")
        
        st.markdown(f"""
        <div class="success-message">
            <h3>✅ Bulk Salary Payment Successfully Initiated</h3>
            <p>Transaction ID: <b>{transaction_id}</b></p>
            <p>Processed on: <b>{current_time}</b></p>
            <p>Funds will be credited to the respective accounts within 1-2 hours.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Payment Details
            """)
            details = pd.DataFrame({
                "Item": ["Number of Employees", "Total Amount", "Processing Fee", "Total Debited"],
                "Value": [
                    f"{selected_count}",
                    f"₹{selected_amount:,.2f}",
                    f"₹{0:,.2f}",
                    f"₹{selected_amount:,.2f}"
                ]
            })
            st.table(details)
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("Download Receipt"):
                # In a real application, this would generate a PDF receipt
                st.info("Receipt download functionality would be implemented here")
        
        with col2:
            if st.button("Email Receipt"):
                # In a real application, this would email the receipt
                st.info("Email functionality would be implemented here")
        
        with col3:
            if st.button("New Transaction"):
                # Reset the state to start a new transaction
                for key in ['auth_required', 'auth_successful', 'payment_processed', 'selected_all']:
                    st.session_state[key] = False
                st.session_state.individual_selections = {i: False for i in range(len(df))}
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Display a message if no file is uploaded
if st.session_state.uploaded_file is None:
    st.markdown("""
    <div class="info-banner">
        <p>Please upload a salary CSV file to begin the bulk processing.</p>
        <p>The file should contain employee details and salary information.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; border-top: 1px solid #e2e8f0;">
    <p style="color: #4b5563; font-size: 0.875rem;">
        BankTech AI Suite © 2023 | Secure Banking Solutions
    </p>
</div>
""", unsafe_allow_html=True)