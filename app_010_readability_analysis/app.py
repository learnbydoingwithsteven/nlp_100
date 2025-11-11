"""
NLP App 010: Readability Analysis
Real-world use case: Text complexity assessment
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
import math

st.set_page_config(
    page_title="Readability Analysis",
    page_icon="🔤",
    layout="wide"
)

st.title("📖 Readability Analysis")
st.markdown("""
**Real-world Use Case**: Text complexity and readability assessment
- Multiple readability formulas (Flesch Reading Ease, Flesch-Kincaid Grade, SMOG)
- Grade level estimation
- Reading time calculation
- Audience targeting recommendations
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
st.sidebar.markdown("---")
st.sidebar.markdown("**Readability Metrics:**")
st.sidebar.markdown("""
- 📊 Flesch Reading Ease
- 🎯 F-K Grade Level
- 📖 SMOG Index
- 👥 Target Audience
- ⏱️ Reading Time
""")

def count_syllables(word):
    """Estimate syllable count in a word"""
    word = word.lower()
    count = 0
    vowels = 'aeiouy'
    prev_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            count += 1
        prev_was_vowel = is_vowel
    
    if word.endswith('e'):
        count -= 1
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        count += 1
    if count == 0:
        count = 1
    
    return count

def analyze_readability(text):
    """Analyze text readability using multiple formulas"""
    
    # Basic counts
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences) if sentences else 1
    
    words = text.split()
    word_count = len(words) if words else 1
    
    # Character and syllable counts
    char_count = len(text.replace(' ', ''))
    syllable_count = sum(count_syllables(word) for word in words)
    
    # Average metrics
    avg_sentence_length = word_count / sentence_count
    avg_syllables_per_word = syllable_count / word_count
    avg_word_length = char_count / word_count
    
    # Flesch Reading Ease (0-100, higher = easier)
    flesch_reading_ease = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
    flesch_reading_ease = max(0, min(100, flesch_reading_ease))
    
    # Flesch-Kincaid Grade Level
    flesch_kincaid_grade = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
    flesch_kincaid_grade = max(0, flesch_kincaid_grade)
    
    # SMOG Index (requires 30+ sentences for accuracy, but we'll estimate)
    if sentence_count >= 3:
        polysyllables = sum(1 for word in words if count_syllables(word) >= 3)
        smog_index = 1.0430 * math.sqrt(polysyllables * (30 / sentence_count)) + 3.1291
        smog_index = max(0, smog_index)
    else:
        smog_index = flesch_kincaid_grade
    
    # Reading difficulty classification
    if flesch_reading_ease >= 90:
        difficulty = "Very Easy"
        audience = "5th grade"
    elif flesch_reading_ease >= 80:
        difficulty = "Easy"
        audience = "6th grade"
    elif flesch_reading_ease >= 70:
        difficulty = "Fairly Easy"
        audience = "7th grade"
    elif flesch_reading_ease >= 60:
        difficulty = "Standard"
        audience = "8th-9th grade"
    elif flesch_reading_ease >= 50:
        difficulty = "Fairly Difficult"
        audience = "10th-12th grade"
    elif flesch_reading_ease >= 30:
        difficulty = "Difficult"
        audience = "College"
    else:
        difficulty = "Very Difficult"
        audience = "College graduate"
    
    # Reading time (average reading speed: 200-250 wpm)
    reading_time_min = word_count / 250
    reading_time_sec = (reading_time_min % 1) * 60
    
    return {
        'text': text,
        'word_count': word_count,
        'sentence_count': sentence_count,
        'syllable_count': syllable_count,
        'avg_sentence_length': avg_sentence_length,
        'avg_syllables_per_word': avg_syllables_per_word,
        'avg_word_length': avg_word_length,
        'flesch_reading_ease': flesch_reading_ease,
        'flesch_kincaid_grade': flesch_kincaid_grade,
        'smog_index': smog_index,
        'difficulty': difficulty,
        'target_audience': audience,
        'reading_time_minutes': int(reading_time_min),
        'reading_time_seconds': int(reading_time_sec)
    }

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Processing")
    
    user_input = st.text_area(
        "Enter text to process:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    if st.button("🔍 Analyze Readability", type="primary"):
        if user_input.strip():
            with st.spinner("Analyzing..."):
                result = analyze_readability(user_input)
            
            st.success("✅ Analysis Complete!")
            
            # Main metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Difficulty", result['difficulty'])
            with col2:
                st.metric("Grade Level", f"{result['flesch_kincaid_grade']:.1f}")
            with col3:
                st.metric("Target Audience", result['target_audience'])
            with col4:
                reading_time = f"{result['reading_time_minutes']}m {result['reading_time_seconds']}s"
                st.metric("Reading Time", reading_time)
            
            # Readability scores
            st.subheader("📊 Readability Scores")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=result['flesch_reading_ease'],
                    title={'text': "Flesch Reading Ease"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "darkblue"},
                           'steps': [
                               {'range': [0, 30], 'color': "red"},
                               {'range': [30, 50], 'color': "orange"},
                               {'range': [50, 70], 'color': "yellow"},
                               {'range': [70, 100], 'color': "lightgreen"}]}
                ))
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=result['flesch_kincaid_grade'],
                    title={'text': "F-K Grade Level"},
                    gauge={'axis': {'range': [0, 18]},
                           'bar': {'color': "darkgreen"}}
                ))
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)
            
            with col3:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=result['smog_index'],
                    title={'text': "SMOG Index"},
                    gauge={'axis': {'range': [0, 18]},
                           'bar': {'color': "purple"}}
                ))
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics
            st.subheader("📈 Detailed Metrics")
            
            metrics_df = pd.DataFrame({
                'Metric': ['Words', 'Sentences', 'Syllables', 'Avg Sentence Length', 
                          'Avg Syllables/Word', 'Avg Word Length'],
                'Value': [
                    result['word_count'],
                    result['sentence_count'],
                    result['syllable_count'],
                    f"{result['avg_sentence_length']:.1f}",
                    f"{result['avg_syllables_per_word']:.2f}",
                    f"{result['avg_word_length']:.1f}"
                ]
            })
            st.table(metrics_df)
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
                    result = analyze_readability(str(text))
                    simple_result = {
                        'text': result['text'][:60] + '...' if len(result['text']) > 60 else result['text'],
                        'flesch_ease': result['flesch_reading_ease'],
                        'grade_level': result['flesch_kincaid_grade'],
                        'difficulty': result['difficulty'],
                        'word_count': result['word_count']
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
                    avg_ease = results_df['flesch_ease'].mean()
                    st.metric("Avg Reading Ease", f"{avg_ease:.1f}")
                with col3:
                    avg_grade = results_df['grade_level'].mean()
                    st.metric("Avg Grade Level", f"{avg_grade:.1f}")
                with col4:
                    avg_words = results_df['word_count'].mean()
                    st.metric("Avg Word Count", f"{avg_words:.0f}")
                
                # Visualizations
                fig = px.histogram(results_df, x='flesch_ease',
                                  title='Readability Distribution',
                                  labels={'flesch_ease': 'Flesch Reading Ease'})
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
    st.markdown("**Testing with texts of varying complexity**")
    
    sample_texts = [
        "The cat sat on the mat. It was a sunny day.",
        "Scientists have discovered a new species of butterfly in the Amazon rainforest, which exhibits unique patterns.",
        "The implementation of quantum computing algorithms necessitates sophisticated mathematical frameworks.",
        "I like ice cream. It is good. My dog likes it too.",
        "Contemporary socioeconomic paradigms demonstrate multifaceted interdependencies within globalized infrastructures."
    ]
    
    with st.expander("👁️ View Sample Texts"):
        for i, text in enumerate(sample_texts, 1):
            st.write(f"{i}. {text}")
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        with st.spinner("Analyzing readability..."):
            for text in sample_texts:
                result = analyze_readability(text)
                results.append({
                    'text': text[:50] + '...' if len(text) > 50 else text,
                    'ease': result['flesch_reading_ease'],
                    'grade': result['flesch_kincaid_grade'],
                    'difficulty': result['difficulty']
                })
        
        results_df = pd.DataFrame(results)
        st.success("✅ Demo Complete!")
        
        # Summary
        st.subheader("📊 Demo Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Samples", len(results_df))
        with col2:
            avg = results_df['ease'].mean()
            st.metric("Avg Reading Ease", f"{avg:.1f}")
        with col3:
            avg_grade = results_df['grade'].mean()
            st.metric("Avg Grade", f"{avg_grade:.1f}")
        
        # Results
        st.subheader("📋 Results")
        for idx, row in results_df.iterrows():
            with st.expander(f"Sample {idx+1}: {row['difficulty']}"):
                st.write(f"**Text**: {row['text']}")
                cols = st.columns(3)
                with cols[0]:
                    st.metric("Reading Ease", f"{row['ease']:.1f}")
                with cols[1]:
                    st.metric("Grade Level", f"{row['grade']:.1f}")
                with cols[2]:
                    st.metric("Difficulty", row['difficulty'])
        
        # Visualization
        fig = px.bar(results_df, x=results_df.index, y='ease',
                     title='Reading Ease by Sample',
                     labels={'x': 'Sample #', 'ease': 'Flesch Reading Ease'},
                     color='ease', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Readability Analysis - Text complexity assessment for content optimization")
st.caption("💡 Tip: Use this to ensure your content matches your target audience's reading level")
