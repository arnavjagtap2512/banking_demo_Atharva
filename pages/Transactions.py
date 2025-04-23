import streamlit as st
import pandas as pd
import os
import datetime
import plotly.express as px
import plotly.graph_objects as go
from math import ceil
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Set page configuration
st.set_page_config(
    page_title="BankTech AI Suite - Transactions",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"  # Show sidebar by default
)

# Remove just the hamburger menu but keep the sidebar
st.markdown("""
<style>
    #MainMenu {
        visibility: hidden;
    }
    
    /* Header styling */
    .header-container {
        background-color: #1e3a8a;
        padding: 1.5rem;
        border-radius: 0.5rem;
        color: white;
        margin-bottom: 1rem;
    }
    
    .stPagination {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 1rem;
    }
    
    .page-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1rem;
    }
    
    .page-info {
        font-size: 0.9rem;
        color: #4A5568;
    }
    
    .customer-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .customer-info {
        display: flex;
        flex-direction: column;
    }
    
    .customer-name {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0A2559;
        margin-bottom: 0.5rem;
    }
    
    .customer-details {
        color: #4A5568;
        font-size: 1rem;
    }
    
    .report-button {
        background-color: #0A2559;
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 4px;
        font-weight: 500;
        cursor: pointer;
        border: none;
        transition: background-color 0.3s;
    }
    
    .report-button:hover {
        background-color: #183C7E;
    }
    
    .charts-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .chart-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0A2559;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# Add custom CSS
st.markdown("""
<style>
    .dashboard-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0A2559;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E2E8F0;
    }
    
    .section-description {
        color: #4A5568;
        margin-bottom: 1.5rem;
        font-size: 1.05rem;
        line-height: 1.5;
        max-width: 100%;
    }
    
    .search-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .search-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2D3748;
        margin-bottom: 1rem;
    }
    
    .ai-report {
        line-height: 1.8;
        font-family: sans-serif;
        word-spacing: normal;
        white-space: normal;
    }

    .ai-report p {
        margin-bottom: 1rem;
    }

    .ai-report h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0A2559;
        margin-bottom: 1rem;
    }
    
    .table-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .footer {
        text-align: center;
        color: #718096;
        padding-top: 2rem;
        font-size: 0.9rem;
    }
    
    .btn-primary {
        background-color: #0A2559;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        border: none;
        font-weight: 500;
        cursor: pointer;
    }
    
    .btn-primary:hover {
        background-color: #183C7E;
    }
    
    .btn-secondary {
        background-color: #F7FAFC;
        color: #2D3748;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        border: 1px solid #E2E8F0;
        font-weight: 500;
        cursor: pointer;
    }
    
    .btn-secondary:hover {
        background-color: #EDF2F7;
    }
    
    .pagination-btn {
        background-color: #F7FAFC;
        color: #2D3748;
        width: 40px;
        height: 40px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 500;
        cursor: pointer;
        border: 1px solid #E2E8F0;
        font-size: 1.2rem;
    }
    
    .pagination-btn:hover {
        background-color: #EDF2F7;
    }
    
    .pagination-btn.disabled {
        background-color: #F7FAFC;
        color: #CBD5E0;
        cursor: not-allowed;
    }
    
    .pagination-btn.active {
        background-color: #0A2559;
        color: white;
        border: none;
    }
    
    hr {
        margin: 1rem 0;
        border-top: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# Function to load and process data
@st.cache_data
def load_data():
    try:
        # Try to load from the /data directory (relative path)
        df = pd.read_csv("data/transactions.csv")
        return df
    except FileNotFoundError:
        try:
            # Try with absolute path
            df = pd.read_csv("/data/transactions.csv")
            return df
        except FileNotFoundError:
            # If data file doesn't exist yet, return a dummy dataframe
            st.error("Transaction data file not found. Please ensure the CSV file is in the correct location.")
            # Create a dummy dataframe with the expected columns
            columns = [
                "Transaction_ID", "Customer_ID", "Name", "Age", "Income", "Credit_Score", 
                "Account_Type", "Existing_Loan", "EMI_Amount", "Credit_Utilization", 
                "Default_History", "Transaction_Date", "Transaction_Amount", "Transaction_Type", 
                "Description", "Unusual_Transaction", "Transaction_Location", 
                "Bank_Ledger_Amount", "Reconciliation_Status", "Bulk_Payment_Type"
            ]
            return pd.DataFrame(columns=columns)

def search_data(df, search_term, search_by):
    """
    Search the dataframe based on the search term and column
    """
    if not search_term:
        return df
    
    if search_by == "Transaction ID":
        try:
            search_term = int(search_term)
            return df[df["Transaction_ID"] == search_term]
        except ValueError:
            st.warning("Transaction ID should be a number")
            return df
    
    elif search_by == "Customer ID":
        try:
            search_term = int(search_term)
            return df[df["Customer_ID"] == search_term]
        except ValueError:
            st.warning("Customer ID should be a number")
            return df
    
    elif search_by == "Name":
        return df[df["Name"].str.contains(search_term, case=False)]
    
    return df

def sort_data(df, sort_by):
    """
    Sort the dataframe based on the selected column
    """
    if sort_by:
        return df.sort_values(by=sort_by)
    return df

def paginate_data(df, page, rows_per_page=100):
    """
    Return a slice of the dataframe for the current page
    """
    start_idx = (page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    return df.iloc[start_idx:end_idx]

def get_customer_info(df):
    """
    Extract unique customer information from the dataframe
    """
    if len(df) > 0:
        # Get the first row for customer details
        customer_id = df["Customer_ID"].iloc[0]
        customer_name = df["Name"].iloc[0]
        customer_age = df["Age"].iloc[0]
        return customer_id, customer_name, customer_age
    return None, None, None

def generate_ai_report(df, customer_name):
    """
    Generate an AI report using Google's Gemini model based on transaction data
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Configure the Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "AI report generation failed: API key not found. Please check your .env file."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Extract relevant data for the report
        total_transactions = len(df)
        total_amount = df["Transaction_Amount"].sum()
        avg_amount = df["Transaction_Amount"].mean()
        max_transaction = df["Transaction_Amount"].max()
        credit_count = len(df[df["Transaction_Type"] == "Credit"])
        debit_count = len(df[df["Transaction_Type"] == "Debit"])
        credit_sum = df[df["Transaction_Type"] == "Credit"]["Transaction_Amount"].sum()
        debit_sum = df[df["Transaction_Type"] == "Debit"]["Transaction_Amount"].sum()
        net_balance = credit_sum - debit_sum
        locations = df["Transaction_Location"].value_counts().to_dict()
        
        # Create a prompt for the AI with explicit formatting instructions
        prompt = f"""
        Generate a structured banking analysis report for customer {customer_name} based on the following transaction data:
        
        - Total Transactions: {total_transactions}
        - Total Transaction Amount: ₹{int(total_amount)}
        - Average Transaction Amount: ₹{int(avg_amount)}
        - Maximum Transaction Amount: ₹{int(max_transaction)}
        - Credit Transactions: {credit_count} totaling ₹{int(credit_sum)}
        - Debit Transactions: {debit_count} totaling ₹{int(debit_sum)}
        - Net Balance: ₹{int(net_balance)}
        - Transaction Locations: {locations}
        
        IMPORTANT FORMATTING RULES:
        1. Use the ₹ symbol for all currency values
        2. Always include spaces between numbers and words
        3. Do NOT run words together
        4. For example, write "over the analyzed period" NOT "overtheanalyzedperiod"
        5. Write "compared to 1 credit transaction of" NOT "comparedto1credittransactionof"
        6. Write "The average transaction amount is" NOT "Theaverage..."
        
        Please organize your report in this exact format with numbering:
        
        ## Banking Analysis Report for {customer_name}
        
        #### 1. Summary:
        [Write summary here with proper spacing between numbers and words]
        
        #### 2. Spending Habits & Financial Behavior:
        [Write analysis here with proper spacing between numbers and words]
        
        #### 3. Loan Recommendations:
        [Write recommendations here with proper spacing between numbers and words]
        
        #### 4. Notable Patterns:
        [Write patterns here with proper spacing between numbers and words]
        """
        
        # Generate the report
        response = model.generate_content(prompt)
        report = response.text
        
        # Post-process the report to fix any remaining spacing issues
        import re
        
        # Fix common patterns where words run together after numbers
        report = re.sub(r'(\d+)([a-zA-Z])', r'\1 \2', report)
        
        # Fix other common patterns
        patterns = [
            (r'over\s*the\s*analyzed\s*period', 'over the analyzed period'),
            (r'The\s*average', 'The average'),
            (r'compared\s*to', 'compared to'),
            (r'resulting\s*in', 'resulting in'),
            (r'indicates\s*a', 'indicates a'),
            (r'with\s*an', 'with an'),
            (r'of\s*₹', 'of ₹'),
            (r'balance\s*of', 'balance of')
        ]
        
        for pattern, replacement in patterns:
            report = re.sub(pattern, replacement, report, flags=re.IGNORECASE)
        
        return report
    
    except Exception as e:
        return f"AI report generation failed: {str(e)}"
    
def generate_transaction_type_chart(df):
    """
    Generate a pie chart of Credit vs Debit transactions
    """
    # For this example, we'll use Transaction_Type column
    # In a real scenario, you might need to categorize transactions
    # based on whether Transaction_Amount is positive or negative
    transaction_counts = df["Transaction_Type"].value_counts().reset_index()
    transaction_counts.columns = ["Type", "Count"]
    
    # If Transaction_Type doesn't have Credit/Debit values, simulate them
    if len(transaction_counts) < 1:
        transaction_counts = pd.DataFrame({
            "Type": ["Credit", "Debit"],
            "Count": [len(df) * 0.7, len(df) * 0.3]  # 70% Credit, 30% Debit as example
        })
    
    fig = px.pie(
        transaction_counts, 
        values="Count", 
        names="Type",
        title="Credit vs Debit Transactions",
        color_discrete_sequence=["#1A365D", "#4299E1"],
        hole=0.3
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=350,  # Increased height
        showlegend=True,
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=-0.2,  # Adjusted to accommodate larger chart
            xanchor="center", 
            x=0.5
        ),
        font=dict(size=14)  # Larger font size
    )
    
    # Add percentage labels inside the pie slices
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=14,
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    
    return fig

def generate_transaction_amount_chart(df):
    """
    Generate a bar chart of Transaction_Date vs Transaction_Amount
    """
    # Ensure the date is properly formatted and sorted
    df_copy = df.copy()
    df_copy["Transaction_Date"] = pd.to_datetime(df_copy["Transaction_Date"])
    df_copy = df_copy.sort_values("Transaction_Date")
    
    # Create a color scale based on transaction amount
    fig = px.bar(
        df_copy,
        x="Transaction_Date",
        y="Transaction_Amount",
        title="Transaction Amount by Date",
        labels={"Transaction_Date": "Date", "Transaction_Amount": "Amount"},
        color="Transaction_Amount",  # Color bars by amount
        color_continuous_scale="Viridis",  # More vibrant color scale
        template="plotly_white"  # Use a cleaner template
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=350,  # Increased height
        xaxis=dict(
            tickangle=-45,
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(
            title="Amount",
            thicknessmode="pixels", thickness=20,
            lenmode="pixels", len=300,
            yanchor="top", y=1,
            ticks="outside"
        ),
        title_font=dict(size=16)
    )
    
    # Add hover information
    fig.update_traces(
        hovertemplate="<b>Date:</b> %{x}<br><b>Amount:</b> %{y:,.2f}<extra></extra>"
    )
    
    return fig

def generate_location_chart(df):
    """
    Generate a donut chart of Transaction_Location
    """
    location_counts = df["Transaction_Location"].value_counts().reset_index()
    location_counts.columns = ["Location", "Count"]
    
    # If there are many locations, limit to top 6 for better visibility
    if len(location_counts) > 6:
        other_sum = location_counts.iloc[6:]["Count"].sum()
        top_locations = location_counts.iloc[:6].copy()
        if other_sum > 0:
            other_row = pd.DataFrame({"Location": ["Other"], "Count": [other_sum]})
            location_counts = pd.concat([top_locations, other_row], ignore_index=True)
        else:
            location_counts = top_locations
    
    # Use distinct colors for better visibility
    color_palette = [
        "#3366CC", "#DC3912", "#FF9900", "#109618", "#990099", "#0099C6", "#DD4477"
    ]
    
    fig = px.pie(
        location_counts,
        values="Count",
        names="Location",
        title="Transactions by Location",
        hole=0.5,
        color_discrete_sequence=color_palette
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,  # Increased height even more
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="right",
            x=1.1,  # Move legend further right
            font=dict(size=14),
            itemsizing="constant"  # Equal-sized legend items
        ),
        font=dict(size=14),
        title_font=dict(size=18)
    )
    
    # Add percentage and value labels
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=14,
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    
    return fig

def main():
    # Track previous search for resetting report state when customer changes
    if 'previous_search' not in st.session_state:
        st.session_state.previous_search = None
    
    st.markdown("""
                <div class="header-container">
                    <h1>Transaction Records</h1>
                    <p>Generate comprehensive financial reports with AI-powered insights and tailored recommendations</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Description
    st.markdown("""
    <div class="section-description">
        This page displays all transaction records from the bank's database. 
        Use the search functionality to find specific transactions by Transaction ID, Customer ID, or customer name. 
        You can also sort the data by various parameters to identify patterns or focus on specific customer segments. 
        The table shows 100 records per page with pagination controls at the bottom.
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Search and filter section
    #st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.markdown('<div class="search-title">Search & Filter Transactions</div>', unsafe_allow_html=True)
    
    # Create two columns for search and sort
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Search section
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            search_term = st.text_input("Search", placeholder="Enter search term...")
        with search_col2:
            search_by = st.selectbox(
                "Search by", 
                options=["Transaction ID", "Customer ID", "Name"],
                index=1  # Default to Customer ID
            )
    
    with col2:
        # Sort section
        sort_by = st.selectbox(
            "Sort by",
            options=["Age", "Income", "Credit_Score", "Transaction_Date", "Transaction_Amount"],
            index=4  # Default to Transaction_Amount
        )
    
    #st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply search and sort
    filtered_df = search_data(df, search_term, search_by)
    sorted_df = sort_data(filtered_df, sort_by)
    
    # Initialize session state for report visibility if not exists
    if 'show_report' not in st.session_state:
        st.session_state.show_report = False
    
    # Get customer information if search results exist
    customer_id, customer_name, customer_age = get_customer_info(filtered_df)
    
    # Check if customer has changed - if so, reset the report state
    current_search = f"{search_by}:{search_term}"
    if current_search != st.session_state.previous_search:
        st.session_state.show_report = False
        st.session_state.previous_search = current_search
    
    # Display customer information and report button if customer exists
    if customer_id is not None:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div class="customer-card">
                <div class="customer-info">
                    <div class="customer-name">{customer_name}</div>
                    <div class="customer-details">Customer ID: {customer_id} | Age: {customer_age}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Report Button - improved styling
            if st.button("Generate Report", type="primary", use_container_width=True):
                st.session_state.show_report = True

    # Display AI Report and charts if button is clicked and we have data
    if st.session_state.show_report and len(filtered_df) > 0:
        # Generate and display AI report
        with st.spinner("Generating AI analysis..."):
            ai_report = generate_ai_report(filtered_df, customer_name)
            
        st.markdown('<div class="charts-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">AI-Generated Insights</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Let Streamlit render the markdown properly
        st.markdown(ai_report)
        
        # Display the charts (existing code)
        st.markdown('<div class="charts-container">', unsafe_allow_html=True)
        
        # First row - bar chart (full width)
        st.subheader("Transaction Analysis")
        
        # Bar Chart: Transaction Date vs Amount (full width for better visibility)
        bar_chart = generate_transaction_amount_chart(filtered_df)
        st.plotly_chart(bar_chart, use_container_width=True)
        
        # Second row - pie charts (two columns)
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie Chart: Credit/Debit
            pie_chart = generate_transaction_type_chart(filtered_df)
            st.plotly_chart(pie_chart, use_container_width=True)
        
        with col2:
            # Donut Chart: Transaction Location
            donut_chart = generate_location_chart(filtered_df)
            st.plotly_chart(donut_chart, use_container_width=True)
        
        # Add a button to hide report if needed
        if st.button("Hide Report", type="secondary"):
            st.session_state.show_report = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Pagination
    rows_per_page = 100
    total_pages = max(1, ceil(len(sorted_df) / rows_per_page))
    
    # Initialize page number in session state if not exists
    if 'page_num' not in st.session_state:
        st.session_state.page_num = 1
    
    # Ensure page number is valid after filtering
    if st.session_state.page_num > total_pages:
        st.session_state.page_num = 1
    
    # Display the current page of data
    current_page_data = paginate_data(sorted_df, st.session_state.page_num, rows_per_page)
    
    # Table container
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    
    # Display the table
    st.dataframe(
        current_page_data,
        hide_index=True,
        use_container_width=True
    )
    
    # Pagination controls
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("< Previous", disabled=(st.session_state.page_num == 1)):
            st.session_state.page_num -= 1
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div class="page-info" style="text-align: center;">
            Page {st.session_state.page_num} of {total_pages} 
            ({len(filtered_df)} records found)
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("Next >", disabled=(st.session_state.page_num == total_pages)):
            st.session_state.page_num += 1
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown('<div class="footer">© 2025 BankTech AI Suite. All rights reserved.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()