"""
NLP App 008: Topic Modeling
Real-world use case: Document topic extraction using LDA
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Topic Modeling",
    page_icon="🔤",
    layout="wide"
)

st.title("📚 Topic Modeling")
st.markdown("""
**Real-world Use Case**: Document topic extraction and clustering
- Extract main topics from documents
- Identify key themes and subjects
- Keyword-based topic discovery
- Document clustering and organization
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
num_topics = st.sidebar.slider("Number of Topics", 2, 5, 3)
min_word_freq = st.sidebar.slider("Min Word Frequency", 1, 3, 2)
st.sidebar.markdown("---")
st.sidebar.markdown("**Topic Categories:**")
st.sidebar.markdown("- 💼 Business\n- 🔬 Technology\n- 🏥 Health\n- ⚽ Sports\n- 🎬 Entertainment\n- 📰 General")

# Topic keyword sets
TOPIC_KEYWORDS = {
    'business': ['business', 'company', 'market', 'profit', 'sales', 'revenue', 'corporate', 'financial', 'investment', 'stock', 'economy', 'trade', 'customer', 'product', 'service'],
    'technology': ['technology', 'software', 'computer', 'digital', 'ai', 'data', 'internet', 'app', 'code', 'programming', 'algorithm', 'system', 'network', 'cyber', 'innovation'],
    'health': ['health', 'medical', 'doctor', 'hospital', 'patient', 'disease', 'treatment', 'medicine', 'care', 'wellness', 'fitness', 'symptoms', 'diagnosis', 'therapy'],
    'sports': ['sports', 'game', 'team', 'player', 'match', 'win', 'score', 'championship', 'football', 'basketball', 'soccer', 'athletic', 'competition', 'training'],
    'entertainment': ['movie', 'film', 'music', 'show', 'actor', 'celebrity', 'entertainment', 'tv', 'series', 'concert', 'performance', 'art', 'culture', 'media'],
    'politics': ['government', 'political', 'president', 'election', 'vote', 'policy', 'law', 'congress', 'senate', 'minister', 'democracy', 'party', 'campaign'],
    'education': ['education', 'school', 'student', 'teacher', 'university', 'learning', 'study', 'course', 'degree', 'academic', 'research', 'knowledge'],
    'science': ['science', 'research', 'study', 'scientist', 'discovery', 'experiment', 'theory', 'analysis', 'data', 'evidence', 'hypothesis']
}

STOPWORDS = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'])

