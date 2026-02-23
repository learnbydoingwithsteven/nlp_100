"""
NLP App 019: Clickbait Detection
Real-world use case: Headline clickbait identification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Clickbait Detection",
    page_icon="🔤",
    layout="wide"
)

st.title("🎣 Clickbait Detection")
st.markdown("""
**Real-world Use Case**: Headline and title clickbait identification
- Detect sensationalist headlines
- Identify clickbait patterns
- Content quality assessment
- News credibility analysis
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
sensitivity = st.sidebar.slider("Detection Sensitivity", 0.0, 1.0, 0.5, 0.1)
st.sidebar.markdown("---")
st.sidebar.markdown("**Clickbait Indicators:**")
st.sidebar.markdown("""
- ❓ Question Hooks
- 🔢 Numbered Lists
- 😱 Sensationalism
- 🚨 Urgency Words
- 🎯 You/Your Language
""")

# Clickbait patterns
CLICKBAIT_PATTERNS = {
    'question_hooks': ['will', 'can', 'should', 'what', 'why', 'how', 'who', 'when', 'where', 'which'],
    'numbered_lists': [r'\d+\s+(?:ways|reasons|things|facts|secrets|tips|tricks)', r'top\s+\d+', r'\d+\s+of\s+the'],
    'sensational': ['shocking', 'unbelievable', 'amazing', 'incredible', 'mind-blowing', 'jaw-dropping', 'outrageous', 'insane'],
    'urgency': ['now', 'today', 'urgent', 'breaking', 'just', 'finally', 'dont miss', 'last chance'],
    'direct_address': ['you wont believe', 'you need', 'you have to', 'youll never', 'this will', 'you must see']
}

def detect_clickbait(text, sensitivity=0.5):
    """Detect clickbait in headlines/titles"""
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words)
    
    # Clickbait scores
    clickbait_score = 0
    found_indicators = {}
    
    # Questions (especially at start)
    if text.strip().endswith('?'):
        clickbait_score += 0.4
        found_indicators['question_mark'] = ['?']
    
    # Question words
    q_words = sum(1 for word in CLICKBAIT_PATTERNS['question_hooks'] if word in text_lower)
    if q_words > 0:
        clickbait_score += q_words * 0.15
        found_indicators['question_words'] = [w for w in CLICKBAIT_PATTERNS['question_hooks'] if w in text_lower]
    
    # Numbered lists
    for pattern in CLICKBAIT_PATTERNS['numbered_lists']:
        if re.search(pattern, text_lower):
            clickbait_score += 0.5
            if 'numbered_lists' not in found_indicators:
                found_indicators['numbered_lists'] = []
            found_indicators['numbered_lists'].append('list pattern')
    
    # Sensational words
    sensational_found = []
    for word in CLICKBAIT_PATTERNS['sensational']:
        if word in text_lower:
            count = text_lower.count(word)
            clickbait_score += count * 0.3
            sensational_found.extend([word] * count)
    if sensational_found:
        found_indicators['sensational'] = sensational_found
    
    # Urgency words
    urgency_found = []
    for word in CLICKBAIT_PATTERNS['urgency']:
        if word in text_lower:
            count = text_lower.count(word)
            clickbait_score += count * 0.2
            urgency_found.extend([word] * count)
    if urgency_found:
        found_indicators['urgency'] = urgency_found
    
    # Direct address patterns
    direct_found = []
    for phrase in CLICKBAIT_PATTERNS['direct_address']:
        if phrase in text_lower:
            clickbait_score += 0.4
            direct_found.append(phrase)
    if direct_found:
        found_indicators['direct_address'] = direct_found
    
    # All caps words
    caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
    if caps_words:
        clickbait_score += len(caps_words) * 0.2
        found_indicators['caps'] = caps_words
    
    # Excessive punctuation
    exc_count = text.count('!')
    if exc_count > 1:
        clickbait_score += exc_count * 0.15
    
    # Adjust by sensitivity
    clickbait_probability = min(clickbait_score * (0.7 + sensitivity * 0.6), 1.0)
    
    # Classification
    if clickbait_probability >= 0.7:
        classification = "🎣 High Clickbait"
        risk = "High"
    elif clickbait_probability >= 0.5:
        classification = "⚠️ Likely Clickbait"
        risk = "Medium"
    elif clickbait_probability >= 0.3:
        classification = "🤔 Possibly Clickbait"
        risk = "Low"
    else:
        classification = "✅ Not Clickbait"
        risk = "Minimal"
    
    return {
        'text': text,
        'clickbait_probability': clickbait_probability,
        'classification': classification,
        'risk': risk,
        'found_indicators': found_indicators,
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
    
    if st.button("🔍 Detect Clickbait", type="primary"):
        if user_input.strip():
            with st.spinner("Analyzing..."):
                result = detect_clickbait(user_input, sensitivity)
            
            st.success("✅ Analysis Complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Classification", result['classification'])
            with col2:
                st.metric("Probability", f"{result['clickbait_probability']:.1%}")
            with col3:
                st.metric("Risk", result['risk'])
            
            st.subheader("📊 Clickbait Score")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['clickbait_probability'] * 100,
                title={'text': "Clickbait Probability (%)"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': 'red' if result['clickbait_probability'] >= 0.7 else 'orange' if result['clickbait_probability'] >= 0.5 else 'yellow' if result['clickbait_probability'] >= 0.3 else 'green'},
                       'steps': [
                           {'range': [0, 30], 'color': "lightgreen"},
                           {'range': [30, 50], 'color': "lightyellow"},
                           {'range': [50, 70], 'color': "lightsalmon"},
                           {'range': [70, 100], 'color': "lightcoral"}]}
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            if result['found_indicators']:
                st.subheader("🔍 Detected Clickbait Indicators")
                for category, indicators in result['found_indicators'].items():
                    st.write(f"**{category.replace('_', ' ').title()}**: {', '.join(map(str, set(indicators)))}")
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
                    result = detect_clickbait(str(text), sensitivity)
                    results.append({
                        'text': result['text'][:60] + '...',
                        'classification': result['classification'],
                        'probability': result['clickbait_probability']
                    })
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Analyzed {len(results_df)} headlines!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total", len(results_df))
                with col2:
                    clickbait = len(results_df[results_df['probability'] >= 0.5])
                    st.metric("Clickbait", clickbait)
                with col3:
                    avg = results_df['probability'].mean()
                    st.metric("Avg Score", f"{avg:.1%}")
                
                fig = px.histogram(results_df, x='probability', nbins=20,
                                  title='Clickbait Distribution')
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
        "You Won't Believe What This Celebrity Did Next!",
        "10 Shocking Facts About Health That Will Change Your Life",
        "Study Finds Correlation Between Exercise and Health Outcomes",
        "Scientists Discover New Species in Amazon Rainforest"
    ]
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        for text in samples:
            result = detect_clickbait(text, sensitivity)
            results.append({
                'text': text,
                'classification': result['classification'],
                'probability': result['clickbait_probability']
            })
        
        results_df = pd.DataFrame(results)
        st.success("✅ Complete!")
        
        for idx, row in results_df.iterrows():
            st.info(f"{row['classification']} ({row['probability']:.1%})")
            st.caption(row['text'])
        
        fig = px.bar(results_df, x=results_df.index, y='probability',
                     title='Clickbait Scores',
                     color='probability', color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Clickbait Detection - Identify sensationalist headlines")
st.caption("💡 Detects question hooks, numbered lists, urgency words, and sensational language")
