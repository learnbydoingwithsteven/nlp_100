"""
NLP App 032: Keyword Extraction
Real-world use case: Important term identification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Keyword Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("🔑 Keyword Extraction")
st.markdown("""
**Real-world Use Case**: Extract important keywords
- Frequency-based extraction
- Capitalized terms
- Multi-word phrases
- Stop word filtering
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

STOP_WORDS = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'was', 'are', 'were'}

def extract_keywords(text, top_n=10):
    """Extract keywords"""
    # Capitalized terms (likely important)
    cap_words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    
    # All words (filtered)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    filtered_words = [w for w in words if w not in STOP_WORDS]
    
    # Count frequencies
    word_freq = Counter(filtered_words)
    cap_freq = Counter(cap_words)
    
    top_keywords = word_freq.most_common(top_n)
    top_capitalized = cap_freq.most_common(5)
    
    return {
        'keywords': [w[0] for w in top_keywords],
        'frequencies': dict(top_keywords),
        'capitalized': [w[0] for w in top_capitalized],
        'total_unique': len(word_freq)
    }

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Processing")
    
    user_input = st.text_area(
        "Enter text to process:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    top_n = st.slider("Number of keywords", 5, 20, 10)
    
    if st.button("🔍 Extract", type="primary"):
        if user_input.strip():
            result = extract_keywords(user_input, top_n)
            st.success("✅ Complete!")
            
            st.metric("Unique Words", result['total_unique'])
            
            st.subheader("🔑 Top Keywords")
            for kw in result['keywords']:
                freq = result['frequencies'][kw]
                st.write(f"• **{kw}** (appears {freq}x)")
            
            if result['capitalized']:
                st.subheader("🏷️ Capitalized Terms")
                st.write(", ".join(result['capitalized']))
        else:
            st.warning("Please enter some text to process.")

# Mode: Batch Processing
elif mode == "Batch Processing":
    st.header("📚 Batch Processing")
    
    uploaded_file = st.file_uploader("Upload CSV with 'text' column", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} rows")
        
        if 'text' in df.columns:
            if st.button("🔍 Extract All", type="primary"):
                all_keywords = []
                for text in df['text']:
                    all_keywords.extend(extract_keywords(str(text), 5)['keywords'])
                keyword_freq = Counter(all_keywords)
                st.success(f"✅ Extracted keywords from {len(df)} texts!")
                st.write("**Top 20 Keywords:**", dict(keyword_freq.most_common(20)))
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = "Machine Learning and Artificial Intelligence are transforming Data Science. Python is the most popular programming language for Machine Learning applications."
    
    if st.button("🚀 Run Demo", type="primary"):
        r = extract_keywords(sample)
        st.success("✅ Demo Complete!")
        st.write("**Keywords:**", r['keywords'])
        st.write("**Capitalized:**", r['capitalized'])

st.markdown("---")
st.markdown("**About**: Keyword Extraction")
st.caption("💡 Extracts important keywords using frequency analysis")
