"""
NLP App 007: Intent Classification
Real-world use case: Chatbot intent recognition
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Intent Classification",
    page_icon="🔤",
    layout="wide"
)

st.title("🤖 Intent Classification")
st.markdown("""
**Real-world Use Case**: Chatbot and virtual assistant intent recognition
- Classify user queries into actionable intents
- Support 10 common intents: Greeting, Question, Complaint, Request, Feedback, Booking, Cancel, Help, Thanks, Goodbye
- Confidence scoring and entity detection
- Real-time intent routing for chatbots
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
st.sidebar.markdown("---")
st.sidebar.markdown("**Supported Intents:**")
st.sidebar.markdown("""
- 👋 Greeting
- ❓ Question
- 😠 Complaint
- 📝 Request
- 💬 Feedback
- 📅 Booking
- ❌ Cancel
- 🆘 Help
- 🙏 Thanks
- 👋 Goodbye
""")

# Intent patterns and keywords
INTENT_PATTERNS = {
    'greeting': {
        'patterns': [r'\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b'],
        'keywords': ['hi', 'hello', 'hey', 'greetings', 'morning', 'afternoon', 'evening'],
        'icon': '👋'
    },
    'question': {
        'patterns': [r'\b(what|when|where|why|how|who|which|can you|could you|is it|do you)\b'],
        'keywords': ['what', 'when', 'where', 'why', 'how', 'who', 'which', '?'],
        'icon': '❓'
    },
    'complaint': {
        'patterns': [r'\b(complain|complaint|problem|issue|bad|terrible|awful|worst|disappointed|not working|broken)\b'],
        'keywords': ['complain', 'problem', 'issue', 'bad', 'terrible', 'awful', 'worst', 'disappointed', 'not working'],
        'icon': '😠'
    },
    'request': {
        'patterns': [r'\b(please|need|want|would like|can i|could i|may i|request)\b'],
        'keywords': ['please', 'need', 'want', 'would like', 'can i', 'could i', 'request'],
        'icon': '📝'
    },
    'feedback': {
        'patterns': [r'\b(feedback|suggest|suggestion|recommend|improve|better|think that)\b'],
        'keywords': ['feedback', 'suggest', 'suggestion', 'recommend', 'improve', 'better'],
        'icon': '💬'
    },
    'booking': {
        'patterns': [r'\b(book|reserve|appointment|schedule|reservation)\b'],
        'keywords': ['book', 'reserve', 'appointment', 'schedule', 'reservation'],
        'icon': '📅'
    },
    'cancel': {
        'patterns': [r'\b(cancel|cancellation|refund|undo|remove)\b'],
        'keywords': ['cancel', 'cancellation', 'refund', 'undo', 'remove'],
        'icon': '❌'
    },
    'help': {
        'patterns': [r'\b(help|assist|support|guide|stuck|confused)\b'],
        'keywords': ['help', 'assist', 'support', 'guide', 'stuck', 'confused'],
        'icon': '🆘'
    },
    'thanks': {
        'patterns': [r'\b(thank|thanks|appreciate|grateful)\b'],
        'keywords': ['thank', 'thanks', 'appreciate', 'grateful'],
        'icon': '🙏'
    },
    'goodbye': {
        'patterns': [r'\b(bye|goodbye|see you|later|farewell)\b'],
        'keywords': ['bye', 'goodbye', 'see you', 'later', 'farewell'],
        'icon': '👋'
    }
}

