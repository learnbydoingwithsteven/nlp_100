"""
NLP App 037: Mention Extraction
Real-world use case: User mention identification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Mention Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("@ Mention Extraction")
st.markdown("""
**Real-world Use Case**: Extract @mentions
- Social media mentions
- User identification
- Network analysis
- Engagement tracking
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

# Main processing function
def extract_mentions(text):
    """Extract mentions"""
    mentions = re.findall(r'@\w+', text)
    mention_counts = Counter(mentions)
    return {
        'mentions': mentions,
        'unique': list(set(mentions)),
        'count': len(mentions),
        'top_mentions': dict(mention_counts.most_common(10))
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
            r = extract_mentions(user_input)
            st.success("✅ Complete!")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Mentions", r['count'])
            with col2:
                st.metric("Unique Users", len(r['unique']))
            if r['mentions']:
                st.subheader("@ Mentions")
                st.write(", ".join(r['unique']))
            else:
                st.info("No mentions found")
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
                all_mentions = []
                for text in df['text']:
                    all_mentions.extend(extract_mentions(str(text))['mentions'])
                mention_counts = Counter(all_mentions)
                st.success(f"✅ Found {len(all_mentions)} mentions!")
                st.write("**Top 20:**", dict(mention_counts.most_common(20)))
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = "Thanks @john and @sarah! cc: @team @alice @john"
    
    if st.button("🚀 Run Demo", type="primary"):
        r = extract_mentions(sample)
        st.success("✅ Demo Complete!")
        st.write("**Mentions:**", r['unique'])
        st.write("**Counts:**", r['top_mentions'])

st.markdown("---")
st.markdown("**About**: Mention Extraction")
st.caption("💡 Extracts @mentions from text")
