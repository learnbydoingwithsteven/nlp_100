"""
NLP App 020: Review Authenticity
Real-world use case: Fake review detection
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Review Authenticity",
    page_icon="🔤",
    layout="wide"
)

st.title("⭐ Review Authenticity")
st.markdown("""
**Real-world Use Case**: Fake and spam review detection
- Detect fake/spam reviews
- Identify authentic customer feedback
- E-commerce trust scoring
- Review quality assessment
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
st.sidebar.markdown("---")
st.sidebar.markdown("**Authenticity Indicators:**")
st.sidebar.markdown("""
- 📝 Specific Details
- 💭 Personal Experience
- ⚖️ Balanced Opinion
- 🚩 Suspicious Patterns
- 🤖 Generic Language
""")

# Authenticity patterns
FAKE_INDICATORS = ['best product ever', 'highly recommend', 'must buy', 'amazing product', 'life changing', 'perfect', 'excellent quality']
SPAM_PATTERNS = ['click here', 'visit', 'check out', 'limited time', 'discount', 'promo', 'coupon']
AUTHENTIC_INDICATORS = ['however', 'but', 'although', 'wish', 'could be better', 'pros and cons', 'disappointed', 'satisfied']

def analyze_review_authenticity(text):
    """Analyze review authenticity"""
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words)
    
    # Scoring
    fake_score = 0
    authentic_score = 0
    found_indicators = {}
    
    # Check for overly positive/generic language
    fake_found = []
    for phrase in FAKE_INDICATORS:
        if phrase in text_lower:
            fake_score += 0.4
            fake_found.append(phrase)
    if fake_found:
        found_indicators['fake_indicators'] = fake_found
    
    # Check for spam patterns
    spam_found = []
    for pattern in SPAM_PATTERNS:
        if pattern in text_lower:
            fake_score += 0.5
            spam_found.append(pattern)
    if spam_found:
        found_indicators['spam_patterns'] = spam_found
    
    # Check for authentic indicators
    authentic_found = []
    for indicator in AUTHENTIC_INDICATORS:
        if indicator in text_lower:
            authentic_score += 0.3
            authentic_found.append(indicator)
    if authentic_found:
        found_indicators['authentic_indicators'] = authentic_found
    
    # Length check (very short = suspicious)
    if word_count < 10:
        fake_score += 0.3
    elif word_count > 30:
        authentic_score += 0.2
    
    # Specificity (numbers, dates, specific details)
    numbers = re.findall(r'\b\d+\b', text)
    if len(numbers) > 0:
        authentic_score += len(numbers) * 0.15
    
    # Personal pronouns (I, my, me = more authentic)
    personal = sum(1 for word in ['i ', 'my ', 'me ', 'mine '] if word in text_lower)
    authentic_score += personal * 0.2
    
    # ALL CAPS (spam indicator)
    caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    if caps_ratio > 0.3:
        fake_score += 0.4
    
    # Excessive punctuation
    if text.count('!') > 3:
        fake_score += 0.3
    
    # Calculate authenticity
    if fake_score > authentic_score:
        authenticity_score = max(0, 1 - (fake_score / max(fake_score + authentic_score, 0.1)))
    else:
        authenticity_score = min(1, authentic_score / max(fake_score + authentic_score, 0.1))
    
    # Classification
    if authenticity_score >= 0.7:
        classification = "✅ Likely Authentic"
        trust = "High"
    elif authenticity_score >= 0.5:
        classification = "🟡 Moderately Authentic"
        trust = "Medium"
    elif authenticity_score >= 0.3:
        classification = "⚠️ Questionable"
        trust = "Low"
    else:
        classification = "🚫 Likely Fake/Spam"
        trust = "Very Low"
    
    return {
        'text': text,
        'authenticity_score': authenticity_score,
        'classification': classification,
        'trust': trust,
        'fake_score': fake_score,
        'authentic_score': authentic_score,
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
    
    if st.button("🔍 Analyze Review", type="primary"):
        if user_input.strip():
            with st.spinner("Analyzing..."):
                result = analyze_review_authenticity(user_input)
            
            st.success("✅ Analysis Complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Classification", result['classification'])
            with col2:
                st.metric("Authenticity", f"{result['authenticity_score']:.1%}")
            with col3:
                st.metric("Trust Level", result['trust'])
            
            st.subheader("📊 Authenticity Score")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['authenticity_score'] * 100,
                title={'text': "Authenticity (%)"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': 'green' if result['authenticity_score'] >= 0.7 else 'yellow' if result['authenticity_score'] >= 0.5 else 'orange' if result['authenticity_score'] >= 0.3 else 'red'},
                       'steps': [
                           {'range': [0, 30], 'color': "lightcoral"},
                           {'range': [30, 50], 'color': "lightyellow"},
                           {'range': [50, 70], 'color': "lightblue"},
                           {'range': [70, 100], 'color': "lightgreen"}]}
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            if result['found_indicators']:
                st.subheader("🔍 Detected Indicators")
                for category, indicators in result['found_indicators'].items():
                    st.write(f"**{category.replace('_', ' ').title()}**: {', '.join(indicators)}")
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
                    result = analyze_review_authenticity(str(text))
                    results.append({
                        'text': result['text'][:60] + '...',
                        'classification': result['classification'],
                        'authenticity': result['authenticity_score'],
                        'trust': result['trust']
                    })
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Analyzed {len(results_df)} reviews!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total", len(results_df))
                with col2:
                    authentic = len(results_df[results_df['authenticity'] >= 0.7])
                    st.metric("Authentic", authentic)
                with col3:
                    fake = len(results_df[results_df['authenticity'] < 0.3])
                    st.metric("Likely Fake", fake)
                
                fig = px.histogram(results_df, x='authenticity', nbins=20,
                                  title='Authenticity Distribution')
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
        "I bought this product 3 weeks ago. It works well, however the battery could be better. Overall satisfied but wish it had more features.",
        "AMAZING PRODUCT!!! Best thing ever! Must buy! Perfect! Highly recommend to everyone! Life changing!",
        "Visit our website now for limited time discount! Click here for promo code! Check out this amazing deal!",
        "I've been using this for about 2 months. It has pros and cons. The quality is good but shipping took longer than expected. Would recommend with reservations."
    ]
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        for text in samples:
            result = analyze_review_authenticity(text)
            results.append({
                'text': text[:60] + '...',
                'classification': result['classification'],
                'authenticity': result['authenticity_score']
            })
        
        results_df = pd.DataFrame(results)
        st.success("✅ Complete!")
        
        for idx, row in results_df.iterrows():
            st.info(f"{row['classification']} ({row['authenticity']:.1%})")
            st.caption(row['text'])
        
        fig = px.bar(results_df, x=results_df.index, y='authenticity',
                     title='Authenticity Scores',
                     color='authenticity', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Review Authenticity - Detect fake and spam reviews")
st.caption("💡 Analyzes language patterns, specificity, and suspicious indicators to assess review authenticity")
