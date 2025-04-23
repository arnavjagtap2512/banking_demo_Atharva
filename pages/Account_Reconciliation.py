import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="BankTech AI Suite - Account Reconciliation",
    page_icon="📊",
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
        
        /* Error message */
        .error-message {
            background-color: #fee2e2;
            border-left: 4px solid #ef4444;
            padding: 1rem;
            border-radius: 0.25rem;
            margin: 1rem 0;
        }
        
        /* File upload styling */
        .upload-container {
            background-color: #f3f4f6;
            border: 2px dashed #d1d5db;
            border-radius: 0.5rem;
            padding: 2rem;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        /* Status indicator styling */
        .status-matched {
            background-color: #d1fae5;
            color: #047857;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-weight: 500;
        }
        
        .status-unmatched {
            background-color: #fee2e2;
            color: #b91c1c;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-weight: 500;
        }
        
        /* Summary card styling */
        .summary-card {
            padding: 1rem;
            border-radius: 0.5rem;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .summary-card h3 {
            margin-top: 0;
            font-size: 1.25rem;
        }
        
        .summary-card p {
            font-size: 2rem;
            font-weight: bold;
            margin: 0.5rem 0;
        }
        
        .summary-matched {
            background-color: #d1fae5;
        }
        
        .summary-unmatched {
            background-color: #fee2e2;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Header
st.markdown("""
<div class="header-container">
    <h1>Account Reconciliation</h1>
    <p>Match bank ledger transactions with customer records to identify discrepancies</p>
</div>
""", unsafe_allow_html=True)

# Session State Initialization
if 'bank_ledger' not in st.session_state:
    st.session_state.bank_ledger = None
if 'customer_records' not in st.session_state:
    st.session_state.customer_records = None
if 'reconciliation_results' not in st.session_state:
    st.session_state.reconciliation_results = None
if 'comparison_done' not in st.session_state:
    st.session_state.comparison_done = False

# File Upload Section
#st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Upload Transaction Files")

col1, col2 = st.columns(2)

with col1:
    #st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    st.subheader("Upload Bank Ledger")
    bank_ledger_file = st.file_uploader("Bank ledger file (CSV)", type=["csv"], key="bank_ledger_uploader")
    if bank_ledger_file is not None:
        try:
            bank_ledger = pd.read_csv(bank_ledger_file)
            st.session_state.bank_ledger = bank_ledger
            st.success(f"Bank ledger file uploaded successfully with {len(bank_ledger)} records.")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    #st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    st.subheader("Upload Customer Records")
    customer_records_file = st.file_uploader("Customer transaction records (CSV)", type=["csv"], key="customer_records_uploader")
    if customer_records_file is not None:
        try:
            customer_records = pd.read_csv(customer_records_file)
            st.session_state.customer_records = customer_records
            st.success(f"Customer records file uploaded successfully with {len(customer_records)} records.")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Reconciliation Process
#st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Reconciliation Process")

# Check if both files are uploaded
if st.session_state.bank_ledger is not None and st.session_state.customer_records is not None:
    st.write("Both files are uploaded. Click 'Compare Transactions' to start the reconciliation process.")
    
    if st.button("Compare Transactions") or st.session_state.comparison_done:
        st.session_state.comparison_done = True
        
        # Display a spinner while processing
        with st.spinner("Comparing transactions..."):
            # Get the dataframes
            bank_df = st.session_state.bank_ledger
            customer_df = st.session_state.customer_records
            
            # Prepare data for reconciliation - now using Transactions_Amount for comparison
            bank_prepared = bank_df[['Transaction_ID', 'Transactions_Amount']].copy()
            bank_prepared.columns = ['Transaction_ID', 'Bank_Amount']
            
            customer_prepared = customer_df[['Transaction_ID', 'Transaction_Amount']].copy()
            customer_prepared.columns = ['Transaction_ID', 'Customer_Amount']
            
            # Merge the dataframes on Transaction_ID
            merged = pd.merge(bank_prepared, customer_prepared, on='Transaction_ID', how='outer')
            
            # Determine if matched or unmatched based on amounts
            def determine_status(row):
                # If any amount is missing, it's unmatched
                if pd.isna(row['Bank_Amount']) or pd.isna(row['Customer_Amount']):
                    return "Unmatched"
                # If amounts don't match, it's unmatched
                elif row['Bank_Amount'] != row['Customer_Amount']:
                    return "Unmatched"
                # Otherwise, it's matched
                else:
                    return "Matched"
            
            # Apply the status function
            merged['Reconciliation_Status'] = merged.apply(determine_status, axis=1)
            
            # Count statuses
            status_counts = merged['Reconciliation_Status'].value_counts()
            total_records = len(merged)
            
            # Calculate percentages
            status_percentages = {}
            for status in ['Matched', 'Unmatched']:
                count = status_counts.get(status, 0)
                percentage = (count / total_records) * 100 if total_records > 0 else 0
                status_percentages[status] = {
                    'count': count,
                    'percentage': percentage
                }
            
            # Save results to session state
            st.session_state.reconciliation_results = {
                'merged_data': merged,
                'status_counts': status_counts,
                'status_percentages': status_percentages,
                'total_records': total_records
            }
        
        # Display the Reconciliation Summary 
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Reconciliation Summary")
        
        results = st.session_state.reconciliation_results
        merged_data = results['merged_data']
        status_percentages = results['status_percentages']
        
        # Summary cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="summary-card summary-matched">
                <h3>Matched</h3>
                <p>{status_percentages['Matched']['percentage']:.1f}%</p>
                <span>{status_percentages['Matched']['count']} transactions</span>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="summary-card summary-unmatched">
                <h3>Unmatched</h3>
                <p>{status_percentages['Unmatched']['percentage']:.1f}%</p>
                <span>{status_percentages['Unmatched']['count']} transactions</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Pie chart for reconciliation status
        status_data = pd.DataFrame({
            'Status': list(status_percentages.keys()),
            'Percentage': [status_percentages[status]['percentage'] for status in status_percentages],
            'Count': [status_percentages[status]['count'] for status in status_percentages]
        })
        
        # Define colors for the chart
        colors = {
            'Matched': '#047857',  # Green
            'Unmatched': '#b91c1c'  # Red
        }
        
        fig = px.pie(
            status_data, 
            values='Percentage',
            names='Status',
            title='Reconciliation Status Distribution',
            hole=0.5,
            color='Status',
            color_discrete_map=colors
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Filter options and transaction display
        status_filter = st.radio(
            "Filter by Status:",
            options=["All", "Matched", "Unmatched"],
            horizontal=True
        )
        
        # Prepare display data
        merged_display = merged.copy()
        merged_display['Amount_Difference'] = merged_display['Bank_Amount'] - merged_display['Customer_Amount']
        
        # Format amounts for display
        merged_display['Bank_Amount'] = merged_display['Bank_Amount'].apply(
            lambda x: f"₹{x:,.2f}" if not pd.isna(x) else "Not Found"
        )
        merged_display['Customer_Amount'] = merged_display['Customer_Amount'].apply(
            lambda x: f"₹{x:,.2f}" if not pd.isna(x) else "Not Found"
        )
        merged_display['Amount_Difference'] = merged_display['Amount_Difference'].apply(
            lambda x: f"₹{x:,.2f}" if not pd.isna(x) else "N/A"
        )
        
        # Function to highlight rows based on reconciliation status
        def highlight_status(val):
            if val == 'Matched':
                return 'background-color: #d1fae5'
            elif val == 'Unmatched':
                return 'background-color: #fee2e2'
            else:
                return ''
        
        # Filter and display transactions based on selection
        if status_filter != "All":
            filtered_df = merged_display[merged_display['Reconciliation_Status'] == status_filter]
            st.write(f"### {status_filter} Transactions ({len(filtered_df)} records)")
            st.dataframe(
                filtered_df.style.apply(
                    lambda row: [highlight_status(row['Reconciliation_Status'])] * len(row) 
                    if 'Reconciliation_Status' in row else [''] * len(row),
                    axis=1
                ),
                use_container_width=True,
                height=400
            )
        
        # Export options
        st.write("### Export Options")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Export All Records"):
                # This would generate a CSV in a real application
                st.info("Export functionality would be implemented here")
        
        with col2:
            if st.button("Export Unmatched Records"):
                # This would filter and generate a CSV in a real application
                st.info("Export functionality would be implemented here")
                
        st.markdown('</div>', unsafe_allow_html=True)
        
else:
    st.info("Please upload both the Bank Ledger and Customer Records files to begin the reconciliation process.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; border-top: 1px solid #e2e8f0;">
    <p style="color: #4b5563; font-size: 0.875rem;">
        BankTech AI Suite © 2023 | Secure Banking Solutions
    </p>
</div>
""", unsafe_allow_html=True)