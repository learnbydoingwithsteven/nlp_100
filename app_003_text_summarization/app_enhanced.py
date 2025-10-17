"""
NLP App 003: Text Summarization (Enhanced)
Real-world use case: Automatic document summarization
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import nltk
from collections import Counter
import re
import time

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

st.set_page_config(page_title="Text Summarization", page_icon="📄", layout="wide")

st.title("📄 Advanced Text Summarization")
st.markdown("""
**Real-world Use Case**: Automatically generate concise summaries of long documents, articles, or reports.
- Multiple summarization algorithms (LSA, Luhn, TextRank, LexRank)
- Adjustable summary length
- Compression ratio analysis
- Keyword extraction and visualization
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Document", "Batch Summarization", "Compare Algorithms"])
algorithm = st.sidebar.selectbox(
    "Summarization Algorithm",
    ["LSA", "Luhn", "TextRank", "LexRank"]
)
summary_length = st.sidebar.slider("Summary Length (sentences)", 1, 10, 3)

# Sample documents
sample_documents = {
    "News Article": """
    Artificial intelligence is transforming the way we live and work. Machine learning algorithms are now 
    being used in healthcare to diagnose diseases, in finance to detect fraud, and in transportation to 
    power self-driving cars. The technology has advanced rapidly in recent years, thanks to improvements 
    in computing power and the availability of large datasets. However, concerns about AI ethics, bias, 
    and job displacement remain significant challenges. Experts predict that AI will continue to evolve 
    and become even more integrated into our daily lives. Companies are investing billions of dollars 
    in AI research and development. Governments are also developing regulations to ensure AI is used 
    responsibly. The future of AI holds both tremendous promise and important questions that society 
    must address. Education systems are adapting to prepare students for an AI-driven world. Many 
    universities now offer specialized AI and machine learning programs.
    """,
    "Research Abstract": """
    This study investigates the effects of climate change on marine ecosystems in the Pacific Ocean. 
    We collected data from 50 monitoring stations over a period of 10 years, measuring water temperature, 
    pH levels, and biodiversity indicators. Our findings reveal a significant correlation between rising 
    ocean temperatures and declining fish populations. Coral bleaching events have increased by 40% 
    during the study period. The research also identifies several species that are particularly vulnerable 
    to environmental changes. We propose a series of conservation measures to protect marine biodiversity. 
    These include establishing marine protected areas, reducing carbon emissions, and implementing 
    sustainable fishing practices. The study contributes to our understanding of climate change impacts 
    on ocean ecosystems and provides actionable recommendations for policymakers. Future research should 
    focus on long-term monitoring and the development of adaptive management strategies.
    """,
    "Business Report": """
    The company achieved record revenue of $5.2 billion in Q4 2023, representing a 25% increase 
    year-over-year. Strong performance was driven by growth in cloud services, which now account for 
    45% of total revenue. Customer acquisition increased by 30%, with particularly strong growth in 
    the enterprise segment. Operating margins improved to 22%, up from 18% in the previous quarter. 
    The company launched three new products during the quarter, all of which exceeded initial sales 
    projections. International markets contributed 40% of revenue, with Asia-Pacific showing the 
    strongest growth at 35%. The company expanded its workforce by 500 employees, focusing on 
    engineering and customer support roles. Looking ahead, management expects continued growth in 
    Q1 2024, with projected revenue of $5.5 billion. Key strategic priorities include expanding 
    AI capabilities, entering new geographic markets, and enhancing customer experience. The board 
    approved a $500 million share buyback program and increased the quarterly dividend by 10%.
    """
}

def get_summarizer(algorithm_name):
    """Get summarizer based on algorithm name"""
    if algorithm_name == "LSA":
        return LsaSummarizer()
    elif algorithm_name == "Luhn":
        return LuhnSummarizer()
    elif algorithm_name == "TextRank":
        return TextRankSummarizer()
    else:  # LexRank
        return LexRankSummarizer()

def summarize_text(text, algorithm_name, num_sentences):
    """Summarize text using specified algorithm"""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = get_summarizer(algorithm_name)
    
    summary_sentences = summarizer(parser.document, num_sentences)
    summary = " ".join([str(sentence) for sentence in summary_sentences])
    
    return summary

