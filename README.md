# BankTech AI Suite

A comprehensive banking operations platform powered by AI and data visualization. This Streamlit application provides bankers with tools for transaction management, account reconciliation, credit analysis, and fraud detection.

## Features

- **Transaction Records Management**: Search, sort, and analyze customer transactions
- **Automated Report Generation**: Generate visual analytics reports for customer transactions
- **Credit Risk Analysis**: Assess credit scores and predict loan defaults with AI
- **Real-Time Fraud Detection**: Flag unusual transactions based on behavioral patterns
- **Bulk Payment Processing**: Automate salary disbursements and vendor payments
- **AI-Powered Chatbots**: Provide quick answers to bankers for queries on policies, rates, and processes

## Project Structure

```
banking_demo/
├── Home.py                # Main landing page
├── pages/                 # Additional pages
│   ├── dashboard.py       # Banking operations dashboard
│   └── transactions.py    # Transaction records and analysis
├── data/                  # Sample and real data files
│   └── transactions.csv   # Transaction data
├── requirements.txt       # Dependencies
└── README.md              # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/banking-demo.git
cd banking-demo
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run Home.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Development

To add new features or pages:

1. Create a new Python file in the `pages/` directory
2. Implement your Streamlit page with the required functionality
3. The file will automatically appear in the navigation