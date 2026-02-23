"""
NLP App 033: Citation Extraction
Real-world use case: Academic reference parsing
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Citation Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("📚 Citation Extraction")
st.markdown("""
**Real-world Use Case**: Extract academic citations
- (Author, Year) format
- [Author et al., Year]
- DOI and reference parsing
- Bibliography extraction
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

def extract_citations(text):
    """Extract citations"""
    # (Author, Year) or (Author et al., Year)
    paren_cites = re.findall(r'\(([A-Z][a-z]+(?:\s+et\s+al\.?)?),?\s+(\d{4})\)', text)
    # [Author, Year] or [1]
    bracket_cites = re.findall(r'\[([A-Z][a-z]+(?:\s+et\s+al\.?)?),?\s+(\d{4})\]|\[(\d+)\]', text)
    # DOI patterns
    dois = re.findall(r'10\.\d{4,}/[-._;()/:A-Za-z0-9]+', text)
    
    citations = [f"{author}, {year}" for author, year in paren_cites]
    citations.extend([f"{m[0]}, {m[1]}" if m[0] else f"[{m[2]}]" for m in bracket_cites])
    
    return {
        'citations': citations,
        'dois': dois,
        'count': len(citations),
        'doi_count': len(dois)
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
            result = extract_citations(user_input)
            st.success("✅ Complete!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Citations", result['count'])
            with col2:
                st.metric("DOIs", result['doi_count'])
            
            if result['citations']:
                st.subheader("📚 Citations")
                for cite in result['citations']:
                    st.write(f"• {cite}")
            
            if result['dois']:
                st.subheader("🔗 DOIs")
                for doi in result['dois']:
                    st.write(f"• {doi}")
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
                all_cites = []
                for text in df['text']:
                    all_cites.extend(extract_citations(str(text))['citations'])
                st.success(f"✅ Found {len(all_cites)} citations!")
                if all_cites:
                    st.write(all_cites[:30])
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = "Recent studies (Smith, 2023) and (Jones et al., 2022) show promising results. DOI: 10.1000/xyz123"
    
    if st.button("🚀 Run Demo", type="primary"):
        r = extract_citations(sample)
        st.success("✅ Demo Complete!")
        st.write("**Citations:**", r['citations'])
        st.write("**DOIs:**", r['dois'])

st.markdown("---")
st.markdown("**About**: Citation Extraction")
st.caption("💡 Extracts academic citations and DOIs")
