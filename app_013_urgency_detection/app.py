"""
NLP App 013: Urgency Detection
Real-world use case: Email priority classification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from datetime import datetime

st.set_page_config(
    page_title="Urgency Detection",
    page_icon="🔤",
    layout="wide"
)

st.title("⏰ Urgency Detection")
st.markdown("""
**Real-world Use Case**: Message and email priority classification
- Detect urgent messages automatically
- Priority level assessment
- Time-sensitive keyword detection
- Action item identification
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
sensitivity = st.sidebar.slider("Urgency Sensitivity", 0.0, 1.0, 0.5, 0.1)
st.sidebar.markdown("---")
st.sidebar.markdown("**Urgency Indicators:**")
st.sidebar.markdown("""
- 🔥 Critical Keywords
- ⏱️ Time Constraints
- ❗ Action Words
- 📅 Deadlines
- 🚨 Priority Markers
""")

# Urgency indicators
URGENCY_INDICATORS = {
    'critical': ['urgent', 'asap', 'emergency', 'critical', 'immediate', 'now', 'important', 'priority', 'crucial'],
    'time_sensitive': ['today', 'tonight', 'deadline', 'due', 'expires', 'tomorrow', 'this week', 'end of day', 'eod', 'by', 'before'],
    'action_required': ['please', 'must', 'need', 'required', 'action', 'respond', 'reply', 'confirm', 'approve', 'complete', 'finish'],
    'escalation': ['escalate', 'alert', 'attention', 'warning', 'notice', 'remind', 'follow up'],
    'punctuation': ['!!!', '!!', '!']
}

