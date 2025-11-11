"""
NLP App 005: Toxicity Detection
Real-world use case: Harmful content identification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Toxicity Detection",
    page_icon="🔤",
    layout="wide"
)

st.title("⚠️ Toxicity Detection")
st.markdown("""
**Real-world Use Case**: Harmful content identification for social media and community platforms
- Detect toxic, threatening, obscene, and insulting content
- Multi-category toxicity analysis
- Severity scoring and risk assessment
- Content moderation support
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
sensitivity = st.sidebar.slider("Sensitivity Threshold", 0.0, 1.0, 0.5, 0.1)
st.sidebar.markdown("---")
st.sidebar.markdown("**Toxicity Categories:**")
st.sidebar.markdown("- 🔴 Toxic\n- 💀 Severe Toxic\n- 🤬 Obscene\n- ⚡ Threat\n- 😡 Insult\n- 👤 Identity Attack")

# Toxicity detection dictionaries
TOXIC_WORDS = {
    'severe': ['kill', 'death', 'die', 'murder', 'destroy'],
    'obscene': ['damn', 'hell', 'crap', 'suck'],
    'threat': ['will kill', 'gonna hurt', 'watch out', 'be sorry', 'regret'],
    'insult': ['idiot', 'stupid', 'dumb', 'moron', 'fool', 'loser', 'pathetic'],
    'identity': ['race', 'religion', 'gender', 'orientation']
}

