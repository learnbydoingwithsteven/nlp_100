"""
NLP App 001: Sentiment Analysis
Real-world use case: Product review sentiment classification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Sentiment Analysis",
    page_icon="😊",
    layout="wide"
)

st.title("😊 Sentiment Analysis")
st.markdown("""
**Real-world Use Case**: Product review sentiment classification
- Analyze sentiment polarity (positive, negative, neutral)
- Extract emotional tone and subjectivity
- Visualize sentiment patterns comprehensively
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
analyzer_choice = st.sidebar.selectbox("Analyzer", ["TextBlob", "VADER", "Both"])

# Initialize VADER
vader_analyzer = SentimentIntensityAnalyzer()

# Main processing function
def analyze_sentiment(text):
    """Perform comprehensive sentiment analysis"""
    results = {
        "text": text,
        "length": len(text),
        "word_count": len(text.split())
    }
    
    # TextBlob analysis
    blob = TextBlob(text)
    results["textblob_polarity"] = blob.sentiment.polarity
    results["textblob_subjectivity"] = blob.sentiment.subjectivity
    
    if blob.sentiment.polarity > 0.1:
        results["textblob_sentiment"] = "Positive"
    elif blob.sentiment.polarity < -0.1:
        results["textblob_sentiment"] = "Negative"
    else:
        results["textblob_sentiment"] = "Neutral"
    
    # VADER analysis
    vader_scores = vader_analyzer.polarity_scores(text)
    results["vader_positive"] = vader_scores['pos']
    results["vader_negative"] = vader_scores['neg']
    results["vader_neutral"] = vader_scores['neu']
    results["vader_compound"] = vader_scores['compound']
    
    if vader_scores['compound'] >= 0.05:
        results["vader_sentiment"] = "Positive"
    elif vader_scores['compound'] <= -0.05:
        results["vader_sentiment"] = "Negative"
    else:
        results["vader_sentiment"] = "Neutral"
    
    return results

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Processing")
    
    user_input = st.text_area(
        "Enter text to process:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    if st.button("🔍 Analyze Sentiment", type="primary"):
        if user_input.strip():
            with st.spinner("Analyzing sentiment..."):
                result = analyze_sentiment(user_input)
            
            st.success("✅ Sentiment Analysis Complete!")
            
            # Display overall sentiment
            col1, col2, col3 = st.columns(3)
            with col1:
                sentiment = result["textblob_sentiment"]
                emoji = "😊" if sentiment == "Positive" else "😢" if sentiment == "Negative" else "😐"
                st.metric(f"TextBlob Sentiment {emoji}", sentiment)
            with col2:
                sentiment = result["vader_sentiment"]
                emoji = "😊" if sentiment == "Positive" else "😢" if sentiment == "Negative" else "😐"
                st.metric(f"VADER Sentiment {emoji}", sentiment)
            with col3:
                st.metric("Word Count", result["word_count"])
            
            # Detailed scores
            st.subheader("📊 Detailed Sentiment Scores")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**TextBlob Scores**")
                st.metric("Polarity", f"{result['textblob_polarity']:.3f}", help="Range: -1 (negative) to +1 (positive)")
                st.metric("Subjectivity", f"{result['textblob_subjectivity']:.3f}", help="Range: 0 (objective) to 1 (subjective)")
                
                # Polarity gauge
                fig_polarity = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=result['textblob_polarity'],
                    title={'text': "Polarity"},
                    gauge={
                        'axis': {'range': [-1, 1]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [-1, -0.1], 'color': "lightcoral"},
                            {'range': [-0.1, 0.1], 'color': "lightgray"},
                            {'range': [0.1, 1], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 0
                        }
                    }
                ))
                st.plotly_chart(fig_polarity, use_container_width=True)
            
            with col2:
                st.markdown("**VADER Scores**")
                st.metric("Compound", f"{result['vader_compound']:.3f}", help="Range: -1 (negative) to +1 (positive)")
                st.metric("Positive", f"{result['vader_positive']:.3f}")
                st.metric("Negative", f"{result['vader_negative']:.3f}")
                st.metric("Neutral", f"{result['vader_neutral']:.3f}")
                
                # VADER component breakdown
                fig_vader = px.bar(
                    x=['Positive', 'Negative', 'Neutral'],
                    y=[result['vader_positive'], result['vader_negative'], result['vader_neutral']],
                    title='VADER Score Breakdown',
                    color=['Positive', 'Negative', 'Neutral'],
                    color_discrete_map={'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}
                )
                st.plotly_chart(fig_vader, use_container_width=True)
            
            # Word cloud
            st.subheader("☁️ Word Cloud")
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(user_input)
            fig_wc, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig_wc)
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
                    result = analyze_sentiment(str(text))
                    results.append(result)
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Analyzed {len(results_df)} texts!")
                
                # Summary stats
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Processed", len(results_df))
                with col2:
                    positive_count = (results_df['textblob_sentiment'] == 'Positive').sum()
                    st.metric("Positive", positive_count)
                with col3:
                    negative_count = (results_df['textblob_sentiment'] == 'Negative').sum()
                    st.metric("Negative", negative_count)
                with col4:
                    neutral_count = (results_df['textblob_sentiment'] == 'Neutral').sum()
                    st.metric("Neutral", neutral_count)
                
                # Sentiment distribution
                st.subheader("📊 Sentiment Distribution")
                fig_dist = px.pie(
                    names=['Positive', 'Negative', 'Neutral'],
                    values=[positive_count, negative_count, neutral_count],
                    color=['Positive', 'Negative', 'Neutral'],
                    color_discrete_map={'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}
                )
                st.plotly_chart(fig_dist, use_container_width=True)
                
                # Polarity distribution
                fig_polarity = px.histogram(
                    results_df, 
                    x='textblob_polarity', 
                    title='Polarity Score Distribution',
                    nbins=30
                )
                st.plotly_chart(fig_polarity, use_container_width=True)
                
                # Results table
                st.subheader("📋 Detailed Results")
                st.dataframe(results_df, use_container_width=True)
                
                # Download
                csv = results_df.to_csv(index=False)
                st.download_button("📥 Download Results", csv, "sentiment_results.csv", "text/csv")
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file to perform batch processing")

# Mode: Demo
else:
    st.header("🎯 Demo Mode")
    
    sample_texts = [
        "This product is absolutely amazing! Best purchase I've ever made. Highly recommend!",
        "Terrible experience. Product broke after one week. Complete waste of money.",
        "It's okay, nothing special. Does what it's supposed to do.",
        "I love it! Great quality and fast shipping. Will buy again!",
        "Disappointed with the quality. Not worth the price at all."
    ]
    
    st.write(f"Analyzing {len(sample_texts)} sample product reviews...")
    
    # Display sample texts
    with st.expander("👁️ View Sample Reviews"):
        for i, text in enumerate(sample_texts, 1):
            st.write(f"{i}. {text}")
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        with st.spinner("Analyzing sentiment..."):
            for text in sample_texts:
                result = analyze_sentiment(text)
                results.append(result)
        
        results_df = pd.DataFrame(results)
        
        st.success("✅ Demo Complete!")
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            positive_count = (results_df['textblob_sentiment'] == 'Positive').sum()
            st.metric("Positive Reviews", positive_count, delta=f"{positive_count/len(results_df)*100:.0f}%")
        with col2:
            negative_count = (results_df['textblob_sentiment'] == 'Negative').sum()
            st.metric("Negative Reviews", negative_count, delta=f"{negative_count/len(results_df)*100:.0f}%")
        with col3:
            neutral_count = (results_df['textblob_sentiment'] == 'Neutral').sum()
            st.metric("Neutral Reviews", neutral_count, delta=f"{neutral_count/len(results_df)*100:.0f}%")
        
        # Display results with emojis
        st.subheader("📋 Analysis Results")
        for idx, row in results_df.iterrows():
            emoji = "😊" if row['textblob_sentiment'] == "Positive" else "😢" if row['textblob_sentiment'] == "Negative" else "😐"
            with st.expander(f"{emoji} Review {idx+1} - {row['textblob_sentiment']}"):
                st.write(f"**Text**: {row['text']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("TextBlob Polarity", f"{row['textblob_polarity']:.3f}")
                    st.metric("Subjectivity", f"{row['textblob_subjectivity']:.3f}")
                with col2:
                    st.metric("VADER Compound", f"{row['vader_compound']:.3f}")
                    st.metric("Sentiment", row['vader_sentiment'])
        
        # Visualization
        st.subheader("📊 Sentiment Distribution")
        fig = px.pie(
            names=['Positive', 'Negative', 'Neutral'],
            values=[positive_count, negative_count, neutral_count],
            title='Overall Sentiment Distribution',
            color=['Positive', 'Negative', 'Neutral'],
            color_discrete_map={'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Polarity comparison
        fig_compare = px.scatter(
            results_df,
            x='textblob_polarity',
            y='vader_compound',
            title='TextBlob vs VADER Polarity',
            labels={'textblob_polarity': 'TextBlob Polarity', 'vader_compound': 'VADER Compound'},
            hover_data=['text']
        )
        st.plotly_chart(fig_compare, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Sentiment Analysis - Product review sentiment classification using TextBlob and VADER")
