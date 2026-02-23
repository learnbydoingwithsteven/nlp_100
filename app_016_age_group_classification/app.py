"""
NLP App 016: Age Group Classification
Real-world use case: Author age prediction from text
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Age Group Classification",
    page_icon="🔤",
    layout="wide"
)

st.title("👶 Age Group Classification")
st.markdown("""
**Real-world Use Case**: Author age prediction from writing style
- Predict age group from text patterns
- Analyze vocabulary and slang usage
- Identify generational language markers
- Marketing and audience targeting
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
st.sidebar.markdown("---")
st.sidebar.markdown("**Age Groups:**")
st.sidebar.markdown("""
- 👶 Teen (13-19)
- 👤 Young Adult (20-35)
- 👔 Adult (36-55)
- 👴 Senior (56+)
""")

# Age-specific language markers
AGE_MARKERS = {
    'teen': ['lol', 'omg', 'bruh', 'literally', 'vibes', 'fr', 'ngl', 'lowkey', 'highkey', 'stan', 'slay', 'bestie', 'sus', 'cap', 'bet'],
    'young_adult': ['awesome', 'cool', 'dude', 'guys', 'basically', 'honestly', 'actually', 'netflix', 'app', 'online', 'social media', 'meme', 'wifi'],
    'adult': ['professional', 'experience', 'career', 'family', 'children', 'mortgage', 'investment', 'retirement', 'business', 'meeting', 'schedule'],
    'senior': ['wonderful', 'lovely', 'dear', 'pleased', 'kindly', 'regards', 'sincerely', 'traditional', 'back then', 'in my day', 'these days']
}

def classify_age_group(text):
    """Classify author age group based on writing style"""
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words)
    
    # Score each age group
    age_scores = {
        'teen': 0,
        'young_adult': 0,
        'adult': 0,
        'senior': 0
    }
    
    found_markers = {k: [] for k in age_scores.keys()}
    
    # Check for age markers
    for age, markers in AGE_MARKERS.items():
        for marker in markers:
            if marker in text_lower:
                count = text_lower.count(marker)
                age_scores[age] += count * 0.3
                found_markers[age].extend([marker] * count)
    
    # Emoji usage (more common in younger groups)
    emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]'
    emoji_count = len(re.findall(emoji_pattern, text))
    if emoji_count > 0:
        age_scores['teen'] += emoji_count * 0.4
        age_scores['young_adult'] += emoji_count * 0.2
    
    # Abbreviations and internet slang
    abbreviations = ['lmao', 'smh', 'tbh', 'imo', 'fyi', 'btw', 'idk']
    for abbr in abbreviations:
        if abbr in text_lower:
            age_scores['teen'] += 0.3
            age_scores['young_adult'] += 0.2
    
    # Formal language indicators
    formal_words = ['furthermore', 'therefore', 'moreover', 'consequently', 'nonetheless', 'heretofore']
    formal_count = sum(1 for word in formal_words if word in text_lower)
    if formal_count > 0:
        age_scores['adult'] += formal_count * 0.3
        age_scores['senior'] += formal_count * 0.2
    
    # Sentence complexity (average word length)
    avg_word_length = sum(len(w) for w in words) / max(word_count, 1)
    if avg_word_length > 6:
        age_scores['adult'] += 0.2
        age_scores['senior'] += 0.2
    elif avg_word_length < 4.5:
        age_scores['teen'] += 0.2
    
    # Exclamation marks (more common in younger)
    exclamations = text.count('!')
    if exclamations > 2:
        age_scores['teen'] += exclamations * 0.1
        age_scores['young_adult'] += exclamations * 0.05
    
    # Find predicted age group
    if sum(age_scores.values()) == 0:
        # Default if no indicators
        predicted_age = 'young_adult'
        confidence = 0.3
    else:
        predicted_age = max(age_scores.items(), key=lambda x: x[1])[0]
        total = sum(age_scores.values())
        confidence = age_scores[predicted_age] / total if total > 0 else 0
    
    # Map to display names
    age_display = {
        'teen': '👶 Teen (13-19)',
        'young_adult': '👤 Young Adult (20-35)',
        'adult': '👔 Adult (36-55)',
        'senior': '👴 Senior (56+)'
    }
    
    age_ranges = {
        'teen': '13-19 years',
        'young_adult': '20-35 years',
        'adult': '36-55 years',
        'senior': '56+ years'
    }
    
    return {
        'text': text,
        'predicted_age': predicted_age,
        'age_display': age_display[predicted_age],
        'age_range': age_ranges[predicted_age],
        'confidence': confidence,
        'age_scores': age_scores,
        'found_markers': {k: v for k, v in found_markers.items() if v},
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
    
    if st.button("🔍 Classify Age", type="primary"):
        if user_input.strip():
            with st.spinner("Analyzing..."):
                result = classify_age_group(user_input)
            
            st.success("✅ Classification Complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Predicted Age", result['age_display'])
            with col2:
                st.metric("Age Range", result['age_range'])
            with col3:
                st.metric("Confidence", f"{result['confidence']:.1%}")
            
            # Age scores
            st.subheader("📊 Age Group Scores")
            scores_data = pd.DataFrame({
                'Age Group': ['Teen', 'Young Adult', 'Adult', 'Senior'],
                'Score': [result['age_scores']['teen'], result['age_scores']['young_adult'], 
                         result['age_scores']['adult'], result['age_scores']['senior']]
            })
            fig = px.bar(scores_data, x='Age Group', y='Score',
                        title='Age Group Probability Distribution',
                        color='Score', color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
            
            if result['found_markers']:
                st.subheader("🔍 Language Markers Found")
                for age, markers in result['found_markers'].items():
                    st.write(f"**{age.replace('_', ' ').title()}**: {', '.join(set(markers))}")
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
                    result = classify_age_group(str(text))
                    results.append({
                        'text': result['text'][:60] + '...',
                        'age_group': result['age_display'],
                        'confidence': result['confidence']
                    })
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Classified {len(results_df)} texts!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total", len(results_df))
                with col2:
                    most_common = results_df['age_group'].mode()[0] if len(results_df) > 0 else "N/A"
                    st.metric("Most Common", most_common)
                with col3:
                    avg_conf = results_df['confidence'].mean()
                    st.metric("Avg Confidence", f"{avg_conf:.1%}")
                
                age_counts = results_df['age_group'].value_counts()
                fig = px.bar(x=age_counts.index, y=age_counts.values,
                            title='Age Group Distribution',
                            labels={'x': 'Age Group', 'y': 'Count'})
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
        "OMG this is literally so cool! Lowkey the best thing ever, ngl 😍",
        "Hey guys, honestly this is pretty awesome. I saw it on social media and had to check it out!",
        "My professional experience in business has taught me the importance of careful investment planning for retirement.",
        "Dear friends, it was a lovely gathering. These days, things are quite different from back then. Sincerely yours."
    ]
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        for text in samples:
            result = classify_age_group(text)
            results.append({
                'text': text[:50] + '...',
                'age': result['age_display'],
                'confidence': result['confidence']
            })
        
        results_df = pd.DataFrame(results)
        st.success("✅ Complete!")
        
        for idx, row in results_df.iterrows():
            st.info(f"{row['age']} ({row['confidence']:.1%}): {row['text']}")
        
        fig = px.bar(results_df, x=results_df.index, y='confidence',
                     title='Confidence Scores',
                     color='confidence', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Age Group Classification - Predict author age from writing style")
st.caption("💡 Based on vocabulary, slang, emojis, and language patterns")
