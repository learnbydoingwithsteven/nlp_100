"""
NLP App 030: Event Extraction
Real-world use case: Event information extraction
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Event Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("📅 Event Extraction")
st.markdown("""
**Real-world Use Case**: Extract event information
- Event names
- Dates and times
- Event types
- Locations
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

EVENT_KEYWORDS = ['conference', 'meeting', 'webinar', 'workshop', 'seminar', 'summit', 'event', 'festival', 'concert', 'expo']

def extract_events(text):
    """Extract events"""
    events = []
    for keyword in EVENT_KEYWORDS:
        pattern = rf'\b[A-Z][\w\s]*{keyword}[\w\s]*'
        events.extend(re.findall(pattern, text, re.I))
    
    # Extract dates
    dates = re.findall(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b', text, re.I)
    
    return {'events': list(set(events))[:10], 'dates': dates, 'total': len(events)}

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
            result = extract_events(user_input)
            st.success("✅ Complete!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Events Found", len(result['events']))
            with col2:
                st.metric("Dates", len(result['dates']))
            
            if result['events']:
                st.subheader("📅 Events")
                for event in result['events']:
                    st.write(f"🎉 {event}")
            
            if result['dates']:
                st.write("**Dates:**", ", ".join(result['dates']))
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
                all_events = []
                for text in df['text']:
                    all_events.extend(extract_events(str(text))['events'])
                st.success(f"✅ Found {len(all_events)} events!")
                if all_events:
                    st.write(all_events[:20])
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = "AI Conference 2024 on March 15, 2024. Join our Tech Summit and Developer Workshop."
    
    if st.button("🚀 Run Demo", type="primary"):
        r = extract_events(sample)
        st.success("✅ Demo Complete!")
        st.write("**Events:**", r['events'])
        st.write("**Dates:**", r['dates'])

st.markdown("---")
st.markdown("**About**: Event Extraction")
st.caption("💡 Extracts event names, types, and dates")
