"""
NLP App 009: Fake News Detection
Real-world use case: News article credibility analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Fake News Detection",
    page_icon="🔤",
    layout="wide"
)

st.title("📰 Fake News Detection")
st.markdown("""
**Real-world Use Case**: News article credibility analysis for fact-checking
- Analyze news articles for credibility indicators
- Detect sensationalism and clickbait patterns
- Source reliability assessment
- Content quality scoring
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
sensitivity = st.sidebar.slider("Detection Sensitivity", 0.0, 1.0, 0.5, 0.1)
st.sidebar.markdown("---")
st.sidebar.markdown("**Credibility Indicators:**")
st.sidebar.markdown("""
- ✅ Reliable Sources
- 📅 Date & Facts
- 🔍 Verification
- ⚠️ Sensationalism
- 👥 Author Info
""")

# Credibility indicators
FAKE_INDICATORS = {
    'sensationalism': ['shocking', 'unbelievable', 'you won\'t believe', 'amazing', 'incredible', 'mind-blowing', 'jaw-dropping', 'viral', 'breaking'],
    'emotion': ['outrage', 'furious', 'devastating', 'horrifying', 'terrifying', 'scandal'],
    'urgency': ['now', 'immediately', 'urgent', 'breaking', 'just in', 'alert'],
    'absolute': ['always', 'never', 'everyone', 'nobody', 'completely', 'totally', 'all'],
    'unreliable': ['sources say', 'rumor', 'allegedly', 'reportedly', 'claims', 'unconfirmed']
}

CREDIBLE_INDICATORS = {
    'sources': ['according to', 'study shows', 'research', 'official', 'reported by', 'statement', 'confirmed'],
    'facts': ['data', 'statistics', 'percent', 'number', 'figure', 'analysis'],
    'attribution': ['said', 'stated', 'announced', 'revealed', 'disclosed'],
    'verification': ['verified', 'fact-checked', 'confirmed', 'authenticated', 'validated']
}

