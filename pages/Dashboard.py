import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# Set page configuration
st.set_page_config(
    page_title="BankTech AI Suite - Dashboard",
    page_icon="🏦",
    layout="wide"
)

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
    
    /* Header styling */
    .header-container {
        background-color: #1e3a8a;
        padding: 1.5rem;
        border-radius: 0.5rem;
        color: white;
        margin-bottom: 1rem;
    }
    
    .welcome-banner {
        background: linear-gradient(to right, #0A2559, #183C7E);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    
    .welcome-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .welcome-subtitle {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 1.25rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        height: 100%;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #718096;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #0A2559;
    }
    
    .metric-delta {
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }
    
    .positive-delta {
        color: #48BB78;
    }
    
    .negative-delta {
        color: #F56565;
    }
    
    .neutral-delta {
        color: #718096;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2D3748;
        margin: 1.5rem 0 1rem 0;
    }
    
    .module-card {
        background-color: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        height: 100%;
        margin-bottom: 1rem;
    }
    
    .module-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0A2559;
        margin-bottom: 1rem;
    }
    
    .chart-container {
        background-color: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .chart-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2D3748;
        margin-bottom: 1rem;
    }
    
    .footer {
        text-align: center;
        color: #718096;
        padding-top: 2rem;
        font-size: 0.9rem;
    }
    
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0A2559;
        margin: 1rem 0;
    }
    
    .sidebar .stButton button {
        background-color: transparent;
        color: #2D3748;
        text-align: left;
        font-weight: 400;
        padding: 0.5rem 0.75rem;
        border: none;
        border-radius: 4px;
        margin-bottom: 0.25rem;
        width: 100%;
    }
    
    .sidebar .stButton button:hover {
        background-color: #EDF2F7;
    }
    
    .main-content {
        padding: 0 1rem;
    }
    
    hr {
        margin: 1rem 0;
        border-top: 1px solid #E2E8F0;
    }
    
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
    }
    
    [data-testid="stSidebar"] [data-testid="stImage"] {
        text-align: center;
        display: block;
        margin: 1rem auto;
    }