def extract_keywords(text, top_n=10):
    """Extract top keywords from text"""
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    stop_words = {'that', 'this', 'with', 'from', 'have', 'been', 'were', 'will', 'would', 'could', 'should'}
    filtered_words = [w for w in words if w not in stop_words]
    return Counter(filtered_words).most_common(top_n)

def calculate_metrics(original, summary):
    """Calculate summarization metrics"""
    orig_words = len(original.split())
    summ_words = len(summary.split())
    orig_chars = len(original)
    summ_chars = len(summary)
    
    compression_ratio = (1 - summ_chars / orig_chars) * 100 if orig_chars > 0 else 0
    
    return {
        "original_words": orig_words,
        "summary_words": summ_words,
        "original_chars": orig_chars,
        "summary_chars": summ_chars,
        "compression_ratio": compression_ratio,
        "word_reduction": orig_words - summ_words
    }

# Mode: Single Document
if mode == "Single Document":
    st.header("📝 Single Document Summarization")
    
    # Sample document selector
    use_sample = st.checkbox("Use sample document")
    
    if use_sample:
        sample_choice = st.selectbox("Select sample document", list(sample_documents.keys()))
        user_text = sample_documents[sample_choice]
        st.text_area("Document text:", value=user_text, height=200, disabled=True)
    else:
        user_text = st.text_area(
            "Enter document to summarize:",
            height=200,
            placeholder="Paste your document here..."
        )
    
    if st.button("📊 Generate Summary", type="primary"):
        if user_text.strip():
            with st.spinner(f"Generating summary using {algorithm}..."):
                summary = summarize_text(user_text, algorithm, summary_length)
                metrics = calculate_metrics(user_text, summary)
                keywords = extract_keywords(user_text)
                time.sleep(0.5)
            
            st.success("Summary Generated!")
            
            # Display summary
            st.subheader("📋 Summary")
            st.info(summary)
            
            # Metrics
            st.subheader("📊 Summarization Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Original Words", metrics["original_words"])
            with col2:
                st.metric("Summary Words", metrics["summary_words"])
            with col3:
                st.metric("Compression", f"{metrics['compression_ratio']:.1f}%")
            with col4:
                st.metric("Words Reduced", metrics["word_reduction"])
            
            # Visualization
            col1, col2 = st.columns(2)
            
            with col1:
                # Length comparison
                fig = go.Figure(data=[
                    go.Bar(name='Original', x=['Words', 'Characters'], 
                          y=[metrics['original_words'], metrics['original_chars']],
                          marker_color='lightblue'),
                    go.Bar(name='Summary', x=['Words', 'Characters'], 
                          y=[metrics['summary_words'], metrics['summary_chars']],
                          marker_color='darkblue')
                ])
                fig.update_layout(title='Length Comparison', barmode='group')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Compression gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=metrics['compression_ratio'],
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Compression Ratio (%)"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "darkgreen"},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgray"},
                            {'range': [30, 60], 'color': "lightgreen"},
                            {'range': [60, 100], 'color': "green"}
                        ]
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            # Keywords
            st.subheader("🔑 Top Keywords")
            if keywords:
                keyword_df = pd.DataFrame(keywords, columns=['Keyword', 'Frequency'])
                fig = px.bar(
                    keyword_df,
                    x='Frequency',
                    y='Keyword',
                    orientation='h',
                    title='Most Frequent Keywords',
                    color='Frequency',
                    color_continuous_scale='viridis'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Side-by-side comparison
            st.subheader("📄 Side-by-Side Comparison")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Original Text**")
                st.text_area("", value=user_text, height=300, disabled=True, label_visibility="collapsed")
            
            with col2:
                st.markdown("**Summary**")
                st.text_area("", value=summary, height=300, disabled=True, label_visibility="collapsed")
        else:
            st.warning("Please enter text to summarize.")

# Mode: Batch Summarization
elif mode == "Batch Summarization":
    st.header("📚 Batch Summarization")
    
    uploaded_file = st.file_uploader("Upload CSV with 'text' column", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} documents")
        
        if 'text' in df.columns:
            if st.button("📊 Summarize All", type="primary"):
                results = []
                progress_bar = st.progress(0)
                
                for idx, text in enumerate(df['text']):
                    try:
                        summary = summarize_text(str(text), algorithm, summary_length)
                        metrics = calculate_metrics(str(text), summary)
                        
                        results.append({
                            'original': str(text)[:100] + "...",
                            'summary': summary,
                            'original_words': metrics['original_words'],
                            'summary_words': metrics['summary_words'],
                            'compression_ratio': metrics['compression_ratio']
                        })
                    except:
                        results.append({
                            'original': str(text)[:100] + "...",
                            'summary': "Error generating summary",
                            'original_words': 0,
                            'summary_words': 0,
                            'compression_ratio': 0
                        })
                    
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                
                st.success(f"Summarized {len(results_df)} documents!")
                
                # Summary statistics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Documents", len(results_df))
                with col2:
                    avg_compression = results_df['compression_ratio'].mean()
                    st.metric("Avg Compression", f"{avg_compression:.1f}%")
                with col3:
                    total_words_saved = results_df['original_words'].sum() - results_df['summary_words'].sum()
                    st.metric("Total Words Saved", total_words_saved)
                with col4:
                    avg_summary_length = results_df['summary_words'].mean()
                    st.metric("Avg Summary Length", f"{avg_summary_length:.0f}")
                
                # Visualizations
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.histogram(
                        results_df,
                        x='compression_ratio',
                        nbins=20,
                        title='Compression Ratio Distribution',
                        labels={'compression_ratio': 'Compression Ratio (%)'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.scatter(
                        results_df,
                        x='original_words',
                        y='summary_words',
                        title='Original vs Summary Length',
                        labels={'original_words': 'Original Words', 'summary_words': 'Summary Words'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Results table
                st.subheader("📋 Summarization Results")
                st.dataframe(results_df, use_container_width=True)
                
                # Download
                csv = results_df.to_csv(index=False)
                st.download_button("📥 Download Results", csv, "summarization_results.csv", "text/csv")
        else:
            st.error("CSV must contain 'text' column")
    else:
        st.info("Upload a CSV file to perform batch summarization")

# Mode: Compare Algorithms
else:
    st.header("🔬 Algorithm Comparison")
    
    sample_choice = st.selectbox("Select sample document", list(sample_documents.keys()))
    user_text = sample_documents[sample_choice]
    
    st.text_area("Document:", value=user_text, height=150, disabled=True)
    
    if st.button("🔍 Compare All Algorithms", type="primary"):
        with st.spinner("Comparing algorithms..."):
            algorithms = ["LSA", "Luhn", "TextRank", "LexRank"]
            results = []
            
            for algo in algorithms:
                try:
                    summary = summarize_text(user_text, algo, summary_length)
                    metrics = calculate_metrics(user_text, summary)
                    
                    results.append({
                        'algorithm': algo,
                        'summary': summary,
                        'summary_words': metrics['summary_words'],
                        'compression_ratio': metrics['compression_ratio']
                    })
                except Exception as e:
                    results.append({
                        'algorithm': algo,
                        'summary': f"Error: {str(e)}",
                        'summary_words': 0,
                        'compression_ratio': 0
                    })
            
            time.sleep(0.5)
        
        st.success("Comparison Complete!")
        
        # Metrics comparison
        st.subheader("📊 Algorithm Performance")
        
        results_df = pd.DataFrame(results)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                results_df,
                x='algorithm',
                y='compression_ratio',
                title='Compression Ratio by Algorithm',
                color='compression_ratio',
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                results_df,
                x='algorithm',
                y='summary_words',
                title='Summary Length by Algorithm',
                color='summary_words',
                color_continuous_scale='blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Display summaries
        st.subheader("📄 Summaries by Algorithm")
        
        for result in results:
            with st.expander(f"**{result['algorithm']}** (Compression: {result['compression_ratio']:.1f}%)"):
                st.write(result['summary'])

st.markdown("---")
st.markdown("""
**About**: This summarization tool uses multiple algorithms:
- **LSA**: Latent Semantic Analysis
- **Luhn**: Frequency-based summarization
- **TextRank**: Graph-based ranking
- **LexRank**: Eigenvector centrality
""")