def classify_intent(text):
    """Classify user intent using pattern and keyword matching"""
    text_lower = text.lower()
    word_count = len(text.split())
    
    # Calculate scores for each intent
    scores = {}
    detected_features = {}
    
    for intent, config in INTENT_PATTERNS.items():
        score = 0.0
        features = []
        
        # Check patterns
        for pattern in config['patterns']:
            matches = re.findall(pattern, text_lower)
            if matches:
                score += 0.3 * len(matches)
                features.extend(matches)
        
        # Check keywords
        for keyword in config['keywords']:
            if keyword in text_lower:
                score += 0.2
                features.append(keyword)
        
        scores[intent] = min(score, 1.0)
        detected_features[intent] = list(set(features))[:5]  # Limit to 5
    
    # Find primary intent
    if max(scores.values()) > 0:
        primary_intent = max(scores, key=scores.get)
        confidence = scores[primary_intent]
    else:
        primary_intent = "unknown"
        confidence = 0.0
    
    # Find secondary intent (if exists)
    sorted_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    secondary_intent = sorted_intents[1][0] if len(sorted_intents) > 1 and sorted_intents[1][1] > 0.2 else None
    
    # Determine complexity
    intent_count = sum(1 for score in scores.values() if score > 0.2)
    if intent_count >= 3:
        complexity = "Complex"
    elif intent_count == 2:
        complexity = "Moderate"
    else:
        complexity = "Simple"
    
    return {
        'text': text,
        'primary_intent': primary_intent,
        'confidence': confidence,
        'secondary_intent': secondary_intent,
        'complexity': complexity,
        'scores': scores,
        'detected_features': detected_features,
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
    
    if st.button("🔍 Classify Intent", type="primary"):
        if user_input.strip():
            with st.spinner("Classifying..."):
                result = classify_intent(user_input)
            
            st.success("✅ Classification Complete!")
            
            # Main metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                icon = INTENT_PATTERNS.get(result['primary_intent'], {}).get('icon', '🤖')
                st.metric("Primary Intent", f"{icon} {result['primary_intent'].title()}")
            with col2:
                st.metric("Confidence", f"{result['confidence']:.1%}")
            with col3:
                st.metric("Complexity", result['complexity'])
            with col4:
                secondary = result['secondary_intent'].title() if result['secondary_intent'] else "None"
                st.metric("Secondary Intent", secondary)
            
            # Intent scores
            st.subheader("📊 Intent Score Distribution")
            scores_df = pd.DataFrame(list(result['scores'].items()), columns=['Intent', 'Score'])
            scores_df = scores_df.sort_values('Score', ascending=False)
            
            fig = px.bar(scores_df, x='Intent', y='Score',
                        title="All Intent Scores",
                        color='Score', color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
            
            # Detected features
            st.subheader("🔍 Detected Features")
            for intent, features in result['detected_features'].items():
                if features and result['scores'][intent] > 0:
                    icon = INTENT_PATTERNS[intent]['icon']
                    st.info(f"**{icon} {intent.title()}**: {', '.join(features)}")
        else:
            st.warning("Please enter some text to classify.")

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
                    result = classify_intent(str(text))
                    simple_result = {
                        'text': result['text'][:60] + '...' if len(result['text']) > 60 else result['text'],
                        'primary_intent': result['primary_intent'],
                        'confidence': result['confidence'],
                        'complexity': result['complexity']
                    }
                    results.append(simple_result)
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                st.success(f"✅ Classified {len(results_df)} texts!")
                
                # Summary stats
                st.subheader("📊 Summary Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Classified", len(results_df))
                with col2:
                    most_common = results_df['primary_intent'].mode()[0] if len(results_df) > 0 else "N/A"
                    st.metric("Most Common", most_common.title())
                with col3:
                    avg_conf = results_df['confidence'].mean()
                    st.metric("Avg Confidence", f"{avg_conf:.1%}")
                
                # Intent distribution
                intent_counts = results_df['primary_intent'].value_counts()
                fig = px.pie(values=intent_counts.values, names=intent_counts.index,
                            title="Intent Distribution")
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
    st.markdown("**Testing with typical chatbot queries**")
    
    sample_texts = [
        "Hello! How can I get started?",
        "What are your business hours?",
        "I need to cancel my booking for tomorrow",
        "This service is terrible! Not working at all!",
        "Can you please help me reset my password?",
        "I'd like to make a reservation for dinner",
        "Thank you so much for your assistance!",
        "Goodbye, have a great day!"
    ]
    
    with st.expander("👁️ View Sample Queries"):
        for i, text in enumerate(sample_texts, 1):
            st.write(f"{i}. {text}")
    
    if st.button("🚀 Run Demo", type="primary"):
        results = []
        with st.spinner("Classifying intents..."):
            for text in sample_texts:
                result = classify_intent(text)
                results.append({
                    'text': result['text'],
                    'intent': result['primary_intent'],
                    'confidence': result['confidence'],
                    'complexity': result['complexity']
                })
        
        results_df = pd.DataFrame(results)
        st.success("✅ Demo Complete!")
        
        # Summary
        st.subheader("📊 Demo Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Queries Analyzed", len(results_df))
        with col2:
            unique = results_df['intent'].nunique()
            st.metric("Unique Intents", unique)
        with col3:
            avg = results_df['confidence'].mean()
            st.metric("Avg Confidence", f"{avg:.1%}")
        
        # Results
        st.subheader("📋 Classification Results")
        for idx, row in results_df.iterrows():
            icon = INTENT_PATTERNS.get(row['intent'], {}).get('icon', '🤖')
            with st.expander(f"{icon} Query {idx+1}: {row['intent'].title()}"):
                st.write(f"**Text**: {row['text']}")
                cols = st.columns(2)
                with cols[0]:
                    st.metric("Confidence", f"{row['confidence']:.1%}")
                with cols[1]:
                    st.metric("Complexity", row['complexity'])
        
        # Visualization
        fig = px.bar(results_df, x=results_df.index, y='confidence',
                     color='intent', title='Intent Confidence by Query',
                     labels={'x': 'Query #', 'confidence': 'Confidence'})
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**About**: Intent Classification - Chatbot intent recognition for customer service automation")
st.caption("💡 Tip: Use this to route user queries to appropriate handlers in chatbots and virtual assistants")
