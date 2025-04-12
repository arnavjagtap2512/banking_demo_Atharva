import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="BankTech AI Suite",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3.2rem;
        font-weight: 700;
        color: #0A2559;
        margin-bottom: 1rem;
    }
    
    .tagline {
        font-size: 1.5rem;
        color: #4A5568;
        margin-bottom: 2.5rem;
        font-weight: 300;
    }
    
    .section-header {
        font-size: 2rem;
        font-weight: 600;
        color: #0A2559;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E2E8F0;
    }
    
    .feature-box {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 1.5rem;
        height: 100%;
        border-left: 4px solid #0A2559;
        transition: transform 0.3s;
    }
    
    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        color: #0A2559;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #0A2559;
        margin-bottom: 0.75rem;
    }
    
    .feature-desc {
        color: #4A5568;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    .cta-section {
        background-color: #E6EFF6;
        padding: 2.5rem;
        border-radius: 8px;
        margin: 3rem 0;
        text-align: center;
    }
    
    .cta-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #0A2559;
        margin-bottom: 1rem;
    }
    
    .cta-text {
        color: #4A5568;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .stats-box {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0A2559;
        margin-bottom: 0.5rem;
    }
    
    .stats-label {
        color: #4A5568;
        font-size: 1rem;
    }
    
    .footer {
        text-align: center;
        color: #718096;
        padding-top: 2rem;
        font-size: 0.9rem;
    }
    
    .dashboard-button {
        background-color: #0A2559;
        color: white;
        border-radius: 4px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        cursor: pointer;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        transition: background-color 0.3s;
    }
    
    .dashboard-button:hover {
        background-color: #183C7E;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Hero Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-header">BankTech AI Suite</div>', unsafe_allow_html=True)
        st.markdown('<div class="tagline">Revolutionizing banking operations with AI-powered solutions</div>', unsafe_allow_html=True)
    
    # Key Stats
    st.markdown('<div class="section-header">Making Banking Smarter</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('''
        <div class="stats-box">
            <div class="stats-number">87%</div>
            <div class="stats-label">Reduction in processing time</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="stats-box">
            <div class="stats-number">99.8%</div>
            <div class="stats-label">Reconciliation accuracy</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div class="stats-box">
            <div class="stats-number">65%</div>
            <div class="stats-label">Fraud detection improvement</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown('''
        <div class="stats-box">
            <div class="stats-number">3.2x</div>
            <div class="stats-label">Faster credit analysis</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Features Section
    st.markdown('<div class="section-header">Advanced Banking Solutions</div>', unsafe_allow_html=True)
    
    # First row of features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('''
        <div class="feature-box">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Automated Report Generation</div>
            <div class="feature-desc">
                Generate comprehensive financial reports with AI-powered insights, tailored recommendations, and loan eligibility analysis for your customers.
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="feature-box">
            <div class="feature-icon">🧮</div>
            <div class="feature-title">Credit Risk Analysis</div>
            <div class="feature-desc">
                Leverage advanced AI algorithms to assess credit scores with precision and predict potential loan defaults before they occur.
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
    with col3:
        st.markdown('''
        <div class="feature-box">
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">Real-Time Fraud Detection</div>
            <div class="feature-desc">
                Identify and flag suspicious transactions instantly based on sophisticated pattern recognition and customer behavioral analysis.
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Second row of features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('''
        <div class="feature-box">
            <div class="feature-icon">💸</div>
            <div class="feature-title">Bulk Payment Processing</div>
            <div class="feature-desc">
                Streamline high-volume transactions with automated processing for salary disbursements, vendor payments, and dividend distributions.
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="feature-box">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Chatbots for Banker Support</div>
            <div class="feature-desc">
                Empower your banking staff with intelligent assistants that provide instant answers to queries about policies, rates, and procedures.
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
    with col3:
        st.markdown('''
        <div class="feature-box">
            <div class="feature-icon">📑</div>
            <div class="feature-title">Automated Account Reconciliation</div>
            <div class="feature-desc">
                Match transaction records from different sources with pinpoint accuracy, drastically reducing manual effort and human error.
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # CTA Section
    st.markdown('''
    <div class="cta-section">
        <div class="cta-title">Ready to transform your banking operations?</div>
        <div class="cta-text">
            BankTech AI Suite brings cutting-edge artificial intelligence and process automation to modernize your financial institution. Our platform seamlessly integrates with your existing systems to deliver immediate efficiency gains while setting the foundation for future innovation.
        </div>
        <a href="Dashboard" target="_self">
            <button class="dashboard-button">Explore Dashboard</button>
        </a>
    </div>
    ''', unsafe_allow_html=True)
    
    # Why Choose Us Section
    st.markdown('<div class="section-header">Why Financial Institutions Choose Us</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Enterprise-Grade Security
        - Bank-level encryption for all data
        - Compliant with global financial regulations
        - Regular security audits and penetration testing
        - Secure multi-factor authentication
        
        ### Seamless Integration
        - Compatible with existing core banking systems
        - Flexible API architecture
        - Minimal disruption during implementation
        - Comprehensive documentation and support
        """)
    
    with col2:
        st.markdown("""
        ### Proven Results
        - 40+ successful implementations with major banks
        - Average ROI within 6 months
        - 24/7 dedicated support team
        - Regular updates and new features
        
        ### Customizable Platform
        - Tailored to your specific operational needs
        - Scalable from small branches to global institutions
        - Custom reporting and dashboard options
        - White-label options available
        """)
    
    # Footer
    st.markdown("---")
    st.markdown('<div class="footer">© 2025 BankTech AI Suite. All rights reserved.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()