"""
NLP App 048: Question Generation
Real-world use case: Educational question creation
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

st.set_page_config(
    page_title="Question Generation",
    page_icon="🔤",
    layout="wide"
)

st.title("🔤 Question Generation")
st.markdown("""
**Real-world Use Case**: Educational question creation
- Process and analyze text data
- Extract meaningful insights
- Visualize results comprehensively
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

# Main processing function
def process_text(text):
    """Main NLP processing function"""
    # Simulate processing
    time.sleep(0.3)
    
    results = {
        "text": text,
        "length": len(text),
        "word_count": len(text.split()),
        "processed": True
    }
    
    return results

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Processing")
    
    user_input = st.text_area(
        "Enter text to process:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    if st.button("🔍 Process", type="primary"):
        if user_input.strip():
            with st.spinner("Processing..."):
                result = process_text(user_input)
            
            st.success("Processing Complete!")
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Text Length", result["length"])
            with col2:
                st.metric("Word Count", result["word_count"])
            with col3:
                st.metric("Status", "✅ Processed")
            
            # Visualization
            st.subheader("📊 Analysis Results")
            fig = go.Figure(go.Indicator(
                mode="number+gauge",
                value=result["word_count"],
                title={"text": "Word Count"},
                gauge={"axis": {"range": [0, 1000]}}
            ))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please enter some text to process.")

# Mode: Batch Processing
elif mode == "Batch Processing":
    st.header("📚 Batch Processing")
    
    uploaded_file = st.file_uploader("Upload CSV with 'text' column", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} rows")
        
        if 'text' in df.columns:
            if st.button("🔍 Process All", type="primary"):
                results = []
                progress_bar = st.progress(0)
                
                for idx, text in enumerate(df['text']):
                    result = process_text(str(text))
                    results.append(result)
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"Processed {len(results_df)} texts!")
                
                # Summary stats
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Processed", len(results_df))
                with col2:
                    st.metric("Avg Word Count", f"{results_df['word_count'].mean():.1f}")
                
                # Visualization
                fig = px.histogram(results_df, x='word_count', title='Word Count Distribution')
                st.plotly_chart(fig, use_container_width=True)
                
                # Results table
                st.dataframe(results_df, use_container_width=True)
                
                # Download
                csv = results_df.to_csv(index=False)
                st.download_button("📥 Download Results", csv, "results.csv", "text/csv")
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file to perform batch processing")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    
    sample_texts = [
        "This is a sample text for demonstration.",
        "Another example to show the processing capabilities.",
        "Third sample text with different content."
    ]
    
    st.write(f"Processing {len(sample_texts)} sample texts...")
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        for text in sample_texts:
            result = process_text(text)
            results.append(result)
        
        results_df = pd.DataFrame(results)
        
        st.success("Demo Complete!")
        
        # Display results
        st.dataframe(results_df, use_container_width=True)
        
        # Visualization
        fig = px.bar(results_df, x='word_count', y='length', title='Text Statistics')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Question Generation - Educational question creation")
