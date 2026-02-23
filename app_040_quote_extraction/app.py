"""
NLP App 040: Quote Extraction
Real-world use case: Quotation and attribution extraction
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Quote Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("💬 Quote Extraction")
st.markdown("""
**Real-world Use Case**: Extract quotations
- Direct quotes ("...")
- Single quotes ('...')
- Attribution detection
- Speaker identification
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

# Main processing function
def extract_quotes(text):
    """Extract quotes"""
    # Double quotes
    double_quotes = re.findall(r'"([^"]+)"', text)
    # Single quotes
    single_quotes = re.findall(r"'([^']+)'", text)
    # Attribution (said/stated/etc)
    attributions = re.findall(r'([A-Z][a-z]+)\s+(?:said|stated|wrote|mentioned|explained)', text)
    
    return {
        'double_quotes': double_quotes,
        'single_quotes': single_quotes,
        'attributions': attributions,
        'total': len(double_quotes) + len(single_quotes)
    }

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
            r = extract_quotes(user_input)
            st.success("✅ Complete!")
            st.metric("Quotes Found", r['total'])
            if r['double_quotes']:
                st.subheader('💬 "Quotes"')
                for q in r['double_quotes']:
                    st.write(f'• "{q}"')
            if r['single_quotes']:
                st.subheader("\u2019Quotes\u2018")
                for q in r['single_quotes']:
                    st.write(f"\u2022 '{q}'")
            if r['attributions']:
                st.write("**Speakers:**", ", ".join(r['attributions']))
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
                all_quotes = []
                for text in df['text']:
                    r = extract_quotes(str(text))
                    all_quotes.extend(r['double_quotes'])
                    all_quotes.extend(r['single_quotes'])
                st.success(f"✅ Found {len(all_quotes)} quotes!")
                if all_quotes:
                    st.write(all_quotes[:20])
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = 'John said "Hello world" and Mary stated "AI is amazing".'
    
    if st.button("🚀 Run Demo", type="primary"):
        r = extract_quotes(sample)
        st.success("✅ Demo Complete!")
        st.write("**Quotes:**", r['double_quotes'])
        st.write("**Speakers:**", r['attributions'])

st.markdown("---")
st.markdown("**About**: Quote Extraction")
st.caption("💡 Extracts quotations and attributions")
