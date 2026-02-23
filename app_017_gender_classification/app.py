"""
NLP App 017: Gender Classification
Real-world use case: Author gender prediction
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Gender Classification",
    page_icon="🔤",
    layout="wide"
)

st.title("👤 Gender Classification")
st.markdown("""
**Real-world Use Case**: Author gender prediction from writing style
- Predict author gender from text patterns
- Analyze communication styles
- Marketing and audience analysis
- Sociolinguistic research
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
st.sidebar.markdown("---")
st.sidebar.markdown("**Classification Categories:**")
st.sidebar.markdown("""
- 🚹 Male
- 🚺 Female
- ⚧️ Neutral/Uncertain
""")
st.sidebar.caption("⚠️ Note: Based on linguistic patterns, not identity")

# Gender-associated language patterns (based on sociolinguistic research)
GENDER_MARKERS = {
    'male': ['sports', 'car', 'game', 'gaming', 'tech', 'computer', 'beer', 'football', 'dude', 'bro', 'man', 'guys'],
    'female': ['love', 'feel', 'shopping', 'cute', 'adorable', 'gorgeous', 'beautiful', 'wonderful', 'excited', 'amazing', 'perfect']
}

def classify_gender(text):
    """Classify author gender based on writing style"""
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words)
    
    # Initialize scores
    male_score = 0
    female_score = 0
    found_male = []
    found_female = []
    
    # Check for gender markers
    for marker in GENDER_MARKERS['male']:
        if marker in text_lower:
            count = text_lower.count(marker)
            male_score += count * 0.3
            found_male.extend([marker] * count)
    
    for marker in GENDER_MARKERS['female']:
        if marker in text_lower:
            count = text_lower.count(marker)
            female_score += count * 0.3
            found_female.extend([marker] * count)
    
    # Emotional language (more common in female writing)
    emotion_words = ['feel', 'felt', 'emotion', 'heart', 'happy', 'sad', 'excited', 'worried']
    emotion_count = sum(1 for word in emotion_words if word in text_lower)
    female_score += emotion_count * 0.2
    
    # Assertive language (more common in male writing)
    assertive_words = ['definitely', 'obviously', 'clearly', 'actually', 'fact']
    assertive_count = sum(1 for word in assertive_words if word in text_lower)
    male_score += assertive_count * 0.2
    
    # Hedging language (more common in female writing)
    hedges = ['maybe', 'perhaps', 'might', 'possibly', 'i think', 'i feel', 'sort of', 'kind of']
    hedge_count = sum(1 for hedge in hedges if hedge in text_lower)
    female_score += hedge_count * 0.25
    
    # Intensifiers
    intensifiers = ['so', 'very', 'really', 'quite', 'extremely']
    intensifier_count = sum(text_lower.count(word) for word in intensifiers)
    female_score += intensifier_count * 0.1
    
    # Question marks (more common in female writing)
    question_count = text.count('?')
    female_score += question_count * 0.15
    
    # Exclamation marks
    exclamation_count = text.count('!')
    if exclamation_count > 0:
        female_score += exclamation_count * 0.1
    
    # Determine classification
    total_score = male_score + female_score
    
    if total_score == 0 or abs(male_score - female_score) < 0.3:
        predicted_gender = 'neutral'
        gender_display = '⚧️ Neutral/Uncertain'
        confidence = 0.5
    elif male_score > female_score:
        predicted_gender = 'male'
        gender_display = '🚹 Male'
        confidence = male_score / total_score if total_score > 0 else 0.5
    else:
        predicted_gender = 'female'
        gender_display = '🚺 Female'
        confidence = female_score / total_score if total_score > 0 else 0.5
    
    return {
        'text': text,
        'predicted_gender': predicted_gender,
        'gender_display': gender_display,
        'confidence': confidence,
        'male_score': male_score,
        'female_score': female_score,
        'found_male_markers': found_male,
        'found_female_markers': found_female,
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
    
    if st.button("🔍 Classify", type="primary"):
        if user_input.strip():
            with st.spinner("Analyzing..."):
                result = classify_gender(user_input)
            
            st.success("✅ Classification Complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Predicted Gender", result['gender_display'])
            with col2:
                st.metric("Confidence", f"{result['confidence']:.1%}")
            with col3:
                st.metric("Words", result['word_count'])
            
            # Scores comparison
            st.subheader("📊 Gender Scores")
            scores_df = pd.DataFrame({
                'Category': ['Male', 'Female'],
                'Score': [result['male_score'], result['female_score']]
            })
            fig = px.bar(scores_df, x='Category', y='Score',
                        title='Gender Score Comparison',
                        color='Score', color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
            
            # Found markers
            col1, col2 = st.columns(2)
            with col1:
                if result['found_male_markers']:
                    st.write("**Male Markers:**", ', '.join(set(result['found_male_markers'])))
            with col2:
                if result['found_female_markers']:
                    st.write("**Female Markers:**", ', '.join(set(result['found_female_markers'])))
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
            if st.button("🔍 Classify All", type="primary"):
                results = []
                progress_bar = st.progress(0)
                
                for idx, text in enumerate(df['text']):
                    result = classify_gender(str(text))
                    results.append({
                        'text': result['text'][:60] + '...',
                        'gender': result['gender_display'],
                        'confidence': result['confidence']
                    })
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Classified {len(results_df)} texts!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total", len(results_df))
                with col2:
                    male = len(results_df[results_df['gender'].str.contains('Male') & ~results_df['gender'].str.contains('Female')])
                    st.metric("Male", male)
                with col3:
                    female = len(results_df[results_df['gender'].str.contains('Female')])
                    st.metric("Female", female)
                
                gender_counts = results_df['gender'].value_counts()
                fig = px.pie(values=gender_counts.values, names=gender_counts.index,
                            title='Gender Distribution')
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
        "I went to the game last night with my bro. The team played great and we had some beers after.",
        "I feel so excited! This is absolutely adorable and perfect. Love it!",
        "The technical implementation requires careful analysis. Obviously, we need to consider the facts.",
        "Maybe I think this could work? I'm not sure, but it might be a good idea, sort of."
    ]
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        for text in samples:
            result = classify_gender(text)
            results.append({
                'text': text[:50] + '...',
                'gender': result['gender_display'],
                'confidence': result['confidence']
            })
        
        results_df = pd.DataFrame(results)
        st.success("✅ Complete!")
        
        for idx, row in results_df.iterrows():
            st.info(f"{row['gender']} ({row['confidence']:.1%}): {row['text']}")
        
        fig = px.bar(results_df, x=results_df.index, y='confidence',
                     title='Confidence Scores',
                     color='confidence', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Gender Classification - Predict author gender from writing style")
st.caption("⚠️ Based on linguistic patterns, not personal identity. For research/analysis purposes only.")
