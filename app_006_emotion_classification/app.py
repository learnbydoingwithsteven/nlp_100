"""
NLP App 006: Emotion Classification
Real-world use case: Multi-emotion detection (joy, anger, sadness, etc.)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Emotion Classification",
    page_icon="🔤",
    layout="wide"
)

st.title("😊 Emotion Classification")
st.markdown("""
**Real-world Use Case**: Multi-emotion detection for customer feedback and mental health
- Detect 6 primary emotions: Joy, Sadness, Anger, Fear, Surprise, Love
- Intensity scoring for each emotion
- Visual emotion distribution
- Sentiment context analysis
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
st.sidebar.markdown("---")
st.sidebar.markdown("**Emotions Detected:**")
st.sidebar.markdown("- 😊 Joy\n- 😢 Sadness\n- 😠 Anger\n- 😨 Fear\n- 😮 Surprise\n- ❤️ Love")

# Emotion keywords dictionary
EMOTION_KEYWORDS = {
    'joy': ['happy', 'joy', 'excited', 'wonderful', 'amazing', 'great', 'fantastic', 'excellent', 
            'love', 'delighted', 'pleased', 'cheerful', 'glad', 'thrilled', 'awesome', 'perfect'],
    'sadness': ['sad', 'unhappy', 'depressed', 'miserable', 'sorrowful', 'disappointed', 
                'grief', 'sorry', 'unfortunate', 'terrible', 'awful', 'bad', 'poor', 'crying'],
    'anger': ['angry', 'mad', 'furious', 'rage', 'hate', 'annoyed', 'irritated', 
              'frustrated', 'outraged', 'disgusted', 'pissed', 'furious'],
    'fear': ['afraid', 'scared', 'fear', 'terrified', 'anxious', 'worried', 'nervous', 
             'panic', 'frightened', 'alarmed', 'terror'],
    'surprise': ['surprise', 'shocked', 'amazed', 'astonished', 'unexpected', 'wow', 
                 'incredible', 'unbelievable', 'sudden', 'startled'],
    'love': ['love', 'adore', 'cherish', 'affection', 'caring', 'romantic', 'passion', 
             'devoted', 'fond', 'treasure', 'sweetheart']
}

EMOTION_ICONS = {
    'joy': '\ud83d\ude0a',
    'sadness': '\ud83d\ude22',
    'anger': '\ud83d\ude20',
    'fear': '\ud83d\ude28',
    'surprise': '\ud83d\ude2e',
    'love': '\u2764\ufe0f'
}

