"""
NLP App 018: Political Bias Detection
Real-world use case: News article bias analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Political Bias Detection",
    page_icon="🔤",
    layout="wide"
)

st.title("🗳️ Political Bias Detection")
st.markdown("""
**Real-world Use Case**: News article and text bias analysis
- Detect political lean in content
- Analyze language bias patterns
- Media bias assessment
- Content neutrality checking
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
st.sidebar.markdown("---")
st.sidebar.markdown("**Bias Categories:**")
st.sidebar.markdown("""
- 🔵 Left/Liberal
- ⚪ Center/Neutral
- 🔴 Right/Conservative
""")

# Political bias keywords (simplified for demonstration)
BIAS_KEYWORDS = {
    'left': ['progressive', 'liberal', 'social justice', 'equality', 'diversity', 'climate change', 'universal healthcare', 'reform', 'regulation', 'workers rights'],
    'right': ['conservative', 'traditional', 'freedom', 'liberty', 'free market', 'deregulation', 'law and order', 'strong borders', 'family values', 'fiscal responsibility'],
    'neutral': ['according to', 'reported', 'stated', 'analysis shows', 'data indicates', 'research suggests', 'officials say', 'experts note']
}

def detect_political_bias(text):
    """Detect political bias in text"""
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words)
    
    # Score each bias category
    left_score = 0
    right_score = 0
    neutral_score = 0
    found_left = []
    found_right = []
    found_neutral = []
    
    # Check for bias keywords
    for keyword in BIAS_KEYWORDS['left']:
        if keyword in text_lower:
            count = text_lower.count(keyword)
            left_score += count * 0.4
            found_left.extend([keyword] * count)
    
    for keyword in BIAS_KEYWORDS['right']:
        if keyword in text_lower:
            count = text_lower.count(keyword)
            right_score += count * 0.4
            found_right.extend([keyword] * count)
    
    for phrase in BIAS_KEYWORDS['neutral']:
        if phrase in text_lower:
            count = text_lower.count(phrase)
            neutral_score += count * 0.3
            found_neutral.extend([phrase] * count)
    
    # Emotional vs factual language
    emotional_words = ['outrageous', 'shocking', 'terrible', 'wonderful', 'amazing', 'horrific']
    emotional_count = sum(1 for word in emotional_words if word in text_lower)
    if emotional_count > 2:
        # Emotional language reduces neutrality
        neutral_score -= 0.3
    
    # Determine bias
    total_score = left_score + right_score + neutral_score
    
    if total_score == 0 or neutral_score > (left_score + right_score):
        bias = 'center'
        bias_display = '⚪ Center/Neutral'
        lean_score = 0
    elif left_score > right_score:
        bias = 'left'
        bias_display = '🔵 Left/Liberal'
        lean_score = (left_score / max(total_score, 0.1)) * 100
    else:
        bias = 'right'
        bias_display = '🔴 Right/Conservative'
        lean_score = (right_score / max(total_score, 0.1)) * 100
    
    # Confidence
    if total_score == 0:
        confidence = 0.5
    else:
        max_score = max(left_score, right_score, neutral_score)
        confidence = max_score / total_score
    
    return {
        'text': text,
        'bias': bias,
        'bias_display': bias_display,
        'lean_score': lean_score,
        'confidence': confidence,
        'left_score': left_score,
        'right_score': right_score,
        'neutral_score': neutral_score,
        'found_left': found_left,
        'found_right': found_right,
        'found_neutral': found_neutral,
        'word_count': word_count
    }

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Processing")
    
    user_input = st.text_area(
        "Enter text to process:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    if st.button("🔍 Analyze Bias", type="primary"):
        if user_input.strip():
            with st.spinner("Analyzing..."):
                result = detect_political_bias(user_input)
            
            st.success("✅ Analysis Complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Detected Bias", result['bias_display'])
            with col2:
                st.metric("Confidence", f"{result['confidence']:.1%}")
            with col3:
                st.metric("Lean Score", f"{result['lean_score']:.0f}")
            
            # Bias scores
            st.subheader("📊 Bias Analysis")
            scores_df = pd.DataFrame({
                'Category': ['Left', 'Center', 'Right'],
                'Score': [result['left_score'], result['neutral_score'], result['right_score']]
            })
            fig = px.bar(scores_df, x='Category', y='Score',
                        title='Political Bias Scores',
                        color='Category',
                        color_discrete_map={'Left': 'blue', 'Center': 'gray', 'Right': 'red'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Found indicators
            st.subheader("🔍 Detected Keywords")
            col1, col2, col3 = st.columns(3)
            with col1:
                if result['found_left']:
                    st.write("**Left:** " + ', '.join(set(result['found_left'])))
            with col2:
                if result['found_neutral']:
                    st.write("**Neutral:** " + ', '.join(set(result['found_neutral'])))
            with col3:
                if result['found_right']:
                    st.write("**Right:** " + ', '.join(set(result['found_right'])))
        else:
            st.warning("Please enter some text.")

# Mode: Batch Processing
elif mode == "Batch Processing":
    st.header("📚 Batch Processing")
    
    uploaded_file = st.file_uploader("Upload CSV with 'text' column", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} rows")
        
        if 'text' in df.columns:
            if st.button("🔍 Analyze All", type="primary"):
                results = []
                progress_bar = st.progress(0)
                
                for idx, text in enumerate(df['text']):
                    result = detect_political_bias(str(text))
                    results.append({
                        'text': result['text'][:60] + '...',
                        'bias': result['bias_display'],
                        'confidence': result['confidence']
                    })
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Analyzed {len(results_df)} texts!")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total", len(results_df))
                with col2:
                    left = len(results_df[results_df['bias'].str.contains('Left')])
                    st.metric("Left", left)
                with col3:
                    center = len(results_df[results_df['bias'].str.contains('Center')])
                    st.metric("Center", center)
                with col4:
                    right = len(results_df[results_df['bias'].str.contains('Right')])
                    st.metric("Right", right)
                
                bias_counts = results_df['bias'].value_counts()
                fig = px.pie(values=bias_counts.values, names=bias_counts.index,
                            title='Bias Distribution')
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
    
    samples = [
        "We need progressive reform to ensure equality and social justice for all. Climate change requires immediate regulation.",
        "Traditional family values and fiscal responsibility are essential. Free market solutions and deregulation promote freedom.",
        "According to the data, research suggests that officials say the analysis shows mixed results.",
        "Universal healthcare is a human right. Workers rights and diversity strengthen our communities."
    ]
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        for text in samples:
            result = detect_political_bias(text)
            results.append({
                'text': text[:50] + '...',
                'bias': result['bias_display'],
                'confidence': result['confidence']
            })
        
        results_df = pd.DataFrame(results)
        st.success("✅ Complete!")
        
        for idx, row in results_df.iterrows():
            st.info(f"{row['bias']} ({row['confidence']:.1%}): {row['text']}")
        
        fig = px.bar(results_df, x=results_df.index, y='confidence',
                     title='Confidence Scores',
                     color='confidence', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Political Bias Detection - Analyze political lean in text")
st.caption("💡 Based on keyword patterns and language analysis. For educational purposes.")
