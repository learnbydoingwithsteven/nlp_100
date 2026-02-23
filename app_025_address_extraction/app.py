"""
NLP App 025: Address Extraction
Real-world use case: Postal address parsing
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Address Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("📍 Address Extraction")
st.markdown("""
**Real-world Use Case**: Extract physical addresses
- Street addresses
- City, state, ZIP codes
- P.O. Boxes
- Multi-line address parsing
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

def extract_addresses(text):
    """Extract addresses from text"""
    # ZIP codes
    zips = re.findall(r'\b\d{5}(?:-\d{4})?\b', text)
    # States (2-letter codes)
    states = re.findall(r'\b[A-Z]{2}\b', text)
    # Street addresses
    streets = re.findall(r'\d+\s+[A-Za-z0-9\s,]+(?:Street|St\.?|Avenue|Ave\.?|Road|Rd\.?|Drive|Dr\.?|Lane|Ln\.?|Boulevard|Blvd\.?|Way|Court|Ct\.?)', text, re.I)
    # P.O. Boxes
    po_boxes = re.findall(r'P\.?O\.?\s*Box\s*\d+', text, re.I)
    
    return {
        'streets': streets,
        'zips': zips,
        'states': states,
        'po_boxes': po_boxes,
        'total_addresses': len(streets) + len(po_boxes)
    }

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Processing")
    
    user_input = st.text_area(
        "Enter text to process:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    if st.button("🔍 Extract Addresses", type="primary"):
        if user_input.strip():
            result = extract_addresses(user_input)
            st.success("✅ Extraction Complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Addresses Found", result['total_addresses'])
            with col2:
                st.metric("ZIP Codes", len(result['zips']))
            with col3:
                st.metric("States", len(set(result['states'])))
            
            if result['streets']:
                st.subheader("🏘️ Street Addresses")
                for addr in result['streets']:
                    st.write(f"📍 {addr}")
            
            if result['po_boxes']:
                st.subheader("📮 P.O. Boxes")
                for po in result['po_boxes']:
                    st.write(f"📮 {po}")
            
            if result['zips']:
                st.write("**ZIP Codes:**", ", ".join(result['zips']))
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
                all_addresses = []
                for text in df['text']:
                    result = extract_addresses(str(text))
                    all_addresses.extend(result['streets'])
                
                st.success(f"✅ Found {len(all_addresses)} addresses!")
                st.metric("Total Addresses", len(all_addresses))
                
                if all_addresses:
                    addr_df = pd.DataFrame({'Address': all_addresses[:50]})
                    st.dataframe(addr_df, use_container_width=True)
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    
    sample = "Visit us at 123 Main Street, New York, NY 10001 or mail to P.O. Box 456, Los Angeles, CA 90001"
    
    if st.button("🚀 Run Demo", type="primary"):
        result = extract_addresses(sample)
        st.success("✅ Demo Complete!")
        st.metric("Addresses Found", result['total_addresses'])
        
        if result['streets']:
            st.write("**Streets:**")
            for addr in result['streets']:
                st.write(f"📍 {addr}")
        if result['po_boxes']:
            st.write("**P.O. Boxes:**", result['po_boxes'])

st.markdown("---")
st.markdown("**About**: Address Extraction - Parse physical addresses")
st.caption("💡 Extracts street addresses, ZIP codes, P.O. Boxes")
