"""
NLP App 031: Relationship Extraction
Real-world use case: Entity relationship identification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Relationship Extraction",
    page_icon="🔤",
    layout="wide"
)

st.title("🔗 Relationship Extraction")
st.markdown("""
**Real-world Use Case**: Extract entity relationships
- Person-Organization relationships
- Subject-Verb-Object patterns
- Ownership and association
- Action and interaction patterns
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

RELATIONSHIP_PATTERNS = {
    'employment': ['works for', 'employed by', 'working at', 'hired by'],
    'management': ['manages', 'supervises', 'leads', 'directs'],
    'ownership': ['owns', 'founded', 'created', 'established'],
    'location': ['lives in', 'located in', 'based in', 'from'],
    'association': ['member of', 'part of', 'belongs to', 'associated with']
}

def extract_relationships(text):
    """Extract relationships between entities"""
    relationships = []
    
    for rel_type, patterns in RELATIONSHIP_PATTERNS.items():
        for pattern in patterns:
            # Find sentences with relationship patterns
            regex = rf'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+{re.escape(pattern)}\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
            matches = re.findall(regex, text)
            for match in matches:
                relationships.append({
                    'subject': match[0],
                    'relation': pattern,
                    'object': match[1],
                    'type': rel_type
                })
    
    return {
        'relationships': relationships,
        'count': len(relationships),
        'types': list(set([r['type'] for r in relationships]))
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
            result = extract_relationships(user_input)
            st.success("✅ Complete!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Relationships Found", result['count'])
            with col2:
                st.metric("Relationship Types", len(result['types']))
            
            if result['relationships']:
                st.subheader("🔗 Extracted Relationships")
                for rel in result['relationships']:
                    st.write(f"**{rel['subject']}** *{rel['relation']}* **{rel['object']}** ({rel['type']})")
            else:
                st.info("No relationships found")
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
                all_rels = []
                for text in df['text']:
                    all_rels.extend(extract_relationships(str(text))['relationships'])
                st.success(f"✅ Found {len(all_rels)} relationships!")
                if all_rels:
                    rel_df = pd.DataFrame(all_rels[:50])
                    st.dataframe(rel_df, use_container_width=True)
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    sample = "John works for Google and manages Alice. Sarah founded Microsoft and lives in Seattle."
    
    if st.button("🚀 Run Demo", type="primary"):
        r = extract_relationships(sample)
        st.success("✅ Demo Complete!")
        st.metric("Relationships", r['count'])
        for rel in r['relationships']:
            st.write(f"**{rel['subject']}** *{rel['relation']}* **{rel['object']}**")

st.markdown("---")
st.markdown("**About**: Relationship Extraction")
st.caption("💡 Extracts relationships between named entities")
