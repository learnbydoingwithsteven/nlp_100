"""
NLP App 034: Price Extraction
Real-world use case: Monetary value extraction
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Price Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("💲 Price Extraction")
st.markdown("""
**Real-world Use Case**: Extract prices and monetary values
- Multiple currencies ($, €, £)
- Range extraction (\$10-\$20)
- Decimal and comma formatting
- Price comparison
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

def extract_prices(text):
    """Extract prices"""
    # Currency symbols
    prices = []
    prices.extend(re.findall(r'\$\s*\d+(?:,\d{3})*(?:\.\d{2})?', text))
    prices.extend(re.findall(r'€\s*\d+(?:,\d{3})*(?:\.\d{2})?', text))
    prices.extend(re.findall(r'£\s*\d+(?:,\d{3})*(?:\.\d{2})?', text))
    # Written format: 100 USD
    prices.extend(re.findall(r'\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|EUR|GBP)', text))
    
    # Parse amounts
    amounts = []
    for price in prices:
        num = re.sub(r'[^\d.]', '', price)
        if num:
            try:
                amounts.append(float(num))
            except:
                pass
    
    return {
        'prices': prices,
        'count': len(prices),
        'total': sum(amounts) if amounts else 0,
        'average': sum(amounts)/len(amounts) if amounts else 0,
        'min': min(amounts) if amounts else 0,
        'max': max(amounts) if amounts else 0
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
            result = extract_prices(user_input)
            st.success("✅ Complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Prices Found", result['count'])
            with col2:
                st.metric("Total", f"${result['total']:.2f}")
            with col3:
                st.metric("Average", f"${result['average']:.2f}")
            
            if result['prices']:
                st.subheader("💲 Extracted Prices")
                for price in result['prices']:
                    st.write(f"• {price}")
                
                st.write(f"**Min:** ${result['min']:.2f} | **Max:** ${result['max']:.2f}")
            else:
                st.info("No prices found")
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
                all_prices = []
                for text in df['text']:
                    all_prices.extend(extract_prices(str(text))['prices'])
                st.success(f"✅ Found {len(all_prices)} prices!")
                if all_prices:
                    st.write(all_prices[:20])
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = "Laptop costs $1,299.99, phone is €799, and headphones are £49.50. Total: $2,148.49"
    
    if st.button("🚀 Run Demo", type="primary"):
        r = extract_prices(sample)
        st.success("✅ Demo Complete!")
        st.metric("Prices", r['count'])
        st.write("**All Prices:**", r['prices'])
        st.write(f"**Total:** ${r['total']:.2f}")

st.markdown("---")
st.markdown("**About**: Price Extraction")
st.caption("💡 Extracts prices in multiple currencies")