def detect_urgency(text, sensitivity=0.5):
    """Detect urgency level in text"""
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words)
    
    # Score different urgency aspects
    urgency_scores = {}
    found_indicators = {}
    
    for category, keywords in URGENCY_INDICATORS.items():
        score = 0
        found = []
        for keyword in keywords:
            if keyword in text_lower:
                count = text_lower.count(keyword)
                score += count * 0.2
                found.extend([keyword] * count)
        urgency_scores[category] = score
        if found:
            found_indicators[category] = found
    
    # Check for all caps (indicates emphasis/urgency)
    caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    if caps_ratio > 0.3:
        urgency_scores['emphasis'] = 0.5
        found_indicators['emphasis'] = ['CAPS EMPHASIS']
    
    # Check for time patterns (dates, times)
    time_patterns = re.findall(r'\d{1,2}[:/]\d{1,2}|\d{1,2}(am|pm|AM|PM)', text)
    if time_patterns:
        urgency_scores['time_constraint'] = len(time_patterns) * 0.3
        found_indicators['time_constraint'] = time_patterns
    
    # Check for exclamation marks
    exclamation_count = text.count('!')
    if exclamation_count > 0:
        urgency_scores['exclamation'] = min(exclamation_count * 0.15, 0.6)
    
    # Calculate overall urgency score
    total_score = sum(urgency_scores.values())
    
    # Adjust by sensitivity
    urgency_score = min(total_score * (0.5 + sensitivity), 1.0)
    
    # Priority classification
    if urgency_score >= 0.7:
        priority = "🔴 Critical"
        level = "Urgent"
        action = "Immediate action required"
    elif urgency_score >= 0.5:
        priority = "🟠 High"
        level = "High Priority"
        action = "Respond soon"
    elif urgency_score >= 0.3:
        priority = "🟡 Medium"
        level = "Moderate"
        action = "Handle within timeframe"
    elif urgency_score >= 0.1:
        priority = "🟢 Low"
        level = "Standard"
        action = "Normal processing"
    else:
        priority = "⚪ None"
        level = "Informational"
        action = "No urgent action"
    
    return {
        'text': text,
        'urgency_score': urgency_score,
        'priority': priority,
        'level': level,
        'action': action,
        'urgency_scores': urgency_scores,
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
    
    if st.button("🔍 Detect Urgency", type="primary"):
        if user_input.strip():
            with st.spinner("Analyzing..."):
                result = detect_urgency(user_input, sensitivity)
            
            st.success("✅ Analysis Complete!")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Priority", result['priority'])
            with col2:
                st.metric("Level", result['level'])
            with col3:
                st.metric("Urgency Score", f"{result['urgency_score']:.1%}")
            with col4:
                st.metric("Words", result['word_count'])
            
            st.info(f"**Recommended Action**: {result['action']}")
            
            # Urgency gauge
            st.subheader("📊 Urgency Score")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['urgency_score'] * 100,
                title={'text': "Urgency Level (%)"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': 'red' if result['urgency_score'] >= 0.7 else 'orange' if result['urgency_score'] >= 0.5 else 'yellow' if result['urgency_score'] >= 0.3 else 'green'},
                       'steps': [
                           {'range': [0, 10], 'color': "lightgreen"},
                           {'range': [10, 30], 'color': "lightyellow"},
                           {'range': [30, 50], 'color': "lightgoldenrodyellow"},
                           {'range': [50, 70], 'color': "lightsalmon"},
                           {'range': [70, 100], 'color': "lightcoral"}]}
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            # Found indicators
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
                    result = detect_urgency(str(text), sensitivity)
                    simple_result = {
                        'text': result['text'][:60] + '...',
                        'priority': result['priority'],
                        'urgency_score': result['urgency_score'],
                        'level': result['level']
                    }
                    results.append(simple_result)
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Analyzed {len(results_df)} messages!")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total", len(results_df))
                with col2:
                    critical = len(results_df[results_df['urgency_score'] >= 0.7])
                    st.metric("Critical", critical)
                with col3:
                    avg_urgency = results_df['urgency_score'].mean()
                    st.metric("Avg Urgency", f"{avg_urgency:.1%}")
                with col4:
                    low = len(results_df[results_df['urgency_score'] < 0.3])
                    st.metric("Low Priority", low)
                
                fig = px.histogram(results_df, x='urgency_score', nbins=20,
                                  title='Urgency Distribution',
                                  labels={'urgency_score': 'Urgency Score'})
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
    st.markdown("**Testing with messages of varying urgency levels**")
    
    sample_texts = [
        "URGENT!!! System failure - immediate action required ASAP! Critical issue needs to be resolved by 5pm today!",
        "Please respond by end of day tomorrow. This is important and requires your attention soon.",
        "FYI - The meeting scheduled for next week has been moved to the conference room.",
        "Can you please review this document when you have time? No rush, just let me know your thoughts.",
        "Emergency! Server down. Need immediate assistance. Production system offline!!!"
    ]
    
    with st.expander("👁️ View Sample Messages"):
        for i, text in enumerate(sample_texts, 1):
            st.write(f"{i}. {text}")
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        with st.spinner("Analyzing urgency..."):
            for text in sample_texts:
                result = detect_urgency(text, sensitivity)
                results.append({
                    'text': text[:50] + '...',
                    'priority': result['priority'],
                    'score': result['urgency_score'],
                    'level': result['level']
                })
        
        results_df = pd.DataFrame(results)
        st.success("✅ Demo Complete!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Messages", len(results_df))
        with col2:
            critical = len(results_df[results_df['score'] >= 0.7])
            st.metric("Critical", critical)
        with col3:
            avg = results_df['score'].mean()
            st.metric("Avg Urgency", f"{avg:.1%}")
        
        st.subheader("📋 Results")
        for idx, row in results_df.iterrows():
            with st.expander(f"{row['priority']} - Message {idx+1}"):
                st.write(f"**Text**: {row['text']}")
                st.metric("Urgency Score", f"{row['score']:.1%}")
                st.write(f"**Level**: {row['level']}")
        
        fig = px.bar(results_df, x=results_df.index, y='score',
                     title='Urgency Scores by Message',
                     labels={'x': 'Message #', 'score': 'Urgency Score'},
                     color='score', color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Urgency Detection - Automatic email and message priority classification")
st.caption("💡 Tip: Use this to prioritize inbox messages, route customer support tickets, or triage emails")
