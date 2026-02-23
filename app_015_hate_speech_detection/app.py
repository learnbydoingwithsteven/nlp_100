"""
NLP App 015: Hate Speech Detection
Real-world use case: Offensive content filtering
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Hate Speech Detection",
    page_icon="🔤",
    layout="wide"
)

st.title("⚠️ Hate Speech Detection")
st.markdown("""
**Real-world Use Case**: Content moderation and offensive language detection
- Detect hate speech and offensive content
- Identify targeted harassment
- Content safety scoring
- Social media moderation
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
strict_mode = st.sidebar.checkbox("Strict Mode", value=False)
st.sidebar.markdown("---")
st.sidebar.markdown("**Detection Categories:**")
st.sidebar.markdown("""
- 🚫 Offensive Language
- 🎯 Targeted Hate
- ⚠️ Harassment
- 🚨 Threats
- 🔥 Inflammatory
""")

# Hate speech indicators (generalized for content moderation)
HATE_INDICATORS = {
    'offensive': ['stupid', 'idiot', 'moron', 'dumb', 'pathetic', 'loser', 'trash', 'garbage'],
    'aggressive': ['hate', 'destroy', 'die', 'kill', 'attack', 'fight', 'beat'],
    'threats': ['threat', 'hurt', 'harm', 'violence', 'dangerous', 'watch out', 'get you'],
    'harassment': ['shut up', 'go away', 'nobody wants', 'nobody likes', 'worthless', 'useless'],
    'inflammatory': ['disgusting', 'horrible', 'terrible', 'awful', 'worst', 'scum'],
    'derogatory': ['inferior', 'subhuman', 'animals', 'vermin', 'plague']
}

