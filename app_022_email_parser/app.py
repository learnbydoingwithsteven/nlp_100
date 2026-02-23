"""
NLP App 022: Email Parser
Real-world use case: Contact information extraction
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Email Parser",
    page_icon="🔤",
    layout="wide"
)

st.title("📧 Email Parser")
st.markdown("""
**Real-world Use Case**: Extract email addresses and contact information
- Email address extraction
- Domain analysis
- Contact information parsing
- Batch email processing
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
st.sidebar.markdown("---")
st.sidebar.markdown("**Extraction Features:**")
st.sidebar.markdown("""
- 📧 Email Addresses
- 🌐 Domain Names
- 👤 Name Patterns
- 📊 Email Statistics
""")

def parse_emails(text):
    """Parse and extract email addresses from text"""
    # Email regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Find all emails
    emails = re.findall(email_pattern, text)
    
    # Extract domains
    domains = [email.split('@')[1] for email in emails]
    
    # Extract usernames
    usernames = [email.split('@')[0] for email in emails]
    
    # Domain statistics
    domain_counts = Counter(domains)
    
    # Categorize by domain type
    domain_types = {}
    for domain in set(domains):
        if any(x in domain for x in ['gmail', 'yahoo', 'hotmail', 'outlook']):
            domain_types[domain] = 'Personal'
        elif any(x in domain for x in ['.edu', 'university']):
            domain_types[domain] = 'Educational'
        elif any(x in domain for x in ['.gov', 'government']):
            domain_types[domain] = 'Government'
        else:
            domain_types[domain] = 'Business/Other'
    
    return {
        'text': text,
        'emails': emails,
        'unique_emails': list(set(emails)),
        'total_emails': len(emails),
        'unique_count': len(set(emails)),
        'domains': domains,
        'unique_domains': list(set(domains)),
        'domain_counts': dict(domain_counts),
        'domain_types': domain_types,
        'usernames': usernames
    }

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Processing")
    
    user_input = st.text_area(
        "Enter text to process:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    if st.button("🔍 Extract Emails", type="primary"):
        if user_input.strip():
            with st.spinner("Parsing..."):
                result = parse_emails(user_input)
            
            st.success("✅ Parsing Complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Emails", result['total_emails'])
            with col2:
                st.metric("Unique Emails", result['unique_count'])
            with col3:
                st.metric("Unique Domains", len(result['unique_domains']))
            
            if result['emails']:
                st.subheader("📧 Extracted Emails")
                for email in result['unique_emails']:
                    st.write(f"• {email}")
                
                if result['domain_counts']:
                    st.subheader("📊 Domain Distribution")
                    domain_df = pd.DataFrame(list(result['domain_counts'].items()),
                                            columns=['Domain', 'Count'])
                    fig = px.bar(domain_df, x='Domain', y='Count',
                                title='Emails by Domain',
                                color='Count', color_continuous_scale='Viridis')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No email addresses found.")
        else:
            st.warning("Please enter some text.")

# Mode: Batch Processing
elif mode == "Batch Processing":
    st.header("📚 Batch Processing")
    
    uploaded_file = st.file_uploader("Upload CSV with 'text' column", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} rows")
        
        if 'text' in df.columns:
            if st.button("🔍 Parse All", type="primary"):
                all_emails = []
                for idx, text in enumerate(df['text']):
                    result = parse_emails(str(text))
                    all_emails.extend(result['emails'])
                
                st.success(f"✅ Parsed {len(df)} texts!")
                st.metric("Total Emails Found", len(all_emails))
                
                if all_emails:
                    emails_df = pd.DataFrame({'Email': list(set(all_emails))})
                    st.dataframe(emails_df, use_container_width=True)
                    csv = emails_df.to_csv(index=False)
                    st.download_button("📥 Download", csv, "emails.csv", "text/csv")
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    
    samples = [
        "Contact us at support@example.com or sales@company.org for more information.",
        "Email john.doe@university.edu and jane.smith@gov.agency for details.",
        "Reach out: info@startup.io, marketing@business.net, admin@service.com"
    ]
    
    if st.button("🚀 Run Demo", type="primary"):
        all_emails = []
        for text in samples:
            result = parse_emails(text)
            all_emails.extend(result['emails'])
        
        st.success(f"✅ Found {len(all_emails)} emails!")
        for email in set(all_emails):
            st.write(f"📧 {email}")

st.markdown("---")
st.markdown("**About**: Email Parser - Extract and analyze email addresses from text")
st.caption("💡 Extracts emails, analyzes domains, categorizes by type")
