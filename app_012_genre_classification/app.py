"""
NLP App 012: Genre Classification
Real-world use case: Literary genre identification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Genre Classification",
    page_icon="🔤",
    layout="wide"
)

st.title("📚 Genre Classification")
st.markdown("""
**Real-world Use Case**: Literary and content genre identification
- Automatic genre detection for books and articles
- Multi-genre classification
- Keyword-based pattern matching
- Content categorization
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
min_confidence = st.sidebar.slider("Min Confidence", 0.0, 1.0, 0.1, 0.05)
st.sidebar.markdown("---")
st.sidebar.markdown("**Genres Supported:**")
st.sidebar.markdown("""
- 👽 Sci-Fi
- 🔪 Mystery/Thriller
- ❤️ Romance
- 💉 Horror
- ⚔️ Fantasy
- 📖 Non-Fiction
""")

# Genre keywords
GENRE_KEYWORDS = {
    'sci-fi': ['space', 'alien', 'robot', 'future', 'technology', 'spacecraft', 'galaxy', 'planet', 'laser', 'cybernetic', 'android', 'starship', 'quantum', 'teleport', 'hologram'],
    'mystery': ['detective', 'murder', 'clue', 'suspect', 'investigation', 'crime', 'mystery', 'solve', 'evidence', 'alibi', 'witness', 'victim', 'thriller', 'conspiracy', 'secret'],
    'romance': ['love', 'heart', 'kiss', 'romance', 'relationship', 'passion', 'wedding', 'dating', 'embrace', 'affection', 'beloved', 'soulmate', 'desire', 'attraction', 'chemistry'],
    'horror': ['fear', 'terror', 'scream', 'haunted', 'ghost', 'blood', 'monster', 'nightmare', 'demon', 'vampire', 'zombie', 'supernatural', 'creepy', 'sinister', 'possessed'],
    'fantasy': ['magic', 'wizard', 'dragon', 'kingdom', 'quest', 'sword', 'spell', 'enchanted', 'castle', 'elf', 'dwarf', 'prophecy', 'sorcerer', 'mythical', 'legendary'],
    'non-fiction': ['research', 'study', 'analysis', 'data', 'fact', 'evidence', 'history', 'theory', 'scientific', 'documented', 'biography', 'according', 'reported', 'statistics', 'published'],
    'adventure': ['journey', 'explore', 'expedition', 'treasure', 'quest', 'adventure', 'voyage', 'discovery', 'wilderness', 'survival'],
    'drama': ['conflict', 'tragedy', 'emotional', 'struggle', 'family', 'society', 'relationship', 'crisis', 'tension']
}

def classify_genre(text, min_confidence=0.1):
    """Classify text into literary genres"""
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words)
    
    # Score each genre
    genre_scores = {}
    genre_keywords_found = {}
    
    for genre, keywords in GENRE_KEYWORDS.items():
        score = 0
        found = []
        for keyword in keywords:
            if keyword in text_lower:
                count = text_lower.count(keyword)
                score += count
                found.extend([keyword] * count)
        
        # Normalize by text length
        confidence = score / max(word_count, 1) if word_count > 0 else 0
        
        if confidence >= min_confidence:
            genre_scores[genre] = confidence
            genre_keywords_found[genre] = found
    
    # Sort by score
    sorted_genres = sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Primary and secondary genres
    primary_genre = sorted_genres[0][0] if sorted_genres else 'unclassified'
    primary_confidence = sorted_genres[0][1] if sorted_genres else 0.0
    
    secondary_genre = sorted_genres[1][0] if len(sorted_genres) > 1 else None
    secondary_confidence = sorted_genres[1][1] if len(sorted_genres) > 1 else 0.0
    
    # Multi-genre check
    is_multi_genre = len(sorted_genres) > 1 and sorted_genres[1][1] >= min_confidence * 2
    
    return {
        'text': text,
        'primary_genre': primary_genre,
        'primary_confidence': primary_confidence,
        'secondary_genre': secondary_genre,
        'secondary_confidence': secondary_confidence,
        'all_genres': sorted_genres,
        'is_multi_genre': is_multi_genre,
        'genre_keywords_found': genre_keywords_found,
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
    
    if st.button("🔍 Classify Genre", type="primary"):
        if user_input.strip():
            with st.spinner("Classifying..."):
                result = classify_genre(user_input, min_confidence)
            
            st.success("✅ Classification Complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Primary Genre", result['primary_genre'].title())
            with col2:
                st.metric("Confidence", f"{result['primary_confidence']:.1%}")
            with col3:
                multi = "Yes" if result['is_multi_genre'] else "No"
                st.metric("Multi-Genre", multi)
            
            if result['secondary_genre']:
                st.info(f"**Secondary**: {result['secondary_genre'].title()} ({result['secondary_confidence']:.1%})")
            
            if result['all_genres']:
                st.subheader("📊 Genre Scores")
                genres = [g[0] for g in result['all_genres']]
                scores = [g[1] for g in result['all_genres']]
                fig = px.bar(x=genres, y=scores, title="Genre Confidence Scores",
                            labels={'x': 'Genre', 'y': 'Confidence'},
                            color=scores, color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("🔍 Detected Keywords")
            for genre, keywords in result['genre_keywords_found'].items():
                if keywords:
                    st.write(f"**{genre.title()}**: {', '.join(set(keywords)[:10])}")
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
                    result = classify_genre(str(text), min_confidence)
                    simple_result = {
                        'text': result['text'][:60] + '...',
                        'primary_genre': result['primary_genre'],
                        'confidence': result['primary_confidence']
                    }
                    results.append(simple_result)
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Classified {len(results_df)} texts!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total", len(results_df))
                with col2:
                    most_common = results_df['primary_genre'].mode()[0] if len(results_df) > 0 else "N/A"
                    st.metric("Most Common", most_common.title())
                with col3:
                    unique = results_df['primary_genre'].nunique()
                    st.metric("Unique Genres", unique)
                
                genre_counts = results_df['primary_genre'].value_counts()
                fig = px.bar(x=genre_counts.index, y=genre_counts.values,
                            title="Genre Distribution",
                            labels={'x': 'Genre', 'y': 'Count'})
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
        "The spaceship landed on the distant planet. Aliens emerged from the craft with advanced technology.",
        "The detective examined the crime scene carefully, looking for clues about the mysterious murder.",
        "Their eyes met across the room, and she felt her heart skip a beat. This was love at first sight.",
        "The haunted house creaked in the darkness. Ghosts wandered the halls, terrifying anyone who entered.",
        "The wizard cast a powerful spell, summoning a dragon to defend the enchanted kingdom.",
    ]
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        for text in samples:
            result = classify_genre(text, min_confidence)
            results.append({
                'text': text[:50] + '...',
                'genre': result['primary_genre'],
                'confidence': result['primary_confidence']
            })
        
        results_df = pd.DataFrame(results)
        st.success("✅ Complete!")
        
        for idx, row in results_df.iterrows():
            st.info(f"**{row['genre'].title()}** ({row['confidence']:.1%}): {row['text']}")
        
        fig = px.bar(results_df, x='genre', y='confidence',
                     title='Genre Confidence',
                     color='confidence', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Genre Classification - Literary and content genre identification")
st.caption("💡 Supports 8 genres: Sci-Fi, Mystery, Romance, Horror, Fantasy, Non-Fiction, Adventure, Drama")