</style>
""", unsafe_allow_html=True)

# Sample data generation functions
def generate_transaction_data():
    # Create a sample dataframe with transaction data
    dates = pd.date_range(start='2025-03-01', end='2025-04-11', freq='D')
    
    # Generate random transaction volumes with a weekly pattern
    import numpy as np
    np.random.seed(42)
    base_volume = np.random.normal(loc=500, scale=50, size=len(dates))
    
    # Add weekly seasonality (lower on weekends)
    weekday_effect = np.array([1.0, 1.1, 1.05, 1.2, 1.3, 0.8, 0.7] * 6)[:len(dates)]
    transaction_volume = base_volume * weekday_effect
    
    # Create the DataFrame
    df = pd.DataFrame({
        'date': dates,
        'transaction_count': transaction_volume.astype(int),
        'total_value': transaction_volume * np.random.uniform(low=100, high=150, size=len(dates))
    })
    
    return df

def generate_fraud_data():
    # Create sample fraud detection data
    categories = ['Card Fraud', 'Identity Theft', 'Account Takeover', 'Loan Fraud', 'Wire Fraud']
    detected = [23, 15, 8, 12, 5]
    false_positives = [3, 2, 1, 2, 1]
    
    df = pd.DataFrame({
        'category': categories,
        'detected': detected,
        'false_positives': false_positives
    })
    
    return df

def generate_credit_data():
    # Create sample credit score distribution
    score_ranges = ['300-500', '501-600', '601-700', '701-800', '801-850']
    percentages = [5, 15, 35, 38, 7]
    
    df = pd.DataFrame({
        'score_range': score_ranges,
        'percentage': percentages
    })
    
    return df

def main():
    # Main content
    st.markdown('<div class="dashboard-header">Banking Operations Dashboard</div>', unsafe_allow_html=True)
    # st.markdown("""
    #             <div class="header-container">
    #                 <h1>Banking Operations Dashboard</h1>
    #             </div>
    #             """, unsafe_allow_html=True)
    
    # Welcome banner
    st.markdown("""
    <div class="welcome-banner">
        <div class="welcome-title">Welcome to BankTech AI Suite</div>
        <div class="welcome-subtitle">Today is {} — Access your banking operations overview below</div>
    </div>
    """.format(datetime.datetime.now().strftime("%A, %B %d, %Y")), unsafe_allow_html=True)
    
    # Key metrics
    st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">TRANSACTIONS TODAY</div>
            <div class="metric-value">4,328</div>
            <div class="metric-delta positive-delta">↑ 7.2% from yesterday</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">RECONCILIATION ACCURACY</div>
            <div class="metric-value">99.8%</div>
            <div class="metric-delta positive-delta">↑ 0.3% from last week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">PENDING APPROVALS</div>
            <div class="metric-value">12</div>
            <div class="metric-delta negative-delta">↑ 3 new since yesterday</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">FRAUD ALERTS</div>
            <div class="metric-value">1</div>
            <div class="metric-delta neutral-delta">No change from yesterday</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Transaction activity chart
    st.markdown('<div class="section-title">Transaction Activity</div>', unsafe_allow_html=True)
    
    transaction_data = generate_transaction_data()
    
    with st.container():
        #st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Daily Transaction Volume</div>', unsafe_allow_html=True)
        
        fig = px.line(
            transaction_data, 
            x='date', 
            y='transaction_count',
            labels={'date': 'Date', 'transaction_count': 'Number of Transactions'},
            line_shape='spline',
            template='plotly_white'
        )
        
        fig.update_traces(line=dict(color='#0A2559', width=3))
        fig.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#E2E8F0')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    
    # Fraud Detection module
    #st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.markdown('<div class="module-title">🛡️ Fraud Detection Overview</div>', unsafe_allow_html=True)
    
    fraud_data = generate_fraud_data()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=fraud_data['category'],
        y=fraud_data['detected'],
        name='Detected Fraud',
        marker_color='#0A2559'
    ))
    
    fig.add_trace(go.Bar(
        x=fraud_data['category'],
        y=fraud_data['false_positives'],
        name='False Positives',
        marker_color='#F56565'
    ))
    
    fig.update_layout(
        barmode='group',
        margin=dict(l=20, r=20, t=20, b=20),
        height=250,
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#E2E8F0')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Action buttons for fraud detection
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.button("Review Alerts", use_container_width=True)
    with col_b:
        st.button("Update Rules", use_container_width=True)
    with col_c:
        st.button("Export Report", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Credit Analysis section
    st.markdown('<div class="section-title">Credit Analysis Overview</div>', unsafe_allow_html=True)
    
    with st.container():
        #st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Customer Credit Score Distribution</div>', unsafe_allow_html=True)
        
        credit_data = generate_credit_data()
        
        fig = px.bar(
            credit_data,
            x='score_range',
            y='percentage',
            labels={'score_range': 'Credit Score Range', 'percentage': 'Percentage of Customers'},
            color='percentage',
            color_continuous_scale=px.colors.sequential.Blues
        )
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#E2E8F0'),
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.button("Run Credit Analysis", use_container_width=True)
        with col2:
            st.button("View Detailed Reports", use_container_width=True)
        with col3:
            st.button("Configure Risk Models", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown('<div class="section-title">Recent Activity</div>', unsafe_allow_html=True)
    
    activity_data = {
        'Time': ['10:45 AM', '09:32 AM', '09:15 AM', '08:53 AM', '08:22 AM'],
        'User': ['John Smith', 'System', 'Mary Johnson', 'System', 'David Chen'],
        'Activity': [
            'Approved loan application #4528',
            'Flagged unusual transaction pattern for review',
            'Completed monthly reconciliation report',
            'Detected 3 potential fraud attempts',
            'Updated customer credit score model'
        ],
        'Status': ['Completed', 'Needs Review', 'Completed', 'In Progress', 'Completed']
    }
    
    activity_df = pd.DataFrame(activity_data)
    st.dataframe(
        activity_df, 
        column_config={
            "Time": st.column_config.TextColumn("Time"),
            "User": st.column_config.TextColumn("User/System"),
            "Activity": st.column_config.TextColumn("Activity"),
            "Status": st.column_config.TextColumn("Status")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Footer
    st.markdown("---")
    st.markdown('<div class="footer">© 2025 BankTech AI Suite. All rights reserved.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()