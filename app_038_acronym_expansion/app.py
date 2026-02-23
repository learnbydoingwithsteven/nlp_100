"""
NLP App 038: Acronym Expansion
Real-world use case: Abbreviation full form extraction
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Acronym Expansion",
    page_icon="🔤",
    layout="wide"
)

st.title("🔤 Acronym Expansion")
st.markdown("""
**Real-world Use Case**: Expand acronyms
- Common acronym detection
- Definition lookup
- Context-based expansion
- Technical abbreviations
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

# Main processing function
ACRONYMS = {
    'AI': 'Artificial Intelligence', 'ML': 'Machine Learning', 'NLP': 'Natural Language Processing',
    'API': 'Application Programming Interface', 'URL': 'Uniform Resource Locator',
    'HTML': 'HyperText Markup Language', 'CSS': 'Cascading Style Sheets',
    'SQL': 'Structured Query Language', 'JSON': 'JavaScript Object Notation',
    'HTTP': 'HyperText Transfer Protocol', 'FTP': 'File Transfer Protocol',
    'CEO': 'Chief Executive Officer', 'CTO': 'Chief Technology Officer',
    'USA': 'United States of America', 'UK': 'United Kingdom'
}

def expand_acronyms(text):
    """Expand acronyms"""
    found_acronyms = {}
    words = text.split()
    
    for word in words:
        clean_word = re.sub(r'[^A-Z]', '', word)
        if clean_word in ACRONYMS:
            found_acronyms[clean_word] = ACRONYMS[clean_word]
    
    return {
        'acronyms': found_acronyms,
        'count': len(found_acronyms)
    }

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Processing")
    
    user_input = st.text_area(
        "Enter text to process:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    if st.button("🔍 Expand", type="primary"):
        if user_input.strip():
            r = expand_acronyms(user_input)
            st.success("✅ Complete!")
            st.metric("Acronyms Found", r['count'])
            if r['acronyms']:
                st.subheader("🔤 Expanded Acronyms")
                for acronym, expansion in r['acronyms'].items():
                    st.write(f"**{acronym}** = {expansion}")
            else:
                st.info("No known acronyms found")
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
            if st.button("🔍 Expand All", type="primary"):
                from collections import Counter
                all_acr = {}
                for text in df['text']:
                    all_acr.update(expand_acronyms(str(text))['acronyms'])
                st.success(f"✅ Found {len(all_acr)} unique acronyms!")
                if all_acr:
                    for acr, exp in all_acr.items():
                        st.write(f"**{acr}** = {exp}")
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = "AI and ML are transforming NLP. Our API uses JSON over HTTP."
    
    if st.button("🚀 Run Demo", type="primary"):
        r = expand_acronyms(sample)
        st.success("✅ Demo Complete!")
        for acr, exp in r['acronyms'].items():
            st.write(f"**{acr}** = {exp}")

st.markdown("---")
st.markdown("**About**: Acronym Expansion")
st.caption("💡 Expands common acronyms to full forms")