def detect_hate_speech(text, strict_mode=False):
    """Detect hate speech and offensive content"""
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words)
    
    # Category scoring
    category_scores = {}
    found_terms = {}
    
    for category, keywords in HATE_INDICATORS.items():
        score = 0
        found = []
        for keyword in keywords:
            if keyword in text_lower:
                count = text_lower.count(keyword)
                score += count * 0.3
                found.extend([keyword] * count)
        if score > 0:
            category_scores[category] = score
            found_terms[category] = found
    
    # Check for ALL CAPS (aggressive tone)
    caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    if caps_ratio > 0.4:
        category_scores['caps_aggression'] = 0.4
        found_terms['caps_aggression'] = ['EXCESSIVE CAPS']
    
    # Check for excessive punctuation (!!! or ???)
    if text.count('!') > 2 or text.count('?') > 2:
        category_scores['aggressive_punctuation'] = 0.2
    
    # Profanity patterns (asterisks or symbols)
    if re.search(r'\*+|\$+|@+|#+', text):
        category_scores['censored_profanity'] = 0.3
        found_terms['censored_profanity'] = ['Censored terms detected']
    
    # Direct attack patterns ("you are X")
    attack_patterns = ['you are', "you're", 'u r', 'ur']
    for pattern in attack_patterns:
        if pattern in text_lower:
            for offensive in HATE_INDICATORS['offensive']:
                if offensive in text_lower:
                    category_scores['direct_attack'] = category_scores.get('direct_attack', 0) + 0.4
                    if 'direct_attack' not in found_terms:
                        found_terms['direct_attack'] = []
                    found_terms['direct_attack'].append(f"{pattern} + {offensive}")
    
    # Calculate overall hate score
    total_score = sum(category_scores.values())
    
    # Adjust for strict mode
    if strict_mode:
        hate_probability = min(total_score * 1.2, 1.0)
    else:
        hate_probability = min(total_score * 0.8, 1.0)
    
    # Classification
    if hate_probability >= 0.8:
        classification = "🚨 Severe"
        risk = "Critical"
        action = "Block/Remove immediately"
    elif hate_probability >= 0.6:
        classification = "🔴 High Risk"
        risk = "High"
        action = "Flag for review"
    elif hate_probability >= 0.4:
        classification = "🟠 Moderate"
        risk = "Medium"
        action = "Monitor closely"
    elif hate_probability >= 0.2:
        classification = "🟡 Low Risk"
        risk = "Low"
        action = "Log for analysis"
    else:
        classification = "✅ Safe"
        risk = "Minimal"
        action = "No action needed"
    
    return {
        'text': text,
        'hate_probability': hate_probability,
        'classification': classification,
        'risk': risk,
        'action': action,
        'category_scores': category_scores,
        'found_terms': found_terms,
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
    
    if st.button("🔍 Analyze Content", type="primary"):
        if user_input.strip():
            with st.spinner("Analyzing..."):
                result = detect_hate_speech(user_input, strict_mode)
            
            st.success("✅ Analysis Complete!")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Classification", result['classification'])
            with col2:
                st.metric("Risk Level", result['risk'])
            with col3:
                st.metric("Hate Score", f"{result['hate_probability']:.1%}")
            with col4:
                st.metric("Words", result['word_count'])
            
            st.warning(f"**Recommended Action**: {result['action']}")
            
            # Risk gauge
            st.subheader("📊 Risk Assessment")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['hate_probability'] * 100,
                title={'text': "Content Risk (%)"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': 'darkred' if result['hate_probability'] >= 0.8 else 'red' if result['hate_probability'] >= 0.6 else 'orange' if result['hate_probability'] >= 0.4 else 'yellow' if result['hate_probability'] >= 0.2 else 'green'},
                       'steps': [
                           {'range': [0, 20], 'color': "lightgreen"},
                           {'range': [20, 40], 'color': "lightyellow"},
                           {'range': [40, 60], 'color': "lightcoral"},
                           {'range': [60, 80], 'color': "indianred"},
                           {'range': [80, 100], 'color': "darkred"}]}
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            if result['found_terms']:
                st.subheader("🔍 Detected Issues")
                for category, terms in result['found_terms'].items():
                    st.write(f"**{category.replace('_', ' ').title()}**: {', '.join(map(str, set(terms)))}")
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
                    result = detect_hate_speech(str(text), strict_mode)
                    results.append({
                        'text': result['text'][:60] + '...',
                        'classification': result['classification'],
                        'risk': result['risk'],
                        'score': result['hate_probability']
                    })
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Analyzed {len(results_df)} texts!")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total", len(results_df))
                with col2:
                    severe = len(results_df[results_df['score'] >= 0.6])
                    st.metric("High Risk", severe)
                with col3:
                    safe = len(results_df[results_df['score'] < 0.2])
                    st.metric("Safe", safe)
                with col4:
                    avg = results_df['score'].mean()
                    st.metric("Avg Risk", f"{avg:.1%}")
                
                fig = px.histogram(results_df, x='score', nbins=20,
                                  title='Risk Distribution')
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
        "I disagree with this policy but respect your opinion.",
        "You are such an idiot! Nobody likes you!",
        "This is a thoughtful discussion about important topics.",
        "SHUT UP! You're terrible and worthless!",
        "Great work on the project. Keep it up!"
    ]
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        for text in samples:
            result = detect_hate_speech(text, strict_mode)
            results.append({
                'text': text[:50] + '...',
                'classification': result['classification'],
                'risk': result['risk'],
                'score': result['hate_probability']
            })
        
        results_df = pd.DataFrame(results)
        st.success("✅ Complete!")
        
        for idx, row in results_df.iterrows():
            st.info(f"{row['classification']} - Risk: {row['risk']} ({row['score']:.1%})")
            st.caption(row['text'])
        
        fig = px.bar(results_df, x=results_df.index, y='score',
                     title='Risk Scores',
                     color='score', color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Hate Speech Detection - Content moderation and offensive language detection")
st.caption("💡 Use for social media moderation, comment filtering, and community safety")
