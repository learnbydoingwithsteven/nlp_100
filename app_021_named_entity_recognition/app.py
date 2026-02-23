"""
NLP App 021: Named Entity Recognition
Real-world use case: Person/Organization/Location extraction
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

st.set_page_config(
    page_title="Named Entity Recognition",
    page_icon="🔤",
    layout="wide"
)

st.title("🏷️ Named Entity Recognition")
st.markdown("""
**Real-world Use Case**: Extract named entities from text
- Identify people, organizations, locations
- Extract dates, money, percentages
- Information extraction
- Document analysis
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
st.sidebar.markdown("---")
st.sidebar.markdown("**Entity Types:**")
st.sidebar.markdown("""
- 👤 PERSON - People names
- 🏢 ORG - Organizations
- 📍 GPE - Countries, cities
- 📅 DATE - Dates
- 💰 MONEY - Monetary values
- 📊 PERCENT - Percentages
""")

# Load spaCy model
@st.cache_resource
def load_spacy_model():
    """Load spaCy model"""
    try:
        import spacy
        return spacy.load("en_core_web_sm")
    except:
        st.error("⚠️ spaCy model not found. Run: python -m spacy download en_core_web_sm")
        return None

nlp = load_spacy_model()

def extract_entities(text):
    """Extract named entities using spaCy"""
    if nlp is None:
        return {
            'text': text,
            'entities': [],
            'entity_counts': {},
            'total_entities': 0
        }
    
    doc = nlp(text)
    
    # Extract entities
    entities = []
    for ent in doc.ents:
        entities.append({
            'text': ent.text,
            'label': ent.label_,
            'start': ent.start_char,
            'end': ent.end_char
        })
    
    # Count by type
    entity_counts = Counter([ent['label'] for ent in entities])
    
    return {
        'text': text,
        'entities': entities,
        'entity_counts': dict(entity_counts),
        'total_entities': len(entities),
        'unique_types': len(entity_counts)
    }

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Processing")
    
    user_input = st.text_area(
        "Enter text to process:",
        height=150,
        placeholder="Type or paste your text here..."
    )
    
    if st.button("🔍 Extract Entities", type="primary"):
        if user_input.strip():
            with st.spinner("Extracting entities..."):
                result = extract_entities(user_input)
            
            st.success("✅ Extraction Complete!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Entities", result['total_entities'])
            with col2:
                st.metric("Entity Types", result['unique_types'])
            with col3:
                st.metric("Text Length", len(result['text']))
            
            if result['entities']:
                # Entity distribution
                st.subheader("📊 Entity Distribution")
                if result['entity_counts']:
                    counts_df = pd.DataFrame(list(result['entity_counts'].items()), 
                                            columns=['Type', 'Count'])
                    fig = px.bar(counts_df, x='Type', y='Count',
                                title='Entity Types Found',
                                color='Count', color_continuous_scale='Viridis')
                    st.plotly_chart(fig, use_container_width=True)
                
                # Entities by type
                st.subheader("🏷️ Extracted Entities")
                entities_by_type = {}
                for ent in result['entities']:
                    label = ent['label']
                    if label not in entities_by_type:
                        entities_by_type[label] = []
                    entities_by_type[label].append(ent['text'])
                
                for label, texts in sorted(entities_by_type.items()):
                    with st.expander(f"{label} ({len(texts)})"):
                        st.write(", ".join(set(texts)))
            else:
                st.info("No entities found in the text.")
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
            if st.button("🔍 Extract All", type="primary"):
                results = []
                progress_bar = st.progress(0)
                
                for idx, text in enumerate(df['text']):
                    result = extract_entities(str(text))
                    results.append({
                        'text': result['text'][:60] + '...',
                        'total_entities': result['total_entities'],
                        'entity_types': result['unique_types']
                    })
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Processed {len(results_df)} texts!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Texts", len(results_df))
                with col2:
                    total_ents = results_df['total_entities'].sum()
                    st.metric("Total Entities", total_ents)
                with col3:
                    avg_ents = results_df['total_entities'].mean()
                    st.metric("Avg Entities/Text", f"{avg_ents:.1f}")
                
                fig = px.histogram(results_df, x='total_entities',
                                  title='Entity Count Distribution')
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
        "Apple Inc. was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in Cupertino, California on April 1, 1976.",
        "Microsoft CEO Satya Nadella announced new AI features at the conference in Seattle last week, with shares rising 5.2%.",
        "The United Nations held a meeting in New York on Monday to discuss climate change initiatives proposed by the European Union."
    ]
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        all_entities = []
        
        for text in samples:
            result = extract_entities(text)
            results.append({
                'text': text[:50] + '...',
                'entities': result['total_entities']
            })
            all_entities.extend(result['entities'])
        
        results_df = pd.DataFrame(results)
        st.success("✅ Complete!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Entities", len(all_entities))
        with col2:
            types = len(set(e['label'] for e in all_entities))
            st.metric("Entity Types", types)
        
        # Show entities by type
        st.subheader("📊 Entities Found")
        entity_types = {}
        for ent in all_entities:
            label = ent['label']
            if label not in entity_types:
                entity_types[label] = []
            entity_types[label].append(ent['text'])
        
        for label, texts in sorted(entity_types.items()):
            st.write(f"**{label}**: {', '.join(set(texts))}")
        
        # Distribution
        type_counts = Counter(e['label'] for e in all_entities)
        fig = px.pie(values=list(type_counts.values()), names=list(type_counts.keys()),
                    title='Entity Type Distribution')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Named Entity Recognition - Extract people, organizations, locations, dates, and more")
st.caption("💡 Powered by spaCy. Extracts PERSON, ORG, GPE, DATE, MONEY, PERCENT, and other entity types")
