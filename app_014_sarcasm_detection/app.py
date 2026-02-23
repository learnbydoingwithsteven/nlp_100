"""
NLP App 014: Sarcasm Detection
Real-world use case: Sarcastic text identification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Sarcasm Detection",
    page_icon="🔤",
    layout="wide"
)

st.title("😏 Sarcasm Detection")
st.markdown("""
**Real-world Use Case**: Sarcastic text and irony identification
- Detect sarcastic language patterns
- Identify ironic statements
- Analyze sentiment contradictions
- Social media and review analysis
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
sensitivity = st.sidebar.slider("Detection Sensitivity", 0.0, 1.0, 0.5, 0.1)
st.sidebar.markdown("---")
st.sidebar.markdown("**Sarcasm Indicators:**")
st.sidebar.markdown("""
- 🎭 Exaggeration
- 🔄 Contradiction
- 😮 Surprise Words
- ✨ Quotation Marks
- 📝 Ironic Phrases
""")

# Sarcasm indicators
SARCASM_INDICATORS = {
    'exaggeration': ['totally', 'absolutely', 'completely', 'perfectly', 'super', 'extremely', 'incredibly', 'literally', 'obviously', 'clearly'],
    'positive_sarcasm': ['oh great', 'yeah right', 'sure thing', 'oh wonderful', 'fantastic', 'brilliant idea', 'how nice', 'well done', 'congratulations'],
    'surprise': ['wow', 'oh', 'gee', 'really', 'seriously', 'shocking', 'amazing', 'unbelievable'],
    'ironic_phrases': ['as if', 'not really', 'like that', 'could be worse', 'just perfect', 'exactly what', 'just what'],
    'negative_positive': ['love how', 'enjoy the', 'thanks for', 'appreciate the', 'glad that']
}

def detect_sarcasm(text, sensitivity=0.5):
    """Detect sarcasm in text"""
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words)
    
    # Sarcasm scoring
    sarcasm_scores = {}
    found_indicators = {}
    
    # Check for sarcasm indicators
    for category, phrases in SARCASM_INDICATORS.items():
        score = 0
        found = []
        for phrase in phrases:
            if phrase in text_lower:
                count = text_lower.count(phrase)
                score += count * 0.25
                found.extend([phrase] * count)
        if score > 0:
            sarcasm_scores[category] = score
            found_indicators[category] = found
    
    # Quotation marks (often indicate irony)
    quote_count = text.count('"') + text.count("'")
    if quote_count >= 2:
        sarcasm_scores['quotation'] = min(quote_count * 0.1, 0.4)
        found_indicators['quotation'] = [f'{quote_count} quotes']
    
    # Ellipsis (trailing off sarcastically)
    if '...' in text or text.count('.') > 3:
        sarcasm_scores['ellipsis'] = 0.2
        found_indicators['ellipsis'] = ['...']
    
    # ALL CAPS words (emphasis)
    caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
    if caps_words:
        sarcasm_scores['caps_emphasis'] = min(len(caps_words) * 0.15, 0.5)
        found_indicators['caps_emphasis'] = caps_words
    
    # Positive words with negative context indicators
    positive_words = ['great', 'good', 'nice', 'wonderful', 'amazing', 'excellent', 'perfect']
    negative_context = ['not', "n't", 'never', 'no', 'hardly', 'barely']
    
    for pos in positive_words:
        for neg in negative_context:
            pattern = f"{neg}.*{pos}|{pos}.*{neg}"
            if re.search(pattern, text_lower):
                sarcasm_scores['contradiction'] = sarcasm_scores.get('contradiction', 0) + 0.3
                if 'contradiction' not in found_indicators:
                    found_indicators['contradiction'] = []
                found_indicators['contradiction'].append(f"{neg}+{pos}")
    
    # Calculate overall sarcasm score
    total_score = sum(sarcasm_scores.values())
    sarcasm_probability = min(total_score * (0.5 + sensitivity), 1.0)
    
    # Classification
    if sarcasm_probability >= 0.7:
        classification = "🎭 Highly Sarcastic"
        confidence = "Very High"
    elif sarcasm_probability >= 0.5:
        classification = "😏 Likely Sarcastic"
        confidence = "High"
    elif sarcasm_probability >= 0.3:
        classification = "🤔 Possibly Sarcastic"
        confidence = "Medium"
    elif sarcasm_probability >= 0.1:
        classification = "😐 Slightly Sarcastic"
        confidence = "Low"
    else:
        classification = "✅ Sincere"
        confidence = "Very Low"
    
    return {
        'text': text,
        'sarcasm_probability': sarcasm_probability,
        'classification': classification,
        'confidence': confidence,
        'sarcasm_scores': sarcasm_scores,
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
    
    if st.button("🔍 Detect Sarcasm", type="primary"):
        if user_input.strip():
            with st.spinner("Analyzing..."):
                result = detect_sarcasm(user_input, sensitivity)
            
            st.success("✅ Analysis Complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Classification", result['classification'])
            with col2:
                st.metric("Probability", f"{result['sarcasm_probability']:.1%}")
            with col3:
                st.metric("Confidence", result['confidence'])
            
            # Gauge
            st.subheader("📊 Sarcasm Probability")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['sarcasm_probability'] * 100,
                title={'text': "Sarcasm Score (%)"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': 'purple' if result['sarcasm_probability'] >= 0.7 else 'blue' if result['sarcasm_probability'] >= 0.5 else 'lightblue'},
                       'steps': [
                           {'range': [0, 30], 'color': "lightgreen"},
                           {'range': [30, 50], 'color': "lightyellow"},
                           {'range': [50, 70], 'color': "lightblue"},
                           {'range': [70, 100], 'color': "lavender"}]}
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            if result['found_indicators']:
                st.subheader("🔍 Detected Indicators")
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
                    result = detect_sarcasm(str(text), sensitivity)
                    results.append({
                        'text': result['text'][:60] + '...',
                        'classification': result['classification'],
                        'probability': result['sarcasm_probability']
                    })
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Analyzed {len(results_df)} texts!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total", len(results_df))
                with col2:
                    sarcastic = len(results_df[results_df['probability'] >= 0.5])
                    st.metric("Sarcastic", sarcastic)
                with col3:
                    avg = results_df['probability'].mean()
                    st.metric("Avg Score", f"{avg:.1%}")
                
                fig = px.histogram(results_df, x='probability', nbins=20,
                                  title='Sarcasm Distribution')
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
        "Oh great, another meeting. Just what I needed today!",
        "Yeah right, because that's going to work perfectly...",
        "Wow, what a brilliant idea. Absolutely genius.",
        "I'm genuinely happy with this outcome. Thank you!",
        "Sure thing, I totally have time for that. Obviously."
    ]
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        for text in samples:
            result = detect_sarcasm(text, sensitivity)
            results.append({
                'text': text,
                'classification': result['classification'],
                'probability': result['sarcasm_probability']
            })
        
        results_df = pd.DataFrame(results)
        st.success("✅ Complete!")
        
        for idx, row in results_df.iterrows():
            st.info(f"{row['classification']} ({row['probability']:.1%}): {row['text']}")
        
        fig = px.bar(results_df, x=results_df.index, y='probability',
                     title='Sarcasm Scores',
                     color='probability', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Sarcasm Detection - Identify sarcastic and ironic language")
st.caption("💡 Useful for social media monitoring, review analysis, and sentiment analysis")
