"""
NLP App 002: Spam Detection
Real-world use case: Email/SMS spam filtering
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Spam Detection",
    page_icon="🚫",
    layout="wide"
)

st.title("🚫 Spam Detection")
st.markdown("""
**Real-world Use Case**: Email/SMS spam filtering
- Identify spam messages using pattern and keyword analysis
- Calculate spam probability scores
- Visualize detection results and confidence levels
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
sensitivity = st.sidebar.slider("Detection Sensitivity", 0.1, 1.0, 0.4, 0.1, 
                                 help="Lower = more strict, Higher = more lenient")

def detect_spam(text, threshold=0.4):
    """Detect spam using keyword and pattern analysis"""
    spam_keywords = ['winner', 'free', 'prize', 'click here', 'urgent', 'cash', 'loan', 
                     'credit', 'congratulations', 'offer', 'discount', 'limited time', 
                     'act now', '$$$', 'buy now', 'call now', 'subscribe', 'unsubscribe',
                     'guarantee', 'risk free', 'viagra', 'pharmacy']
    
    text_lower = text.lower()
    spam_score = 0
    found_keywords = []
    
    # Check spam keywords
    for keyword in spam_keywords:
        if keyword in text_lower:
            spam_score += 1
            found_keywords.append(keyword)
    
    # Pattern checks
    patterns_found = []
    if re.search(r'\d{3,}', text):  # Multiple digits
        spam_score += 0.5
        patterns_found.append("Multiple digits")
    
    if len([c for c in text if c.isupper()]) / max(len(text), 1) > 0.5:  # Excessive caps
        spam_score += 1
        patterns_found.append("Excessive CAPS")
    
    if text.count('!') > 2:  # Multiple exclamations
        spam_score += 0.5
        patterns_found.append("Multiple exclamations")
    
    if re.search(r'\$\d+', text):  # Dollar amounts
        spam_score += 0.5
        patterns_found.append("Dollar amounts")
    
    if len(re.findall(r'http[s]?://', text)) > 1:  # Multiple URLs
        spam_score += 0.5
        patterns_found.append("Multiple URLs")
    
    # Calculate spam probability
    spam_probability = min(spam_score / 5.0, 1.0)
    is_spam = spam_probability > threshold
    
    return {
        'text': text,
        'is_spam': is_spam,
        'classification': 'SPAM ❌' if is_spam else 'HAM ✅',
        'spam_probability': spam_probability,
        'ham_probability': 1 - spam_probability,
        'spam_score': spam_score,
        'found_keywords': found_keywords,
        'keyword_count': len(found_keywords),
        'patterns_found': patterns_found,
        'pattern_count': len(patterns_found),
        'confidence': max(spam_probability, 1 - spam_probability),
        'word_count': len(text.split()),
        'text_length': len(text)
    }

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Message Analysis")
    
    user_input = st.text_area(
        "Enter message to analyze:",
        height=150,
        placeholder="Paste an email or SMS message here..."
    )
    
    if st.button("🔍 Detect Spam", type="primary"):
        if user_input.strip():
            with st.spinner("Analyzing message..."):
                result = detect_spam(user_input, sensitivity)
            
            # Display classification
            if result['is_spam']:
                st.error(f"🚫 **{result['classification']}**")
            else:
                st.success(f"✅ **{result['classification']}**")
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Spam Probability", f"{result['spam_probability']:.1%}")
            with col2:
                st.metric("Confidence", f"{result['confidence']:.1%}")
            with col3:
                st.metric("Keywords Found", result['keyword_count'])
            with col4:
                st.metric("Patterns Found", result['pattern_count'])
            
            # Detailed Analysis
            st.subheader("📊 Detailed Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Probability gauge
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=result['spam_probability'] * 100,
                    title={'text': "Spam Probability (%)"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "darkred"},
                        'steps': [
                            {'range': [0, 40], 'color': "lightgreen"},
                            {'range': [40, 70], 'color': "lightyellow"},
                            {'range': [70, 100], 'color': "lightcoral"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': sensitivity * 100
                        }
                    }
                ))
                st.plotly_chart(fig_gauge, use_container_width=True)
                
                # Score breakdown
                fig_scores = px.bar(
                    x=['Spam', 'Ham'],
                    y=[result['spam_probability'], result['ham_probability']],
                    title='Classification Scores',
                    color=['Spam', 'Ham'],
                    color_discrete_map={'Spam': 'red', 'Ham': 'green'},
                    labels={'x': 'Classification', 'y': 'Probability'}
                )
                st.plotly_chart(fig_scores, use_container_width=True)
            
            with col2:
                # Keywords found
                st.markdown("**🔍 Spam Keywords Found:**")
                if result['found_keywords']:
                    for keyword in result['found_keywords']:
                        st.markdown(f"- `{keyword}`")
                else:
                    st.info("No spam keywords detected")
                
                # Patterns found
                st.markdown("**🔎 Spam Patterns Found:**")
                if result['patterns_found']:
                    for pattern in result['patterns_found']:
                        st.markdown(f"- `{pattern}`")
                else:
                    st.info("No spam patterns detected")
                
                # Text statistics
                st.markdown("**📝 Text Statistics:**")
                st.write(f"- Word count: {result['word_count']}")
                st.write(f"- Character count: {result['text_length']}")
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
                    result = detect_spam(str(text), sensitivity)
                    results.append(result)
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Analyzed {len(results_df)} messages!")
                
                # Summary stats
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Messages", len(results_df))
                with col2:
                    spam_count = (results_df['is_spam']).sum()
                    st.metric("Spam Detected", spam_count)
                with col3:
                    ham_count = (~results_df['is_spam']).sum()
                    st.metric("Legitimate (Ham)", ham_count)
                with col4:
                    spam_rate = (spam_count / len(results_df) * 100) if len(results_df) > 0 else 0
                    st.metric("Spam Rate", f"{spam_rate:.1f}%")
                
                # Classification distribution
                st.subheader("📊 Classification Distribution")
                fig_dist = px.pie(
                    names=['Spam', 'Ham'],
                    values=[spam_count, ham_count],
                    title='Spam vs Ham Distribution',
                    color=['Spam', 'Ham'],
                    color_discrete_map={'Spam': 'red', 'Ham': 'green'}
                )
                st.plotly_chart(fig_dist, use_container_width=True)
                
                # Probability distribution
                fig_hist = px.histogram(
                    results_df,
                    x='spam_probability',
                    title='Spam Probability Distribution',
                    nbins=20,
                    labels={'spam_probability': 'Spam Probability'}
                )
                st.plotly_chart(fig_hist, use_container_width=True)
                
                # Results table
                st.subheader("📋 Detailed Results")
                display_df = results_df[['text', 'classification', 'spam_probability', 
                                         'keyword_count', 'pattern_count']].copy()
                st.dataframe(display_df, use_container_width=True)
                
                # Download
                csv = results_df.to_csv(index=False)
                st.download_button("📥 Download Results", csv, "spam_detection_results.csv", "text/csv")
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file to perform batch processing")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    
    sample_texts = [
        "CONGRATULATIONS! You've WON $1,000,000! Click here NOW to claim your prize!!!",
        "Hi, can we schedule a meeting tomorrow at 3pm to discuss the project progress?",
        "FREE OFFER! Limited time only! Act now and get 90% OFF! Click here!!! Risk free!!!",
        "Your Amazon order #123-456-7890 has been shipped and will arrive tomorrow.",
        "URGENT: Your account will be closed. Send your password immediately to verify!",
        "Thanks for the great presentation yesterday. The team really appreciated your insights.",
        "BUY NOW!!! Best price guaranteed!!! Call 555-1234 for exclusive offer!!!"
    ]
    
    st.write(f"Analyzing {len(sample_texts)} sample messages...")
    
    # Display sample texts
    with st.expander("👁️ View Sample Messages"):
        for i, text in enumerate(sample_texts, 1):
            st.write(f"{i}. {text}")
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        with st.spinner("Analyzing messages..."):
            for text in sample_texts:
                result = detect_spam(text, sensitivity)
                results.append(result)
        
        results_df = pd.DataFrame(results)
        
        st.success("✅ Demo Complete!")
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            spam_count = (results_df['is_spam']).sum()
            st.metric("Spam Detected", spam_count, 
                     delta=f"{spam_count/len(results_df)*100:.0f}%")
        with col2:
            ham_count = (~results_df['is_spam']).sum()
            st.metric("Legitimate (Ham)", ham_count,
                     delta=f"{ham_count/len(results_df)*100:.0f}%")
        with col3:
            avg_confidence = results_df['confidence'].mean()
            st.metric("Avg Confidence", f"{avg_confidence:.1%}")
        
        # Display results
        st.subheader("📋 Classification Results")
        for idx, row in results_df.iterrows():
            emoji = "🚫" if row['is_spam'] else "✅"
            color = "red" if row['is_spam'] else "green"
            
            with st.expander(f"{emoji} Message {idx+1} - {row['classification']}"):
                st.write(f"**Text**: {row['text']}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Spam Probability", f"{row['spam_probability']:.1%}")
                with col2:
                    st.metric("Keywords Found", row['keyword_count'])
                with col3:
                    st.metric("Patterns Found", row['pattern_count'])
                
                if row['found_keywords']:
                    st.write(f"**Keywords**: {', '.join(row['found_keywords'])}")
                if row['patterns_found']:
                    st.write(f"**Patterns**: {', '.join(row['patterns_found'])}")
        
        # Visualization
        st.subheader("📊 Results Visualization")
        
        col1, col2 = st.columns(2)
        with col1:
            fig_dist = px.pie(
                names=['Spam', 'Ham'],
                values=[spam_count, ham_count],
                title='Classification Distribution',
                color=['Spam', 'Ham'],
                color_discrete_map={'Spam': 'red', 'Ham': 'green'}
            )
            st.plotly_chart(fig_dist, use_container_width=True)
        
        with col2:
            fig_probs = px.bar(
                results_df,
                y='spam_probability',
                title='Spam Probability by Message',
                labels={'index': 'Message #', 'spam_probability': 'Spam Probability'},
                color='is_spam',
                color_discrete_map={True: 'red', False: 'green'}
            )
            st.plotly_chart(fig_probs, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Spam Detection - Email/SMS spam filtering using keyword and pattern analysis")
