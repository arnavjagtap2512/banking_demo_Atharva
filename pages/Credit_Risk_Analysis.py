import streamlit as st
import pandas as pd
import numpy as np
import io

# Set page config
st.set_page_config(page_title="Credit Risk Analysis", layout="wide")

# Custom CSS to style the app
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #F8F9FA;
        padding: 20px;
    }
    
    /* Header styling */
    .header-container {
        background-color: #1e3a8a;
        padding: 1.5rem;
        border-radius: 0.5rem;
        color: white;
        margin-bottom: 1rem;
    }
    
    /* Cards styling */
    .stCardContainer {
        border-radius: 10px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #273044;
    }
    
    /* Metrics */
    .metric-card {
        background-color: #f0f2f5;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }
    
    .metric-label {
        color: #6c757d;
        font-size: 14px;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 22px;
        font-weight: bold;
    }
    
    /* Risk scores */
    .risk-high {
        color: #dc3545;
    }
    
    .risk-medium {
        color: #ffc107;
    }
    
    .risk-low {
        color: #28a745;
    }
    
    /* Customer profile styling */
    .customer-name {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .profile-section {
        margin-bottom: 5px;
    }
    
    .profile-label {
        color: #6c757d;
        font-size: 14px;
    }
    
    .profile-value {
        font-size: 16px;
        font-weight: bold;
    }
    
    /* Progress bar styling */
    .progress-container {
        width: 100%;
        height: 10px;
        background-color: #e9ecef;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    
    .progress-bar-high {
        height: 100%;
        border-radius: 5px;
        background-color: #dc3545;
    }
    
    .progress-bar-medium {
        height: 100%;
        border-radius: 5px;
        background-color: #ffc107;
    }
    
    .progress-bar-low {
        height: 100%;
        border-radius: 5px;
        background-color: #28a745;
    }
    
    /* Alert icon */
    .risk-alert {
        color: #dc3545;
        margin-right: 5px;
    }
    
    /* Search and filters */
    .search-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Risk tag */
    .risk-tag {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        color: white;
    }
    
    .high-risk-tag {
        background-color: #dc3545;
    }
    
    .medium-risk-tag {
        background-color: #ffc107;
    }
    
    .low-risk-tag {
        background-color: #28a745;
    }
    
    /* Divider */
    .divider {
        border-top: 1px solid #e9ecef;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

def calculate_risk_score(customer):
    """Calculate a risk score based on customer data"""
    score = 0
    
    # Credit score factor (max 40 points)
    if customer['Credit_Score'] >= 750:
        score += 40
    elif customer['Credit_Score'] >= 700:
        score += 30
    elif customer['Credit_Score'] >= 650:
        score += 20
    elif customer['Credit_Score'] >= 600:
        score += 10
    
    # Income factor (max 25 points)
    if customer['Income'] >= 100000:
        score += 25
    elif customer['Income'] >= 75000:
        score += 20
    elif customer['Income'] >= 50000:
        score += 15
    elif customer['Income'] >= 30000:
        score += 10
    else:
        score += 5
    
    # Credit utilization (max 15 points)
    credit_util = customer['Credit_Utilization']
    if credit_util <= 0.1:
        score += 15
    elif credit_util <= 0.3:
        score += 12
    elif credit_util <= 0.5:
        score += 8
    elif credit_util <= 0.7:
        score += 4
    
    # Default history (max 20 points)
    if customer['Default_History'] == 'No':
        score += 20
    
    return score

def get_risk_category(score):
    """Get risk category and styling based on score"""
    if score >= 80:
        return "Low Risk", "risk-low", "low-risk-tag"
    elif score >= 60:
        return "Medium Risk", "risk-medium", "medium-risk-tag"
    else:
        return "High Risk", "risk-high", "high-risk-tag"

def get_credit_score_category(score):
    """Get credit score category and styling"""
    if score >= 750:
        return "Excellent", "risk-low"
    elif score >= 700:
        return "Good", "risk-low"
    elif score >= 650:
        return "Fair", "risk-medium"
    elif score >= 600:
        return "Poor", "risk-medium"
    else:
        return "Very Poor", "risk-high"

def format_currency(value):
    """Format a number as currency"""
    return f"₹{value:,.0f}"

def main():
    # Heading
    st.markdown("""
                <div class="header-container">
                    <h1>Credit Risk Analysis</h1>
                    <p>Leverage advanced AI algorithms to assess credit scores with precision and predict potential loan defaults before they occur</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.write("""
        This Credit Risk Analysis tool helps bank professionals assess borrower risk profiles and make informed lending decisions. 
        Upload customer data to analyze credit scores, income levels, and default history. The system calculates risk scores 
        and provides key risk indicators to streamline the loan evaluation process and identify potential high-risk borrowers.
        """)
    
    # File uploader
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is not None:
        # Load and process data
        try:
            df = pd.read_csv(uploaded_file)
            
            # Convert Credit_Utilization to float if it's not already
            if 'Credit_Utilization' in df.columns:
                df['Credit_Utilization'] = df['Credit_Utilization'].astype(float)
            
            # Get unique customers
            unique_customers = df.drop_duplicates(subset=['Customer_ID']).copy()
            
            # Calculate risk metrics for dashboard
            avg_credit_score = int(unique_customers['Credit_Score'].mean())
            default_count = len(unique_customers[unique_customers['Default_History'] == 'Yes'])
            default_rate = int((default_count / len(unique_customers)) * 100)
            high_risk_count = len(unique_customers[unique_customers['Credit_Score'] < 600])
            high_risk_perc = int((high_risk_count / len(unique_customers)) * 100)
            avg_credit_util = round(unique_customers['Credit_Utilization'].mean() * 100, 1)
            
            # Dashboard metrics row
            st.markdown("### Portfolio Overview")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.markdown("""
                <div class="metric-card" style="background-color: #e6f0ff;">
                    <div class="metric-label">Average Credit Score</div>
                    <div class="metric-value">{}</div>
                </div>
                """.format(avg_credit_score), unsafe_allow_html=True)
                
            with col2:
                st.markdown("""
                <div class="metric-card" style="background-color: #ffe6e6;">
                    <div class="metric-label">Default Rate</div>
                    <div class="metric-value">{}%</div>
                </div>
                """.format(default_rate), unsafe_allow_html=True)
                
            with col3:
                st.markdown("""
                <div class="metric-card" style="background-color: #fff5e6;">
                    <div class="metric-label">High Risk Customers</div>
                    <div class="metric-value">{}%</div>
                </div>
                """.format(high_risk_perc), unsafe_allow_html=True)
                
            with col4:
                st.markdown("""
                <div class="metric-card" style="background-color: #e6ffe6;">
                    <div class="metric-label">Avg Credit Utilization</div>
                    <div class="metric-value">{}%</div>
                </div>
                """.format(avg_credit_util), unsafe_allow_html=True)
                
            with col5:
                st.markdown("""
                <div class="metric-card" style="background-color: #f0e6ff;">
                    <div class="metric-label">Approval Ratio</div>
                    <div class="metric-value">65%</div>
                </div>
                """.format(), unsafe_allow_html=True)
            
            # Search and filter section
            st.markdown("### Search & Filter Transactions")
            col1, col2 = st.columns([3, 1])
            
            with col1:
                search_term = st.text_input("Search", placeholder="Enter search term...")
            
            with col2:
                search_by = st.selectbox("Search by", options=["Customer ID", "Name"], index=0)
            
            # Filter data based on search
            filtered_customers = unique_customers
            if search_term:
                if search_by == "Customer ID":
                    filtered_customers = unique_customers[unique_customers['Customer_ID'].astype(str).str.contains(search_term)]
                elif search_by == "Name":
                    filtered_customers = unique_customers[unique_customers['Name'].str.contains(search_term, case=False)]
            
            # Display search results
            if not filtered_customers.empty:
                # Take just the first result for demo purposes
                selected_customer = filtered_customers.iloc[0]
                
                st.markdown(f"""
                <div class="stCardContainer">
                    <div class="customer-name">{selected_customer['Name']}</div>
                    <div>Customer ID: {selected_customer['Customer_ID']} | Age: {selected_customer['Age']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Customer profile and risk assessment columns
                col1, col2 = st.columns(2)
                
                # Calculate risk score for the customer
                risk_score = calculate_risk_score(selected_customer)
                risk_category, risk_color_class, risk_tag_class = get_risk_category(risk_score)
                credit_category, credit_color_class = get_credit_score_category(selected_customer['Credit_Score'])
                default_probability = 100 - risk_score
                
                # Maximum loan amount calculation (simple formula for demonstration)
                max_loan = round((risk_score / 100) * selected_customer['Income'] * 3)
                
                # Customer Profile Card
                with col1:
                    st.subheader("🏦 Customer Profile")
                    st.markdown(f"## {selected_customer['Name']}")
                    
                    st.markdown("**Customer ID**")
                    st.markdown(f"{selected_customer['Customer_ID']}")
                    
                    st.markdown("**Age**")
                    st.markdown(f"{selected_customer['Age']}")
                    
                    st.markdown("**Income**")
                    st.markdown(f"{format_currency(selected_customer['Income'])}")
                    
                    st.markdown("**Credit Score**")
                    credit_category, credit_color = get_credit_score_category(selected_customer['Credit_Score'])
                    credit_color_hex = "#dc3545" if "high" in credit_color else "#28a745"
                    st.markdown(f"<span style='color: {credit_color_hex};'>{selected_customer['Credit_Score']} - {credit_category}</span>", unsafe_allow_html=True)
                    
                    st.markdown("**Credit Utilization**")
                    util_color = "#dc3545" if selected_customer['Credit_Utilization'] > 0.7 else "#28a745"
                    st.markdown(f"<span style='color: {util_color};'>{selected_customer['Credit_Utilization'] * 100:.1f}%</span>", unsafe_allow_html=True)
                    
                    st.markdown("**Existing Loan**")
                    st.markdown(f"{selected_customer['Existing_Loan']}")
                    
                    st.markdown("**Default History**")
                    default_color = "#dc3545" if selected_customer['Default_History'] == 'Yes' else "#28a745"
                    st.markdown(f"<span style='color: {default_color};'>{selected_customer['Default_History']}</span>", unsafe_allow_html=True)
                
                # Risk Assessment Card
                with col2:
                    st.subheader("⚠️ Risk Assessment")
                    
                    st.markdown("**Risk Score**")
                    risk_category, risk_color_class, risk_tag_class = get_risk_category(risk_score)
                    
                    # Create columns for score and tag
                    score_col, tag_col = st.columns([1, 1])
                    with score_col:
                        risk_color_hex = "#dc3545" if risk_score < 60 else "#ffc107" if risk_score < 80 else "#28a745"
                        st.markdown(f"<span style='color: {risk_color_hex}; font-size: 24px; font-weight: bold;'>{risk_score}</span>", unsafe_allow_html=True)
                    
                    with tag_col:
                        tag_bg_color = "#dc3545" if risk_score < 60 else "#ffc107" if risk_score < 80 else "#28a745"
                        st.markdown(f"<span style='background-color: {tag_bg_color}; color: white; padding: 4px 12px; border-radius: 16px; font-weight: bold;'>{risk_category}</span>", unsafe_allow_html=True)
                    
                    # Progress bar
                    st.progress(risk_score/100)
                    
                    st.markdown("**Default Probability**")
                    default_probability = 100 - risk_score
                    default_color = "#dc3545" if default_probability > 30 else "#28a745"
                    st.markdown(f"<span style='color: {default_color};'>{default_probability}%</span>", unsafe_allow_html=True)
                    
                    st.markdown("**Recommended Max Loan**")
                    max_loan = round((risk_score / 100) * selected_customer['Income'] * 3)
                    st.markdown(f"{format_currency(max_loan)}")
                    
                    st.markdown("---")
                    
                    st.markdown("**Key Risk Factors:**")
                    
                    if selected_customer['Credit_Score'] < 650:
                        st.markdown("⚠️ Low credit score")
                    
                    if selected_customer['Credit_Utilization'] > 0.7:
                        st.markdown("⚠️ High credit utilization")
                    
                    if selected_customer['Default_History'] == 'Yes':
                        st.markdown("⚠️ Previous default history")
                    
                    if selected_customer['Income'] < 30000:
                        st.markdown("⚠️ Low income")
                    
                    # If no significant risk factors
                    if (selected_customer['Credit_Score'] >= 650 and 
                        selected_customer['Credit_Utilization'] <= 0.7 and 
                        selected_customer['Default_History'] == 'No' and
                        selected_customer['Income'] >= 30000):
                        st.markdown("✅ No significant risk factors")
                
                # End of display for customer
                
            else:
                st.info("No customers found matching your search criteria.")
        
        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.info("Please upload a CSV file to begin credit risk analysis.")

if __name__ == "__main__":
    main()