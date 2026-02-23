"""
NLP App 024: Invoice Parser
Real-world use case: Financial document extraction
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Invoice Parser",
    page_icon="🔤",
    layout="wide"
)

st.title("💰 Invoice Parser")
st.markdown("""
**Real-world Use Case**: Extract invoice data - amounts, dates, numbers
- Currency amounts extraction
- Date and invoice number parsing
- Financial data analysis
- Batch invoice processing
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

def parse_invoice(text):
    """Parse invoice and extract key financial data"""
    # Extract currency amounts ($, €, £)
    amounts = re.findall(r'\$\s*\d+(?:,\d{3})*(?:\.\d{2})?|€\s*\d+(?:,\d{3})*(?:\.\d{2})?|£\s*\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|EUR|GBP)', text)
    
    # Extract dates (various formats)
    dates = re.findall(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b', text, re.I)
    
    # Extract invoice numbers
    inv_numbers = re.findall(r'INV[-#]?\s*\d+|Invoice\s*#?\s*\d+|\bINV\d+\b', text, re.I)
    
    # Calculate total
    total = 0
    for amt in amounts:
        num_str = re.sub(r'[^\d.]', '', amt)
        if num_str:
            try:
                total += float(num_str)
            except:
                pass
    
    return {
        'text': text,
        'amounts': amounts,
        'total_amount': total,
        'dates': dates,
        'invoice_numbers': inv_numbers,
        'item_count': len(amounts)
    }

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Processing")
    
    user_input = st.text_area(
        "Enter text to process:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    if st.button("🔍 Parse Invoice", type="primary"):
        if user_input.strip():
            with st.spinner("Parsing invoice..."):
                result = parse_invoice(user_input)
            
            st.success("✅ Parsing Complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Amount", f"${result['total_amount']:.2f}")
            with col2:
                st.metric("Line Items", result['item_count'])
            with col3:
                st.metric("Dates Found", len(result['dates']))
            
            st.subheader("💵 Extracted Amounts")
            if result['amounts']:
                for amt in result['amounts']:
                    st.write(f"• {amt}")
            else:
                st.info("No amounts found")
            
            if result['dates']:
                st.subheader("📅 Dates")
                st.write(", ".join(result['dates']))
            
            if result['invoice_numbers']:
                st.subheader("#️⃣ Invoice Numbers")
                st.write(", ".join(result['invoice_numbers']))
        else:
            st.warning("Please enter invoice text.")

# Mode: Batch Processing
elif mode == "Batch Processing":
    st.header("📚 Batch Processing")
    
    uploaded_file = st.file_uploader("Upload CSV with 'text' column", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} rows")
        
        if 'text' in df.columns:
            if st.button("🔍 Parse All", type="primary"):
                results = []
                progress_bar = st.progress(0)
                
                for idx, text in enumerate(df['text']):
                    result = parse_invoice(str(text))
                    results.append({
                        'total': result['total_amount'],
                        'items': result['item_count'],
                        'dates': len(result['dates'])
                    })
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Parsed {len(results_df)} invoices!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Invoices", len(results_df))
                with col2:
                    st.metric("Total Amount", f"${results_df['total'].sum():.2f}")
                with col3:
                    st.metric("Avg Amount", f"${results_df['total'].mean():.2f}")
                
                fig = px.histogram(results_df, x='total', title='Invoice Amount Distribution')
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(results_df, use_container_width=True)
                csv = results_df.to_csv(index=False)
                st.download_button("📥 Download", csv, "results.csv", "text/csv")
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    
    sample = """INVOICE #12345
Date: 01/15/2024
Due Date: 02/15/2024

Item 1: $150.00
Item 2: $275.50
Item 3: $824.00

Subtotal: $1,249.50
Tax: $99.96
Total: $1,349.46"""
    
    if st.button("🚀 Run Demo", type="primary"):
        result = parse_invoice(sample)
        st.success("✅ Demo Complete!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Amount", f"${result['total_amount']:.2f}")
        with col2:
            st.metric("Line Items", result['item_count'])
        
        st.write("**Amounts:**", result['amounts'])
        st.write("**Invoice Number:**", result['invoice_numbers'][0] if result['invoice_numbers'] else "N/A")

st.markdown("---")
st.markdown("**About**: Invoice Parser - Extract financial data from invoices")
st.caption("💡 Extracts amounts, dates, invoice numbers, and calculates totals")
