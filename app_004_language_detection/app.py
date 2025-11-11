"""
NLP App 004: Language Detection
Real-world use case: Multi-language identification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from langdetect import detect, detect_langs, DetectorFactory
DetectorFactory.seed = 0  # For consistent results

st.set_page_config(
    page_title="Language Detection",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Language Detection")
st.markdown("""
**Real-world Use Case**: Multi-language identification
- Analyze and process text with real NLP techniques
- Extract meaningful insights and patterns
- Visualize results comprehensively
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

def process_text(text):
    '''Detect the language of text'''
    try:
        lang_code = detect(text)
        lang_probs = detect_langs(text)
        
        # Language name mapping
        lang_names = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
            'zh-cn': 'Chinese', 'ar': 'Arabic', 'hi': 'Hindi', 'ko': 'Korean',
            'nl': 'Dutch', 'sv': 'Swedish', 'no': 'Norwegian', 'da': 'Danish'
        }
        
        detected_lang = lang_names.get(lang_code, lang_code.upper())
        
        # Parse probabilities
        prob_dict = {}
        for lp in lang_probs:
            parts = str(lp).split(':')
            if len(parts) == 2:
                prob_dict[parts[0]] = float(parts[1])
        
        top_prob = max(prob_dict.values()) if prob_dict else 0.0
        
        return {
            'text': text,
            'language_code': lang_code,
            'language_name': detected_lang,
            'confidence': top_prob,
            'text_length': len(text),
            'word_count': len(text.split()),
            'all_probabilities': str(prob_dict)
        }
    except Exception as e:
        return {
            'text': text,
            'error': str(e),
            'language_code': 'unknown',
            'language_name': 'Unknown',
            'confidence': 0.0,
            'word_count': len(text.split())
        }

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Processing")
    
    user_input = st.text_area(
        "Enter text to process:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    if st.button("🔍 Analyze", type="primary"):
        if user_input.strip():
            with st.spinner("Processing..."):
                result = process_text(user_input)
            
            st.success("✅ Analysis Complete!")
            
            # Display key metrics
            metrics_cols = st.columns(min(4, len(result)))
            metric_keys = list(result.keys())[:4]
            
            for idx, key in enumerate(metric_keys):
                if key != 'text' and isinstance(result[key], (int, float, str)):
                    with metrics_cols[idx]:
                        value = result[key]
                        if isinstance(value, float):
                            st.metric(key.replace('_', ' ').title(), f"{{value:.3f}}")
                        else:
                            st.metric(key.replace('_', ' ').title(), value)
            
            # Detailed results
            st.subheader("📊 Detailed Results")
            
            # Create two columns for display
            col1, col2 = st.columns(2)
            
            with col1:
                st.json({k: v for k, v in result.items() if k != 'text' and not k.startswith('_')})
            
            with col2:
                # Visualization if numeric data available
                numeric_keys = [k for k, v in result.items() if isinstance(v, (int, float)) and k not in ['length', 'word_count']]
                if numeric_keys:
                    values = [result[k] for k in numeric_keys]
                    fig = px.bar(x=numeric_keys, y=values, title='Analysis Metrics')
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please enter some text to analyze.")

# Mode: Batch Processing
elif mode == "Batch Processing":
    st.header("📚 Batch Processing")
    
    uploaded_file = st.file_uploader("Upload CSV with 'text' column", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {{len(df)}} rows")
        
        if 'text' in df.columns:
            if st.button("🔍 Process All", type="primary"):
                results = []
                progress_bar = st.progress(0)
                
                for idx, text in enumerate(df['text']):
                    result = process_text(str(text))
                    results.append(result)
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Processed {{len(results_df)}} texts!")
                
                # Summary stats
                st.subheader("📊 Summary Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Processed", len(results_df))
                with col2:
                    if 'word_count' in results_df.columns:
                        st.metric("Avg Word Count", f"{{results_df['word_count'].mean():.1f}}")
                with col3:
                    numeric_cols = results_df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        st.metric("Total Metrics", len(numeric_cols))
                
                # Visualizations
                numeric_cols = results_df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    col_to_plot = numeric_cols[0]
                    fig = px.histogram(results_df, x=col_to_plot, title=f'{{col_to_plot.replace("_", " ").title()}} Distribution')
                    st.plotly_chart(fig, use_container_width=True)
                
                # Results table
                st.subheader("📋 Detailed Results")
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
    
    sample_texts = ['Hello, how are you today? This is a sample text in English.', 'Bonjour, comment allez-vous? Ceci est un exemple de texte en français.', 'Hola, ¿cómo estás? Este es un texto de ejemplo en español.', 'Hallo, wie geht es dir? Dies ist ein Beispieltext auf Deutsch.', 'Ciao, come stai? Questo è un testo di esempio in italiano.']
    
    st.write(f"Processing {{len(sample_texts)}} sample texts...")
    
    # Display sample texts
    with st.expander("👁️ View Sample Texts"):
        for i, text in enumerate(sample_texts, 1):
            st.write(f"{{i}}. {{text}}")
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        with st.spinner("Processing..."):
            for text in sample_texts:
                result = process_text(text)
                results.append(result)
        
        results_df = pd.DataFrame(results)
        
        st.success("✅ Demo Complete!")
        
        # Display results
        st.subheader("📋 Analysis Results")
        for idx, row in results_df.iterrows():
            with st.expander(f"📄 Sample {{idx+1}}"):
                text_preview = row['text'][:100] + ('...' if len(row['text']) > 100 else '')
                st.write(f"**Text**: {{text_preview}}")
                
                # Display key metrics
                metric_cols = st.columns(min(4, len(row) - 1))
                displayed = 0
                for key, value in row.items():
                    if key != 'text' and displayed < 4 and isinstance(value, (int, float, str)):
                        with metric_cols[displayed]:
                            if isinstance(value, float):
                                st.metric(key.replace('_', ' ').title(), f"{{value:.3f}}")
                            else:
                                st.metric(key.replace('_', ' ').title(), value)
                        displayed += 1
        
        # Visualizations
        st.subheader("📊 Results Visualization")
        numeric_cols = results_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            col_to_plot = numeric_cols[0]
            fig = px.bar(
                results_df.reset_index(),
                x='index',
                y=col_to_plot,
                title=f'{{col_to_plot.replace("_", " ").title()}} by Sample',
                labels={'index': 'Sample #', col_to_plot: col_to_plot.replace("_", " ").title()}
            )
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown(f"**About**: Language Detection - Multi-language identification")