def classify_emotion(text):
    """Classify emotions in text using keyword-based approach"""
    text_lower = text.lower()
    word_count = len(text.split())
    
    # Initialize emotion scores
    scores = {emotion: 0.0 for emotion in EMOTION_KEYWORDS.keys()}
    detected_words = {emotion: [] for emotion in EMOTION_KEYWORDS.keys()}
    
    # Count emotion keywords
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                scores[emotion] += 0.15
                detected_words[emotion].append(keyword)
                
                # Boost for multiple occurrences
                count = text_lower.count(keyword)
                if count > 1:
                    scores[emotion] += 0.05 * (count - 1)
    
    # Pattern boosters
    if re.search(r'!{2,}', text):  # Excitement
        scores['joy'] += 0.1
        scores['surprise'] += 0.05
    
    if re.search(r'[A-Z]{3,}', text):  # Caps
        scores['anger'] += 0.1
        scores['joy'] += 0.05
    
    # Normalize scores
    for emotion in scores:
        scores[emotion] = min(scores[emotion], 1.0)
    
    # Find dominant emotion
    if max(scores.values()) > 0:
        dominant_emotion = max(scores, key=scores.get)
        dominant_score = scores[dominant_emotion]
    else:
        dominant_emotion = "neutral"
        dominant_score = 0.0
    
    # Calculate intensity
    total_score = sum(scores.values())
    if total_score > 0.7:
        intensity = "High"
    elif total_score > 0.3:
        intensity = "Medium"
    else:
        intensity = "Low"
    
    return {
        'text': text,
        'dominant_emotion': dominant_emotion,
        'dominant_score': dominant_score,
        'intensity': intensity,
        'joy': scores['joy'],
        'sadness': scores['sadness'],
        'anger': scores['anger'],
        'fear': scores['fear'],
        'surprise': scores['surprise'],
        'love': scores['love'],
        'detected_words': detected_words,
        'word_count': word_count
    }

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Analysis")
    
    user_input = st.text_area(
        "Enter text to analyze emotions:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    if st.button("🔍 Analyze Emotions", type="primary"):
        if user_input.strip():
            with st.spinner("Analyzing emotions..."):
                result = classify_emotion(user_input)
            
            st.success("✅ Analysis Complete!")
            
            # Main metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                icon = EMOTION_ICONS.get(result['dominant_emotion'], '😐')
                st.metric("Dominant Emotion", f"{icon} {result['dominant_emotion'].title()}")
            with col2:
                st.metric("Confidence", f"{result['dominant_score']:.1%}")
            with col3:
                st.metric("Intensity", result['intensity'])
            with col4:
                st.metric("Word Count", result['word_count'])
            
            # Emotion distribution
            st.subheader("📊 Emotion Distribution")
            
            emotions = {
                'Joy': result['joy'],
                'Sadness': result['sadness'],
                'Anger': result['anger'],
                'Fear': result['fear'],
                'Surprise': result['surprise'],
                'Love': result['love']
            }
            
            # Radar chart
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=list(emotions.values()),
                theta=list(emotions.keys()),
                fill='toself',
                name='Emotions'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=False,
                title="Emotion Radar Chart"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Bar chart
            fig_bar = px.bar(
                x=list(emotions.keys()),
                y=list(emotions.values()),
                title="Emotion Scores",
                labels={'x': 'Emotion', 'y': 'Score'},
                color=list(emotions.values()),
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Detected keywords
            st.subheader("🔎 Detected Keywords")
            any_detected = False
            for emotion, words in result['detected_words'].items():
                if words:
                    any_detected = True
                    icon = EMOTION_ICONS[emotion]
                    st.info(f"**{icon} {emotion.title()}**: {', '.join(set(words))}")
            
            if not any_detected:
                st.info("😐 No strong emotional keywords detected")
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
                    result = classify_emotion(str(text))
                    simple_result = {
                        'text': result['text'][:80] + '...' if len(result['text']) > 80 else result['text'],
                        'dominant_emotion': result['dominant_emotion'],
                        'dominant_score': result['dominant_score'],
                        'intensity': result['intensity'],
                        'joy': result['joy'],
                        'sadness': result['sadness'],
                        'anger': result['anger']
                    }
                    results.append(simple_result)
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Analyzed {len(results_df)} texts!")
                
                # Summary
                st.subheader("📊 Summary Statistics")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Analyzed", len(results_df))
                with col2:
                    most_common = results_df['dominant_emotion'].mode()[0] if len(results_df) > 0 else "N/A"
                    st.metric("Most Common", most_common.title())
                with col3:
                    avg_confidence = results_df['dominant_score'].mean()
                    st.metric("Avg Confidence", f"{avg_confidence:.1%}")
                with col4:
                    positive = len(results_df[results_df['dominant_emotion'].isin(['joy', 'love'])])
                    st.metric("Positive", positive)
                
                # Emotion distribution
                emotion_counts = results_df['dominant_emotion'].value_counts()
                fig = px.pie(values=emotion_counts.values, names=emotion_counts.index,
                            title="Emotion Distribution")
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
    st.markdown("**Testing with diverse emotional expressions**")
    
    sample_texts = [
        "I'm so happy and excited! This is the best day ever!",
        "I feel really sad and disappointed about the news.",
        "This makes me so angry! I can't believe this happened!",
        "I'm terrified and afraid of what might happen next.",
        "Wow! I'm completely shocked and surprised by this!",
        "I love you so much! You mean everything to me.",
        "The weather is nice today."
    ]
    
    with st.expander("👁️ View Sample Texts"):
        for i, text in enumerate(sample_texts, 1):
            st.write(f"{i}. {text}")
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        with st.spinner("Analyzing emotions..."):
            for text in sample_texts:
                result = classify_emotion(text)
                simple_result = {
                    'text': result['text'],
                    'emotion': result['dominant_emotion'],
                    'score': result['dominant_score'],
                    'intensity': result['intensity']
                }
                results.append(simple_result)
        
        results_df = pd.DataFrame(results)
        st.success("✅ Demo Complete!")
        
        # Summary
        st.subheader("📊 Demo Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Samples", len(results_df))
        with col2:
            unique_emotions = results_df['emotion'].nunique()
            st.metric("Unique Emotions", unique_emotions)
        with col3:
            avg_score = results_df['score'].mean()
            st.metric("Avg Confidence", f"{avg_score:.1%}")
        
        # Display results
        st.subheader("📋 Detailed Results")
        for idx, row in results_df.iterrows():
            icon = EMOTION_ICONS.get(row['emotion'], '😐')
            with st.expander(f"{icon} Sample {idx+1}: {row['emotion'].title()}"):
                st.write(f"**Text**: {row['text']}")
                cols = st.columns(3)
                with cols[0]:
                    st.metric("Emotion", row['emotion'].title())
                with cols[1]:
                    st.metric("Confidence", f"{row['score']:.1%}")
                with cols[2]:
                    st.metric("Intensity", row['intensity'])
        
        # Visualization
        fig = px.bar(results_df, x=results_df.index, y='score',
                     color='emotion', title='Emotion Confidence by Sample',
                     labels={'x': 'Sample #', 'score': 'Confidence'})
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Emotion Classification - Multi-emotion detection for text analysis")
st.caption("💡 Tip: Use this for customer feedback analysis, mental health monitoring, or social media sentiment")
