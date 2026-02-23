"""
NLP App 026: Date/Time Extraction
Real-world use case: Temporal information extraction
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Date/Time Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("📅 Date/Time Extraction")
st.markdown("""
**Real-world Use Case**: Extract dates and times
- Multiple date formats
- Time expressions
- Relative dates
- Date ranges
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

def extract_datetimes(text):
    """Extract dates and times"""
    dates = []
    # Numeric dates: MM/DD/YYYY, DD-MM-YYYY
    dates.extend(re.findall(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b', text))
    # Written dates: January 15, 2024
    dates.extend(re.findall(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b', text, re.I))
    # ISO format: 2024-01-15
    dates.extend(re.findall(r'\b\d{4}-\d{2}-\d{2}\b', text))
    
    # Times: 3:30 PM, 15:00, 3pm
    times = re.findall(r'\b\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?\b|\b\d{1,2}\s*(?:AM|PM|am|pm)\b', text)
    
    return {'dates': dates, 'times': times, 'total': len(dates) + len(times)}

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
            result = extract_datetimes(user_input)
            st.success("✅ Complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Found", result['total'])
            with col2:
                st.metric("Dates", len(result['dates']))
            with col3:
                st.metric("Times", len(result['times']))
            
            if result['dates']:
                st.subheader("📅 Dates")
                for date in result['dates']:
                    st.write(f"📅 {date}")
            
            if result['times']:
                st.subheader("🕐 Times")
                st.write(", ".join(result['times']))
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
                all_dates, all_times = [], []
                for text in df['text']:
                    r = extract_datetimes(str(text))
                    all_dates.extend(r['dates'])
                    all_times.extend(r['times'])
                st.success(f"✅ Found {len(all_dates)} dates, {len(all_times)} times!")
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = "Meeting on January 15, 2024 at 3:30 PM. Next session: 02/20/2024 at 10am."
    
    if st.button("🚀 Run Demo", type="primary"):
        r = extract_datetimes(sample)
        st.success("✅ Demo Complete!")
        st.write("**Dates:**", r['dates'])
        st.write("**Times:**", r['times'])

st.markdown("---")
st.markdown("**About**: Date/Time Extraction")
st.caption("💡 Extracts dates and times in multiple formats")