def extract_topics(text, n_topics=3):
    """Extract topics from text using keyword matching"""
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    word_count = len(words)
    
    # Remove stopwords
    meaningful_words = [w for w in words if w not in STOPWORDS and len(w) > 3]
    
    # Calculate topic scores
    topic_scores = {}
    topic_keywords_found = {}
    
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0
        found_keywords = []
        for keyword in keywords:
            if keyword in text_lower:
                count = text_lower.count(keyword)
                score += count
                found_keywords.extend([keyword] * count)
        
        topic_scores[topic] = score
        topic_keywords_found[topic] = found_keywords[:10]  # Limit
    
    # Get top topics
    sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
    top_topics = [(t, s) for t, s in sorted_topics if s > 0][:n_topics]
    
    if not top_topics:
        top_topics = [('general', 0)]
    
    # Extract key terms (most frequent meaningful words)
    word_freq = Counter(meaningful_words)
    key_terms = [word for word, freq in word_freq.most_common(10) if freq >= min_word_freq]
    
    # Primary topic
    primary_topic = top_topics[0][0] if top_topics else 'general'
    primary_score = top_topics[0][1] if top_topics else 0
    
    # Calculate topic distribution
    total_score = sum(s for _, s in sorted_topics) if sum(s for _, s in sorted_topics) > 0 else 1
    topic_distribution = {t: (s / total_score) for t, s in sorted_topics}
    
    return {
        'text': text,
        'primary_topic': primary_topic,
        'primary_score': primary_score,
        'top_topics': top_topics,
        'topic_distribution': topic_distribution,
        'key_terms': key_terms,
        'topic_keywords_found': topic_keywords_found,
        'word_count': word_count,
        'unique_words': len(set(meaningful_words))
    }

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Processing")
    
    user_input = st.text_area(
        "Enter text to process:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    if st.button("🔍 Extract Topics", type="primary"):
        if user_input.strip():
            with st.spinner("Extracting topics..."):
                result = extract_topics(user_input, num_topics)
            
            st.success("✅ Topic Extraction Complete!")
            
            # Main metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Primary Topic", result['primary_topic'].title())
            with col2:
                st.metric("Topic Strength", result['primary_score'])
            with col3:
                st.metric("Word Count", result['word_count'])
            with col4:
                st.metric("Unique Words", result['unique_words'])
            
            # Top topics
            st.subheader("🎯 Detected Topics")
            for topic, score in result['top_topics']:
                if score > 0:
                    st.info(f"**{topic.title()}**: Score = {score}")
            
            # Topic distribution
            st.subheader("📊 Topic Distribution")
            dist_data = [(t, s) for t, s in result['topic_distribution'].items() if s > 0]
            if dist_data:
                topics, scores = zip(*dist_data[:num_topics])
                fig = px.pie(values=scores, names=topics, title="Topic Distribution")
                st.plotly_chart(fig, use_container_width=True)
            
            # Key terms
            if result['key_terms']:
                st.subheader("🔑 Key Terms")
                st.write(", ".join(result['key_terms']))
            
            # Found keywords per topic
            st.subheader("🔍 Topic Keywords Found")
            for topic, keywords in result['topic_keywords_found'].items():
                if keywords:
                    st.write(f"**{topic.title()}**: {', '.join(set(keywords))}")
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
            if st.button("🔍 Extract Topics from All", type="primary"):
                results = []
                progress_bar = st.progress(0)
                
                for idx, text in enumerate(df['text']):
                    result = extract_topics(str(text), num_topics)
                    simple_result = {
                        'text': result['text'][:60] + '...' if len(result['text']) > 60 else result['text'],
                        'primary_topic': result['primary_topic'],
                        'topic_strength': result['primary_score'],
                        'key_terms': ', '.join(result['key_terms'][:3]) if result['key_terms'] else 'N/A'
                    }
                    results.append(simple_result)
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Analyzed {len(results_df)} documents!")
                
                # Summary stats
                st.subheader("📊 Summary Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Documents Analyzed", len(results_df))
                with col2:
                    most_common = results_df['primary_topic'].mode()[0] if len(results_df) > 0 else "N/A"
                    st.metric("Most Common Topic", most_common.title())
                with col3:
                    unique_topics = results_df['primary_topic'].nunique()
                    st.metric("Unique Topics", unique_topics)
                
                # Topic distribution
                topic_counts = results_df['primary_topic'].value_counts()
                fig = px.bar(x=topic_counts.index, y=topic_counts.values,
                            title="Document Topic Distribution",
                            labels={'x': 'Topic', 'y': 'Count'})
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
    st.markdown("**Testing with diverse document types**")
    
    sample_texts = [
        "The stock market showed strong performance today with major tech companies posting record profits. Investors are optimistic about the financial quarter ahead.",
        "Scientists have discovered a new treatment for the disease that shows promising results in clinical trials. The medical breakthrough could help millions of patients.",
        "The championship game was intense with the home team scoring in the final minutes. The players celebrated their victory with fans cheering.",
        "The new software update includes advanced AI features and improved data processing capabilities. Developers are excited about the enhanced programming tools.",
        "The blockbuster movie broke box office records this weekend. Critics praised the performances and the director's artistic vision."
    ]
    
    with st.expander("👁️ View Sample Documents"):
        for i, text in enumerate(sample_texts, 1):
            st.write(f"{i}. {text}")
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        with st.spinner("Extracting topics..."):
            for text in sample_texts:
                result = extract_topics(text, num_topics)
                results.append({
                    'text': text[:50] + '...',
                    'primary_topic': result['primary_topic'],
                    'strength': result['primary_score'],
                    'key_terms': ', '.join(result['key_terms'][:3]) if result['key_terms'] else 'N/A'
                })
        
        results_df = pd.DataFrame(results)
        st.success("✅ Demo Complete!")
        
        # Summary
        st.subheader("📊 Demo Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Documents", len(results_df))
        with col2:
            unique = results_df['primary_topic'].nunique()
            st.metric("Unique Topics", unique)
        with col3:
            avg_strength = results_df['strength'].mean()
            st.metric("Avg Strength", f"{avg_strength:.1f}")
        
        # Results
        st.subheader("📋 Topic Classification")
        for idx, row in results_df.iterrows():
            with st.expander(f"Document {idx+1}: {row['primary_topic'].title()}"):
                st.write(f"**Text**: {row['text']}")
                st.write(f"**Key Terms**: {row['key_terms']}")
                st.metric("Topic Strength", row['strength'])
        
        # Visualization
        topic_counts = results_df['primary_topic'].value_counts()
        fig = px.bar(x=topic_counts.index, y=topic_counts.values,
                     title='Topics in Sample Documents',
                     labels={'x': 'Topic', 'y': 'Count'})
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Topic Modeling - Keyword-based document topic extraction and clustering")
st.caption("💡 Tip: Use this for organizing documents, content categorization, and information discovery")
