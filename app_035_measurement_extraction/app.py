"""
NLP App 035: Measurement Extraction
Real-world use case: Quantity and unit parsing
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Measurement Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("📏 Measurement Extraction")
st.markdown("""
**Real-world Use Case**: Extract measurements
- Weight, length, volume
- Metric and imperial units
- Quantity parsing
- Unit conversion
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

# Main processing function
def extract_measurements(text):
    """Extract measurements"""
    # Pattern: number + unit
    measurements = re.findall(r'\d+(?:\.\d+)?\s*(?:kg|g|mg|lb|oz|m|cm|mm|km|ft|in|L|ml|gal)', text, re.I)
    
    # Count by unit type
    units = [re.search(r'[a-zA-Z]+$', m).group() for m in measurements]
    unit_counts = Counter(units)
    
    return {
        'measurements': measurements,
        'count': len(measurements),
        'units': list(set(units)),
        'unit_counts': dict(unit_counts)
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
            r = extract_measurements(user_input)
            st.success("✅ Complete!")
            st.metric("Measurements Found", r['count'])
            if r['measurements']:
                st.subheader("📏 Extracted Measurements")
                for m in r['measurements']:
                    st.write(f"• {m}")
                st.write("**Unit Distribution:**", r['unit_counts'])
            else:
                st.info("No measurements found")
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
                all_m = []
                for text in df['text']:
                    all_m.extend(extract_measurements(str(text))['measurements'])
                st.success(f"✅ Found {len(all_m)} measurements!")
                if all_m:
                    st.write(all_m[:30])
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = "Package weighs 5kg, dimensions: 30cm x 20cm x 10cm, volume: 2.5L"
    
    if st.button("🚀 Run Demo", type="primary"):
        r = extract_measurements(sample)
        st.success("✅ Demo Complete!")
        st.write("**Measurements:**", r['measurements'])

st.markdown("---")
st.markdown("**About**: Measurement Extraction")
st.caption("💡 Extracts measurements with units")
