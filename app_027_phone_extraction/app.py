"""
NLP App 027: Phone Number Extraction
Real-world use case: Contact number parsing
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Phone Number Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("☎️ Phone Number Extraction")
st.markdown("""
**Real-world Use Case**: Extract phone numbers
- US format: (555) 123-4567
- International: +1-555-123-4567
- Various separators
- Extensions
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

def extract_phones(text):
    """Extract phone numbers"""
    phones = []
    # (555) 123-4567 or 555-123-4567
    phones.extend(re.findall(r'\(?\d{3}\)?[-\s.]?\d{3}[-\s.]?\d{4}', text))
    # International: +1-555-123-4567
    phones.extend(re.findall(r'\+\d{1,3}[-\s.]?\(?\d{3}\)?[-\s.]?\d{3}[-\s.]?\d{4}', text))
    
    return {'phones': list(set(phones)), 'count': len(set(phones))}

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Processing")
    
    user_input = st.text_area(
        "Enter text to process:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    if st.button("🔍 Extract", type="primary"):
        if user_input.strip():
            result = extract_phones(user_input)
            st.success("✅ Complete!")
            st.metric("Phones Found", result['count'])
            
            if result['phones']:
                st.subheader("☎️ Phone Numbers")
                for phone in result['phones']:
                    st.write(f"☎️ {phone}")
            else:
                st.info("No phone numbers found")
        else:
            st.warning("Please enter text.")

# Mode: Batch Processing
elif mode == "Batch Processing":
    st.header("📚 Batch Processing")
    
    uploaded_file = st.file_uploader("Upload CSV with 'text' column", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} rows")
        
        if 'text' in df.columns:
            if st.button("🔍 Extract All", type="primary"):
                all_phones = []
                for text in df['text']:
                    all_phones.extend(extract_phones(str(text))['phones'])
                st.success(f"✅ Found {len(set(all_phones))} unique phones!")
                if all_phones:
                    st.write(list(set(all_phones))[:20])
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = "Call (555) 123-4567 or +1-555-987-6543 for support."
    
    if st.button("🚀 Run Demo", type="primary"):
        r = extract_phones(sample)
        st.success("✅ Demo Complete!")
        st.write("**Phones:**", r['phones'])

st.markdown("---")
st.markdown("**About**: Phone Extraction")
st.caption("💡 Extracts phone numbers in various formats")
