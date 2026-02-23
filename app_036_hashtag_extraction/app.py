"""
NLP App 036: Hashtag Extraction
Real-world use case: Social media tag extraction
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Hashtag Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("#️⃣ Hashtag Extraction")
st.markdown("""
**Real-world Use Case**: Extract hashtags
- Social media tags
- Trend analysis
- Frequency counting
- Topic identification
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

# Main processing function
def extract_hashtags(text):
    """Extract hashtags"""
    hashtags = re.findall(r'#\w+', text)
    hashtag_counts = Counter(hashtags)
    return {
        'hashtags': hashtags,
        'unique': list(set(hashtags)),
        'count': len(hashtags),
        'top_hashtags': dict(hashtag_counts.most_common(10))
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
            r = extract_hashtags(user_input)
            st.success("✅ Complete!")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Hashtags", r['count'])
            with col2:
                st.metric("Unique", len(r['unique']))
            if r['hashtags']:
                st.subheader("#️⃣ Hashtags")
                st.write(", ".join(r['unique']))
            else:
                st.info("No hashtags found")
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
                all_tags = []
                for text in df['text']:
                    all_tags.extend(extract_hashtags(str(text))['hashtags'])
                tag_counts = Counter(all_tags)
                st.success(f"✅ Found {len(all_tags)} hashtags!")
                st.write("**Top 20:**", dict(tag_counts.most_common(20)))
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = "Love this! #AI #MachineLearning #DataScience #Python #NLP #AI"
    
    if st.button("🚀 Run Demo", type="primary"):
        r = extract_hashtags(sample)
        st.success("✅ Demo Complete!")
        st.write("**Hashtags:**", r['unique'])

st.markdown("---")
st.markdown("**About**: Hashtag Extraction")
st.caption("💡 Extracts social media hashtags")
