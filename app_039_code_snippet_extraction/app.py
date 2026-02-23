"""
NLP App 039: Code Snippet Extraction
Real-world use case: Programming code identification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Code Snippet Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("💻 Code Snippet Extraction")
st.markdown("""
**Real-world Use Case**: Extract code snippets
- Inline code (`code`)
- Code blocks
- Function/variable names
- Programming patterns
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

# Main processing function
def extract_code(text):
    """Extract code snippets"""
    # Inline code: `code`
    inline = re.findall(r'`([^`]+)`', text)
    # Code blocks: ```code```
    blocks = re.findall(r'```([^`]+)```', text, re.DOTALL)
    # Function calls: func()
    functions = re.findall(r'\b\w+\(\)', text)
    
    return {
        'inline': inline,
        'blocks': blocks,
        'functions': functions,
        'total': len(inline) + len(blocks) + len(functions)
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
            r = extract_code(user_input)
            st.success("✅ Complete!")
            st.metric("Code Elements", r['total'])
            if r['inline']:
                st.subheader("📝 Inline Code")
                for code in r['inline']:
                    st.code(code)
            if r['blocks']:
                st.subheader("📋 Code Blocks")
                for block in r['blocks']:
                    st.code(block)
            if r['functions']:
                st.write("**Functions:**", ", ".join(set(r['functions'])))
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
                all_code = []
                for text in df['text']:
                    r = extract_code(str(text))
                    all_code.extend(r['inline'])
                    all_code.extend(r['blocks'])
                st.success(f"✅ Found {len(all_code)} code snippets!")
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = "Use `print()` function. Example: ```python\nprint('Hello')\n```"
    
    if st.button("🚀 Run Demo", type="primary"):
        r = extract_code(sample)
        st.success("✅ Demo Complete!")
        st.write("**Inline:**", r['inline'])
        st.write("**Blocks:**", len(r['blocks']))

st.markdown("---")
st.markdown("**About**: Code Snippet Extraction")
st.caption("💡 Extracts code from text")
