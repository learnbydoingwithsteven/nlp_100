"""
NLP App 029: Product Mention Extraction
Real-world use case: Brand/product identification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Product Mention Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("🏷️ Product Mention Extraction")
st.markdown("""
**Real-world Use Case**: Extract product mentions
- Brand names
- Product models
- Version numbers
- Product categories
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

BRANDS = ['Apple', 'Samsung', 'Google', 'Microsoft', 'Sony', 'Dell', 'HP', 'Lenovo', 'Amazon', 'Nike', 'Adidas']

def extract_products(text):
    """Extract product mentions"""
    found_brands = [b for b in BRANDS if b.lower() in text.lower()]
    # Product models: iPhone 15, Galaxy S24, Pixel 8
    models = re.findall(r'\b(?:iPhone|Galaxy|Pixel|Surface|MacBook|iPad|Kindle)\s*\d+\s*(?:Pro|Max|Ultra|Plus)?\b', text, re.I)
    
    return {'brands': found_brands, 'models': models, 'total': len(found_brands) + len(models)}

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
            result = extract_products(user_input)
            st.success("✅ Complete!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Products Found", result['total'])
            with col2:
                st.metric("Brands", len(result['brands']))
            
            if result['brands']:
                st.subheader("🏷️ Brands")
                st.write(", ".join(result['brands']))
            
            if result['models']:
                st.subheader("📱 Product Models")
                for model in result['models']:
                    st.write(f"• {model}")
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
                all_brands = []
                for text in df['text']:
                    all_brands.extend(extract_products(str(text))['brands'])
                st.success(f"✅ Found {len(all_brands)} product mentions!")
                if all_brands:
                    from collections import Counter
                    brand_counts = Counter(all_brands)
                    st.write(dict(brand_counts))
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = "I bought an iPhone 15 Pro and Samsung Galaxy S24. Also considering a Google Pixel 8."
    
    if st.button("🚀 Run Demo", type="primary"):
        r = extract_products(sample)
        st.success("✅ Demo Complete!")
        st.write("**Brands:**", r['brands'])
        st.write("**Models:**", r['models'])

st.markdown("---")
st.markdown("**About**: Product Mention Extraction")
st.caption("💡 Extracts brand names and product models")