def detect_toxicity(text):
    """Detect toxicity in text using rule-based approach"""
    text_lower = text.lower()
    word_count = len(text.split())
    
    # Initialize scores
    scores = {
        'toxic': 0.0,
        'severe_toxic': 0.0,
        'obscene': 0.0,
        'threat': 0.0,
        'insult': 0.0,
        'identity_attack': 0.0
    }
    
    detected_items = {k: [] for k in scores.keys()}
    
    # Check for severe toxic words
    for word in TOXIC_WORDS['severe']:
        if word in text_lower:
            scores['severe_toxic'] += 0.3
            scores['toxic'] += 0.2
            detected_items['severe_toxic'].append(word)
    
    # Check for obscene words
    for word in TOXIC_WORDS['obscene']:
        if word in text_lower:
            scores['obscene'] += 0.25
            scores['toxic'] += 0.15
            detected_items['obscene'].append(word)
    
    # Check for threats
    for phrase in TOXIC_WORDS['threat']:
        if phrase in text_lower:
            scores['threat'] += 0.4
            scores['toxic'] += 0.25
            detected_items['threat'].append(phrase)
    
    # Check for insults
    for word in TOXIC_WORDS['insult']:
        if word in text_lower:
            scores['insult'] += 0.2
            scores['toxic'] += 0.15
            detected_items['insult'].append(word)
    
    # Check for identity attacks
    for word in TOXIC_WORDS['identity']:
        if word in text_lower:
            scores['identity_attack'] += 0.15
            scores['toxic'] += 0.1
            detected_items['identity_attack'].append(word)
    
    # Pattern-based detection
    if re.search(r'[A-Z]{5,}', text):  # Excessive caps
        scores['toxic'] += 0.1
    
    if re.search(r'!{3,}', text):  # Excessive exclamation
        scores['toxic'] += 0.05
    
    # Normalize scores to 0-1 range
    for key in scores:
        scores[key] = min(scores[key], 1.0)
    
    # Overall toxicity
    overall_toxicity = max(scores.values())
    
    # Classification
    if overall_toxicity >= 0.7:
        classification = "Highly Toxic"
        risk_level = "🔴 HIGH RISK"
    elif overall_toxicity >= 0.4:
        classification = "Moderately Toxic"
        risk_level = "🟡 MEDIUM RISK"
    elif overall_toxicity >= 0.2:
        classification = "Mildly Toxic"
        risk_level = "🟠 LOW RISK"
    else:
        classification = "Non-Toxic"
        risk_level = "🟢 SAFE"
    
    return {
        'text': text,
        'overall_toxicity': overall_toxicity,
        'classification': classification,
        'risk_level': risk_level,
        'toxic': scores['toxic'],
        'severe_toxic': scores['severe_toxic'],
        'obscene': scores['obscene'],
        'threat': scores['threat'],
        'insult': scores['insult'],
        'identity_attack': scores['identity_attack'],
        'detected_items': detected_items,
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
    
    if st.button("🔍 Analyze Toxicity", type="primary"):
        if user_input.strip():
            with st.spinner("Analyzing..."):
                result = detect_toxicity(user_input)
            
            st.success("✅ Analysis Complete!")
            
            # Display main metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Overall Toxicity", f"{result['overall_toxicity']:.1%}")
            with col2:
                st.metric("Classification", result['classification'])
            with col3:
                st.metric("Risk Level", result['risk_level'])
            with col4:
                st.metric("Word Count", result['word_count'])
            
            # Toxicity breakdown
            st.subheader("📊 Toxicity Breakdown")
            
            categories = {
                'Toxic': result['toxic'],
                'Severe Toxic': result['severe_toxic'],
                'Obscene': result['obscene'],
                'Threat': result['threat'],
                'Insult': result['insult'],
                'Identity Attack': result['identity_attack']
            }
            
            # Bar chart
            fig = px.bar(
                x=list(categories.keys()),
                y=list(categories.values()),
                title="Toxicity Scores by Category",
                labels={'x': 'Category', 'y': 'Score'},
                color=list(categories.values()),
                color_continuous_scale='Reds'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed scores
            st.subheader("🔍 Detailed Scores")
            cols = st.columns(3)
            for idx, (cat, score) in enumerate(categories.items()):
                with cols[idx % 3]:
                    # Gauge chart
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=score,
                        title={'text': cat},
                        gauge={'axis': {'range': [0, 1]},
                               'bar': {'color': 'red' if score > sensitivity else 'green'},
                               'threshold': {
                                   'line': {'color': "orange", 'width': 4},
                                   'thickness': 0.75,
                                   'value': sensitivity}}
                    ))
                    fig_gauge.update_layout(height=200)
                    st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Show detected items
            st.subheader("🔎 Detected Items")
            any_detected = False
            for cat_name, items in result['detected_items'].items():
                if items:
                    any_detected = True
                    st.warning(f"**{cat_name.replace('_', ' ').title()}**: {', '.join(items)}")
            
            if not any_detected:
                st.info("✅ No toxic keywords detected")
            
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
                    result = detect_toxicity(str(text))
                    # Simplify for batch results
                    simple_result = {
                        'text': result['text'][:100] + '...' if len(result['text']) > 100 else result['text'],
                        'overall_toxicity': result['overall_toxicity'],
                        'classification': result['classification'],
                        'risk_level': result['risk_level'],
                        'toxic': result['toxic'],
                        'severe_toxic': result['severe_toxic'],
                        'obscene': result['obscene'],
                        'threat': result['threat'],
                        'insult': result['insult'],
                        'identity_attack': result['identity_attack']
                    }
                    results.append(simple_result)
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"Processed {len(results_df)} texts!")
                
                # Summary stats
                st.subheader("📊 Summary Statistics")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Analyzed", len(results_df))
                with col2:
                    high_risk = len(results_df[results_df['overall_toxicity'] >= 0.7])
                    st.metric("High Risk", high_risk, delta="🔴" if high_risk > 0 else "")
                with col3:
                    avg_toxicity = results_df['overall_toxicity'].mean()
                    st.metric("Avg Toxicity", f"{avg_toxicity:.1%}")
                with col4:
                    toxic_count = len(results_df[results_df['overall_toxicity'] >= 0.2])
                    st.metric("Toxic Items", toxic_count)
                
                # Visualization
                fig = px.histogram(results_df, x='overall_toxicity', title='Toxicity Distribution',
                                   labels={'overall_toxicity': 'Toxicity Score'},
                                   nbins=20, color_discrete_sequence=['#ff4b4b'])
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
    st.markdown("**Testing with varied examples from safe to toxic content**")
    
    sample_texts = [
        "I love this community! Everyone is so helpful and kind.",
        "This product is okay, nothing special but it works.",
        "Your idea is stupid and you're an idiot for thinking that.",
        "I will KILL you if you don't shut up!",
        "This movie was damn good, hell of a performance!",
        "People of all races and religions deserve respect and equality."
    ]
    
    # Display sample texts
    with st.expander("👁️ View Sample Texts"):
        for i, text in enumerate(sample_texts, 1):
            st.write(f"{i}. {text}")
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        with st.spinner("Analyzing sample texts..."):
            for text in sample_texts:
                result = detect_toxicity(text)
                # Simplify for demo display
                simple_result = {
                    'text': result['text'][:80] + '...' if len(result['text']) > 80 else result['text'],
                    'overall_toxicity': result['overall_toxicity'],
                    'classification': result['classification'],
                    'risk_level': result['risk_level'],
                    'toxic': result['toxic'],
                    'threat': result['threat'],
                    'insult': result['insult']
                }
                results.append(simple_result)
        
        results_df = pd.DataFrame(results)
        
        st.success("✅ Demo Complete!")
        
        # Summary
        st.subheader("📊 Demo Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Samples Analyzed", len(results_df))
        with col2:
            toxic = len(results_df[results_df['overall_toxicity'] >= 0.2])
            st.metric("Toxic Samples", toxic)
        with col3:
            safe = len(results_df[results_df['overall_toxicity'] < 0.2])
            st.metric("Safe Samples", safe)
        
        # Display results
        st.subheader("📋 Detailed Results")
        for idx, row in results_df.iterrows():
            with st.expander(f"Sample {idx+1}: {row['classification']}"):
                st.write(f"**Text**: {row['text']}")
                st.write(f"**Risk**: {row['risk_level']}")
                cols = st.columns(3)
                with cols[0]:
                    st.metric("Overall", f"{row['overall_toxicity']:.1%}")
                with cols[1]:
                    st.metric("Toxic", f"{row['toxic']:.1%}")
                with cols[2]:
                    st.metric("Threat", f"{row['threat']:.1%}")
        
        # Visualization
        fig = px.bar(results_df, y='overall_toxicity', x=results_df.index,
                     title='Toxicity Levels Across Samples',
                     labels={'y': 'Toxicity Score', 'x': 'Sample #'},
                     color='overall_toxicity', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Toxicity Detection - Multi-category content moderation for online platforms")
st.caption("⚠️ Note: This is a rule-based demonstration. Production systems should use ML models like Detoxify or Perspective API.")