def detect_fake_news(text):
    """Analyze text for fake news indicators"""
    text_lower = text.lower()
    word_count = len(text.split())
    
    # Calculate fake indicators
    fake_score = 0.0
    fake_found = {}
    
    for category, keywords in FAKE_INDICATORS.items():
        found = []
        for keyword in keywords:
            if keyword in text_lower:
                count = text_lower.count(keyword)
                fake_score += count * 0.15
                found.append(keyword)
        fake_found[category] = found
    
    # Calculate credibility indicators
    credible_score = 0.0
    credible_found = {}
    
    for category, keywords in CREDIBLE_INDICATORS.items():
        found = []
        for keyword in keywords:
            if keyword in text_lower:
                count = text_lower.count(keyword)
                credible_score += count * 0.2
                found.append(keyword)
        credible_found[category] = found
    
    # Pattern checks
    if re.search(r'[A-Z]{10,}', text):  # Excessive caps
        fake_score += 0.3
    
    if re.search(r'!{3,}', text):  # Multiple exclamation marks
        fake_score += 0.2
    
    if re.search(r'\?{2,}', text):  # Multiple question marks
        fake_score += 0.1
    
    # Normalize scores
    fake_score = min(fake_score, 1.0)
    credible_score = min(credible_score, 1.0)
    
    # Calculate overall credibility (0 = fake, 1 = credible)
    if credible_score > 0 or fake_score > 0:
        credibility = credible_score / (credible_score + fake_score) if (credible_score + fake_score) > 0 else 0.5
    else:
        credibility = 0.5  # Neutral
    
    # Classification
    if credibility >= 0.7:
        classification = "Likely Credible"
        risk = "🟢 Low Risk"
    elif credibility >= 0.5:
        classification = "Mixed Signals"
        risk = "🟡 Medium Risk"
    elif credibility >= 0.3:
        classification = "Questionable"
        risk = "🟠 High Risk"
    else:
        classification = "Likely Fake"
        risk = "🔴 Very High Risk"
    
    return {
        'text': text,
        'credibility': credibility,
        'classification': classification,
        'risk_level': risk,
        'fake_score': fake_score,
        'credible_score': credible_score,
        'fake_indicators': fake_found,
        'credible_indicators': credible_found,
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
    
    if st.button("🔍 Analyze Credibility", type="primary"):
        if user_input.strip():
            with st.spinner("Analyzing..."):
                result = detect_fake_news(user_input)
            
            st.success("✅ Analysis Complete!")
            
            # Main metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Credibility Score", f"{result['credibility']:.1%}")
            with col2:
                st.metric("Classification", result['classification'])
            with col3:
                st.metric("Risk Level", result['risk_level'])
            with col4:
                st.metric("Word Count", result['word_count'])
            
            # Credibility gauge
            st.subheader("📊 Credibility Score")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['credibility'] * 100,
                title={'text': "Credibility (%)"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': 'green' if result['credibility'] >= 0.7 else 'orange' if result['credibility'] >= 0.5 else 'red'},
                       'steps': [
                           {'range': [0, 30], 'color': "lightcoral"},
                           {'range': [30, 50], 'color': "lightyellow"},
                           {'range': [50, 70], 'color': "lightblue"},
                           {'range': [70, 100], 'color': "lightgreen"}]}
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            # Score comparison
            st.subheader("⚖️ Score Breakdown")
            scores_data = pd.DataFrame({
                'Indicator': ['Fake Signs', 'Credible Signs'],
                'Score': [result['fake_score'], result['credible_score']]
            })
            fig = px.bar(scores_data, x='Indicator', y='Score',
                        title="Fake vs Credible Indicators",
                        color='Score', color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)
            
            # Detected indicators
            st.subheader("🔍 Detected Indicators")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**⚠️ Fake Indicators:**")
                any_fake = False
                for category, items in result['fake_indicators'].items():
                    if items:
                        any_fake = True
                        st.warning(f"**{category.title()}**: {', '.join(set(items))}")
                if not any_fake:
                    st.info("None detected")
            
            with col2:
                st.markdown("**✅ Credible Indicators:**")
                any_credible = False
                for category, items in result['credible_indicators'].items():
                    if items:
                        any_credible = True
                        st.success(f"**{category.title()}**: {', '.join(set(items))}")
                if not any_credible:
                    st.info("None detected")
        else:
            st.warning("Please enter some text to analyze.")

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
                    result = detect_fake_news(str(text))
                    simple_result = {
                        'text': result['text'][:60] + '...' if len(result['text']) > 60 else result['text'],
                        'credibility': result['credibility'],
                        'classification': result['classification'],
                        'risk_level': result['risk_level']
                    }
                    results.append(simple_result)
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Analyzed {len(results_df)} articles!")
                
                # Summary stats
                st.subheader("📊 Summary Statistics")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Analyzed", len(results_df))
                with col2:
                    likely_fake = len(results_df[results_df['credibility'] < 0.3])
                    st.metric("Likely Fake", likely_fake)
                with col3:
                    likely_credible = len(results_df[results_df['credibility'] >= 0.7])
                    st.metric("Likely Credible", likely_credible)
                with col4:
                    avg_cred = results_df['credibility'].mean()
                    st.metric("Avg Credibility", f"{avg_cred:.1%}")
                
                # Visualization
                fig = px.histogram(results_df, x='credibility', nbins=20,
                                  title='Credibility Score Distribution',
                                  labels={'credibility': 'Credibility Score'})
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
    st.markdown("**Testing with different types of news content**")
    
    sample_texts = [
        "According to a study published in Nature, researchers have confirmed that regular exercise improves cognitive function. The data shows significant improvements in memory and attention.",
        "SHOCKING!!! You won't believe what this celebrity did!!! This is absolutely mind-blowing and everyone is talking about it!!! VIRAL!!!",
        "The government announced today that new policies will be implemented next quarter. Officials stated that the changes aim to improve efficiency.",
        "Sources say that something terrible might happen soon. Allegedly, rumors are spreading about unconfirmed reports. Claims suggest something shocking.",
        "Scientists revealed new findings today based on verified research. The official statement confirmed the results were fact-checked and authenticated."
    ]
    
    with st.expander("👁️ View Sample Articles"):
        for i, text in enumerate(sample_texts, 1):
            st.write(f"{i}. {text}")
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        with st.spinner("Analyzing credibility..."):
            for text in sample_texts:
                result = detect_fake_news(text)
                results.append({
                    'text': text[:60] + '...',
                    'credibility': result['credibility'],
                    'classification': result['classification']
                })
        
        results_df = pd.DataFrame(results)
        st.success("✅ Demo Complete!")
        
        # Summary
        st.subheader("📊 Demo Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Articles", len(results_df))
        with col2:
            credible = len(results_df[results_df['credibility'] >= 0.7])
            st.metric("Credible", credible)
        with col3:
            fake = len(results_df[results_df['credibility'] < 0.3])
            st.metric("Likely Fake", fake)
        
        # Results
        st.subheader("📋 Analysis Results")
        for idx, row in results_df.iterrows():
            emoji = "🟢" if row['credibility'] >= 0.7 else "🟡" if row['credibility'] >= 0.5 else "🔴"
            with st.expander(f"{emoji} Article {idx+1}: {row['classification']}"):
                st.write(f"**Text**: {row['text']}")
                st.metric("Credibility", f"{row['credibility']:.1%}")
        
        # Visualization
        fig = px.bar(results_df, x=results_df.index, y='credibility',
                     title='Credibility Scores by Article',
                     labels={'x': 'Article #', 'credibility': 'Credibility'},
                     color='credibility', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Fake News Detection - News article credibility analysis using linguistic patterns")
st.caption("💡 Tip: This is a demonstration tool. Real fact-checking requires human verification and source investigation")
