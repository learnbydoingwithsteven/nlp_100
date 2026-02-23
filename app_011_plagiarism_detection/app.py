"""
NLP App 011: Plagiarism Detection
Real-world use case: Document similarity checking
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter
from itertools import combinations

st.set_page_config(
    page_title="Plagiarism Detection",
    page_icon="🔤",
    layout="wide"
)

st.title("🔍 Plagiarism Detection")
st.markdown("""
**Real-world Use Case**: Document similarity and plagiarism checking
- Text similarity scoring
- N-gram overlap detection
- Word-level and phrase-level matching
- Plagiarism risk assessment
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Compare Two Texts", "Batch Processing", "Demo"])
ngram_size = st.sidebar.slider("N-gram Size", 2, 5, 3)
st.sidebar.markdown("---")
st.sidebar.markdown("**Similarity Metrics:**")
st.sidebar.markdown("""
- 📊 Word Overlap
- 🔤 N-gram Matching
- 📝 Jaccard Similarity
- ⚠️ Plagiarism Risk
""")

def preprocess_text(text):
    """Clean and normalize text"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_ngrams(text, n=3):
    """Extract n-grams from text"""
    words = text.split()
    ngrams = [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
    return ngrams

def calculate_jaccard_similarity(set1, set2):
    """Calculate Jaccard similarity coefficient"""
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0

def detect_plagiarism(text1, text2, ngram_size=3):
    """Detect plagiarism between two texts"""
    
    # Preprocess
    clean_text1 = preprocess_text(text1)
    clean_text2 = preprocess_text(text2)
    
    # Word-level analysis
    words1 = set(clean_text1.split())
    words2 = set(clean_text2.split())
    
    word_overlap = len(words1.intersection(words2))
    total_unique = len(words1.union(words2))
    word_similarity = word_overlap / total_unique if total_unique > 0 else 0
    
    # N-gram analysis
    ngrams1 = get_ngrams(clean_text1, ngram_size)
    ngrams2 = get_ngrams(clean_text2, ngram_size)
    
    ngrams_set1 = set(ngrams1)
    ngrams_set2 = set(ngrams2)
    
    ngram_overlap = len(ngrams_set1.intersection(ngrams_set2))
    total_ngrams = len(ngrams_set1.union(ngrams_set2))
    ngram_similarity = ngram_overlap / total_ngrams if total_ngrams > 0 else 0
    
    # Jaccard similarity
    jaccard_words = calculate_jaccard_similarity(words1, words2)
    jaccard_ngrams = calculate_jaccard_similarity(ngrams_set1, ngrams_set2)
    
    # Overall similarity (weighted average)
    overall_similarity = (word_similarity * 0.3 + ngram_similarity * 0.4 + jaccard_ngrams * 0.3)
    
    # Plagiarism risk assessment
    if overall_similarity >= 0.7:
        risk_level = "🔴 Very High"
        assessment = "Likely Plagiarism"
    elif overall_similarity >= 0.5:
        risk_level = "🟠 High"
        assessment = "Suspicious"
    elif overall_similarity >= 0.3:
        risk_level = "🟡 Medium"
        assessment = "Some Overlap"
    elif overall_similarity >= 0.15:
        risk_level = "🟢 Low"
        assessment = "Minor Similarity"
    else:
        risk_level = "✅ Very Low"
        assessment = "Original"
    
    # Common phrases
    common_ngrams = list(ngrams_set1.intersection(ngrams_set2))[:10]
    common_words = list(words1.intersection(words2))[:20]
    
    return {
        'text1': text1,
        'text2': text2,
        'overall_similarity': overall_similarity,
        'word_similarity': word_similarity,
        'ngram_similarity': ngram_similarity,
        'jaccard_words': jaccard_words,
        'jaccard_ngrams': jaccard_ngrams,
        'word_overlap': word_overlap,
        'ngram_overlap': ngram_overlap,
        'risk_level': risk_level,
        'assessment': assessment,
        'common_ngrams': common_ngrams,
        'common_words': common_words,
        'word_count1': len(text1.split()),
        'word_count2': len(text2.split())
    }

# Mode: Compare Two Texts
if mode == "Compare Two Texts":
    st.header("📝 Compare Two Documents")
    
    col1, col2 = st.columns(2)
    with col1:
        text1 = st.text_area(
            "Document 1 (Original):",
            height=200,
            placeholder="Paste the original document here..."
        )
    with col2:
        text2 = st.text_area(
            "Document 2 (To Check):",
            height=200,
            placeholder="Paste the document to check here..."
        )
    
    if st.button("🔍 Check for Plagiarism", type="primary"):
        if text1.strip() and text2.strip():
            with st.spinner("Analyzing similarity..."):
                result = detect_plagiarism(text1, text2, ngram_size)
            
            st.success("✅ Analysis Complete!")
            
            # Main metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Overall Similarity", f"{result['overall_similarity']:.1%}")
            with col2:
                st.metric("Assessment", result['assessment'])
            with col3:
                st.metric("Risk Level", result['risk_level'])
            with col4:
                st.metric("Common Words", result['word_overlap'])
            
            # Similarity gauge
            st.subheader("📊 Similarity Score")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['overall_similarity'] * 100,
                title={'text': "Similarity (%)"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': 'red' if result['overall_similarity'] >= 0.7 else 'orange' if result['overall_similarity'] >= 0.5 else 'yellow' if result['overall_similarity'] >= 0.3 else 'green'},
                       'steps': [
                           {'range': [0, 15], 'color': "lightgreen"},
                           {'range': [15, 30], 'color': "lightyellow"},
                           {'range': [30, 50], 'color': "lightgoldenrodyellow"},
                           {'range': [50, 70], 'color': "lightsalmon"},
                           {'range': [70, 100], 'color': "lightcoral"}]}
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics
            st.subheader("📈 Detailed Metrics")
            metrics_df = pd.DataFrame({
                'Metric': ['Word Similarity', 'N-gram Similarity', 'Jaccard (Words)', 'Jaccard (N-grams)', 'Overall Similarity'],
                'Score': [
                    f"{result['word_similarity']:.1%}",
                    f"{result['ngram_similarity']:.1%}",
                    f"{result['jaccard_words']:.1%}",
                    f"{result['jaccard_ngrams']:.1%}",
                    f"{result['overall_similarity']:.1%}"
                ]
            })
            
            col1, col2 = st.columns(2)
            with col1:
                st.table(metrics_df)
            with col2:
                # Bar chart
                fig = px.bar(metrics_df, x='Metric', y=[float(s.strip('%'))/100 for s in metrics_df['Score']],
                            title='Similarity Breakdown',
                            labels={'y': 'Score'},
                            color=[float(s.strip('%'))/100 for s in metrics_df['Score']],
                            color_continuous_scale='RdYlGn_r')
                st.plotly_chart(fig, use_container_width=True)
            
            # Common elements
            st.subheader("🔍 Common Elements")
            
            col1, col2 = st.columns(2)
            with col1:
                if result['common_words']:
                    st.markdown("**Common Words:**")
                    st.write(", ".join(result['common_words'][:20]))
                else:
                    st.info("No common words found")
            
            with col2:
                if result['common_ngrams']:
                    st.markdown(f"**Common {ngram_size}-grams:**")
                    for ngram in result['common_ngrams'][:10]:
                        st.write(f"• {ngram}")
                else:
                    st.info("No common n-grams found")
        else:
            st.warning("Please enter both documents to compare.")

# Mode: Batch Processing
elif mode == "Batch Processing":
    st.header("📚 Batch Processing")
    
    uploaded_file = st.file_uploader("Upload CSV with 'text' column", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} rows")
        
        if 'text1' in df.columns and 'text2' in df.columns:
            if st.button("🔍 Check All Pairs", type="primary"):
                results = []
                progress_bar = st.progress(0)
                
                for idx, row in df.iterrows():
                    result = detect_plagiarism(str(row['text1']), str(row['text2']), ngram_size)
                    simple_result = {
                        'pair': f"Pair {idx+1}",
                        'similarity': result['overall_similarity'],
                        'assessment': result['assessment'],
                        'risk_level': result['risk_level']
                    }
                    results.append(simple_result)
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Analyzed {len(results_df)} document pairs!")
                
                # Summary
                st.subheader("📊 Summary Statistics")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Pairs", len(results_df))
                with col2:
                    high_risk = len(results_df[results_df['similarity'] >= 0.7])
                    st.metric("High Risk", high_risk)
                with col3:
                    avg_sim = results_df['similarity'].mean()
                    st.metric("Avg Similarity", f"{avg_sim:.1%}")
                with col4:
                    original = len(results_df[results_df['similarity'] < 0.15])
                    st.metric("Original", original)
                
                # Visualization
                fig = px.histogram(results_df, x='similarity', nbins=20,
                                  title='Similarity Distribution',
                                  labels={'similarity': 'Similarity Score'})
                st.plotly_chart(fig, use_container_width=True)
                
                # Results table
                st.dataframe(results_df, use_container_width=True)
                
                # Download
                csv = results_df.to_csv(index=False)
                st.download_button("📥 Download Results", csv, "results.csv", "text/csv")
        else:
            st.error("CSV must contain 'text1' and 'text2' columns")
    else:
        st.info("Upload a CSV file to perform batch processing")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    st.markdown("**Testing with document pairs of varying similarity**")
    
    demo_pairs = [
        {
            'name': 'Identical Text (Exact Copy)',
            'text1': 'Machine learning is a subset of artificial intelligence that enables systems to learn from data.',
            'text2': 'Machine learning is a subset of artificial intelligence that enables systems to learn from data.'
        },
        {
            'name': 'High Similarity (Paraphrased)',
            'text1': 'The quick brown fox jumps over the lazy dog in the park.',
            'text2': 'A fast brown fox leaps over a lazy dog in the park area.'
        },
        {
            'name': 'Medium Similarity (Partial Match)',
            'text1': 'Python is a versatile programming language used for web development and data science.',
            'text2': 'Python is used for web development. JavaScript is great for frontend applications.'
        },
        {
            'name': 'Low Similarity (Different Topics)',
            'text1': 'The weather today is sunny and warm with clear blue skies.',
            'text2': 'Quantum computing uses principles of quantum mechanics to process information.'
        },
        {
            'name': 'Original Content (No Match)',
            'text1': 'Artificial intelligence is transforming industries worldwide.',
            'text2': 'Basketball players practice daily to improve their performance.'
        }
    ]
    
    with st.expander("👁️ View Demo Pairs"):
        for i, pair in enumerate(demo_pairs, 1):
            st.write(f"**{i}. {pair['name']}**")
            st.write(f"Doc 1: {pair['text1']}")
            st.write(f"Doc 2: {pair['text2']}")
            st.write("---")
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        with st.spinner("Analyzing all pairs..."):
            for pair in demo_pairs:
                result = detect_plagiarism(pair['text1'], pair['text2'], ngram_size)
                results.append({
                    'pair': pair['name'],
                    'similarity': result['overall_similarity'],
                    'assessment': result['assessment'],
                    'risk': result['risk_level']
                })
        
        results_df = pd.DataFrame(results)
        st.success("✅ Demo Complete!")
        
        # Summary
        st.subheader("📊 Demo Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Pairs Tested", len(results_df))
        with col2:
            avg_sim = results_df['similarity'].mean()
            st.metric("Avg Similarity", f"{avg_sim:.1%}")
        with col3:
            high_risk = len(results_df[results_df['similarity'] >= 0.7])
            st.metric("High Risk", high_risk)
        
        # Results
        st.subheader("📋 Results")
        for idx, row in results_df.iterrows():
            with st.expander(f"{row['risk']} {row['pair']}"):
                cols = st.columns(3)
                with cols[0]:
                    st.metric("Similarity", f"{row['similarity']:.1%}")
                with cols[1]:
                    st.metric("Assessment", row['assessment'])
                with cols[2]:
                    st.metric("Risk", row['risk'])
        
        # Visualization
        fig = px.bar(results_df, x='pair', y='similarity',
                     title='Similarity Scores by Pair',
                     labels={'similarity': 'Similarity Score', 'pair': 'Document Pair'},
                     color='similarity', color_continuous_scale='RdYlGn_r')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Plagiarism Detection - Document similarity checking using n-gram analysis")
st.caption("💡 Tip: Adjust n-gram size in sidebar for different granularity. Higher values catch phrase-level copying.")
