"""
NLP App 028: URL Extraction
Real-world use case: Link extraction and validation
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="URL Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("🔗 URL Extraction")
st.markdown("""
**Real-world Use Case**: Extract web links
- HTTP/HTTPS URLs
- www. domains
- Domain extraction
- Link validation
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

def extract_urls(text):
    """Extract URLs"""
    urls = re.findall(r'https?://[^\s]+|www\.[^\s]+', text, re.I)
    domains = []
    for url in urls:
        match = re.search(r'(?:https?://)?(?:www\.)?([^/\s]+)', url)
        if match:
            domains.append(match.group(1))
    
    return {'urls': urls, 'domains': list(set(domains)), 'count': len(urls)}

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
            result = extract_urls(user_input)
            st.success("✅ Complete!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("URLs Found", result['count'])
            with col2:
                st.metric("Unique Domains", len(result['domains']))
            
            if result['urls']:
                st.subheader("🔗 URLs")
                for url in result['urls']:
                    st.write(f"🔗 {url}")
            else:
                st.info("No URLs found")
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
                all_urls = []
                for text in df['text']:
                    all_urls.extend(extract_urls(str(text))['urls'])
                st.success(f"✅ Found {len(all_urls)} URLs!")
                if all_urls:
                    st.write(all_urls[:20])
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = "Visit https://example.com and www.test.org for more info."
    
    if st.button("🚀 Run Demo", type="primary"):
        r = extract_urls(sample)
        st.success("✅ Demo Complete!")
        st.write("**URLs:**", r['urls'])
        st.write("**Domains:**", r['domains'])

st.markdown("---")
st.markdown("**About**: URL Extraction")
st.caption("💡 Extracts web links and domains")
