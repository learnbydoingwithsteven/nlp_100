"""
Batch App Improvement Script - Systematically Improve All 100 NLP Apps
This script reads each app and replaces the generic process_text function with proper NLP implementation
"""

import os
from pathlib import Path
import re

# Base directory
BASE_DIR = Path(__file__).parent

# Define proper implementations for each app
APP_IMPROVEMENTS = {
    1: {  # Sentiment Analysis - ALREADY DONE
        "skip": True
    },
    
    2: {  # Spam Detection
        "title": "Spam Detection",
        "emoji": "🚫",
        "imports": """from sklearn.feature_extraction.text import CountVectorizer
import re""",
        "function": """def analyze_spam(text):
    '''Detect spam using keyword and pattern analysis'''
    spam_keywords = ['winner', 'free', 'prize', 'click here', 'urgent', 'cash', 'loan', 
                     'credit', 'congratulations', 'offer', 'discount', 'limited time', 
                     'act now', '$$$', 'buy now', 'call now']
    
    text_lower = text.lower()
    spam_score = 0
    found_keywords = []
    
    # Check spam keywords
    for keyword in spam_keywords:
        if keyword in text_lower:
            spam_score += 1
            found_keywords.append(keyword)
    
    # Pattern checks
    if re.search(r'\\d{3,}', text):  # Multiple digits
        spam_score += 0.5
    if len([c for c in text if c.isupper()]) / max(len(text), 1) > 0.5:  # Excessive caps
        spam_score += 1
    if text.count('!') > 2:  # Multiple exclamations
        spam_score += 0.5
    if re.search(r'\\$\\d+', text):  # Dollar amounts
        spam_score += 0.5
    
    spam_probability = min(spam_score / 5.0, 1.0)
    is_spam = spam_probability > 0.4
    
    return {
        'text': text,
        'is_spam': is_spam,
        'classification': 'SPAM ❌' if is_spam else 'HAM ✅',
        'spam_probability': spam_probability,
        'ham_probability': 1 - spam_probability,
        'spam_score': spam_score,
        'found_keywords': found_keywords,
        'keyword_count': len(found_keywords),
        'confidence': max(spam_probability, 1 - spam_probability),
        'word_count': len(text.split())
    }""",
        "demo_texts": [
            "CONGRATULATIONS! You've WON $1000000! Click here NOW to claim your prize!!!",
            "Hi, can we schedule a meeting tomorrow at 3pm to discuss the project?",
            "FREE OFFER! Limited time only! Act now and get 90% OFF! Click here!!!",
            "Your Amazon order has been shipped and will arrive tomorrow.",
            "URGENT: Your account will be closed. Send your password immediately!"
        ]
    },
    
    3: {  # Text Summarization
        "title": "Text Summarization",
        "emoji": "📄",
        "imports": """from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)""",
        "function": """def summarize_text(text, sentences_count=3, algorithm='textrank'):
    '''Summarize text using extractive summarization'''
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        
        # Choose algorithm
        if algorithm == 'lsa':
            summarizer = LsaSummarizer()
        elif algorithm == 'lexrank':
            summarizer = LexRankSummarizer()
        else:
            summarizer = TextRankSummarizer()
        
        # Generate summary
        summary_sentences = summarizer(parser.document, sentences_count)
        summary = ' '.join([str(sentence) for sentence in summary_sentences])
        
        # Calculate metrics
        original_sents = text.split('.')
        original_words = text.split()
        summary_words = summary.split()
        
        compression_ratio = (1 - len(summary) / max(len(text), 1)) * 100
        
        return {
            'original_text': text,
            'summary': summary,
            'original_length': len(text),
            'summary_length': len(summary),
            'original_sentences': len([s for s in original_sents if s.strip()]),
            'summary_sentences': sentences_count,
            'original_words': len(original_words),
            'summary_words': len(summary_words),
            'compression_ratio': compression_ratio,
            'algorithm': algorithm,
            'words_saved': len(original_words) - len(summary_words)
        }
    except Exception as e:
        return {
            'error': str(e),
            'original_text': text,
            'summary': 'Error generating summary',
            'original_length': len(text)
        }""",
        "demo_texts": [
            "Artificial intelligence is revolutionizing the way we live and work. From healthcare to transportation, AI is making significant impacts across various industries. Machine learning algorithms can now detect diseases earlier than human doctors. Self-driving cars are becoming a reality on our roads. Natural language processing enables computers to understand and generate human language. Despite these advances, AI also raises important ethical questions about privacy, job displacement, and algorithmic bias. As we continue to develop AI technologies, it's crucial that we address these concerns and ensure that AI benefits all of humanity."
        ]
    },
    
    4: {  # Language Detection
        "title": "Language Detection",
        "emoji": "🌍",
        "imports": """from langdetect import detect, detect_langs, DetectorFactory
DetectorFactory.seed = 0""",
        "function": """def detect_language(text):
    '''Detect the language of text'''
    try:
        lang_code = detect(text)
        lang_probs = detect_langs(text)
        
        # Language name mapping
        lang_names = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
            'zh-cn': 'Chinese (Simplified)', 'zh-tw': 'Chinese (Traditional)',
            'ar': 'Arabic', 'hi': 'Hindi', 'ko': 'Korean', 'nl': 'Dutch',
            'sv': 'Swedish', 'no': 'Norwegian', 'da': 'Danish', 'fi': 'Finnish',
            'pl': 'Polish', 'tr': 'Turkish', 'vi': 'Vietnamese', 'th': 'Thai'
        }
        
        detected_lang = lang_names.get(lang_code, lang_code.upper())
        
        # Parse probabilities
        prob_dict = {}
        for lp in lang_probs:
            parts = str(lp).split(':')
            if len(parts) == 2:
                prob_dict[parts[0]] = float(parts[1])
        
        top_prob = max(prob_dict.values()) if prob_dict else 0.0
        
        return {
            'text': text,
            'language_code': lang_code,
            'language_name': detected_lang,
            'confidence': top_prob,
            'all_probabilities': prob_dict,
            'text_length': len(text),
            'word_count': len(text.split()),
            'top_3_languages': sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)[:3]
        }
    except Exception as e:
        return {
            'text': text,
            'error': str(e),
            'language_code': 'unknown',
            'language_name': 'Unknown',
            'confidence': 0.0
        }""",
        "demo_texts": [
            "Hello, how are you today? This is a sample text in English.",
            "Bonjour, comment allez-vous? Ceci est un exemple de texte en français.",
            "Hola, ¿cómo estás? Este es un texto de ejemplo en español.",
            "Hallo, wie geht es dir? Dies ist ein Beispieltext auf Deutsch.",
            "Ciao, come stai? Questo è un testo di esempio in italiano."
        ]
    },
    
    21: {  # Named Entity Recognition
        "title": "Named Entity Recognition",
        "emoji": "🏷️",
        "imports": """import spacy
try:
    nlp = spacy.load('en_core_web_sm')
except:
    st.warning("Downloading spaCy model... This may take a moment.")
    import subprocess
    subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'], check=True)
    nlp = spacy.load('en_core_web_sm')""",
        "function": """def extract_entities(text):
    '''Extract named entities using spaCy'''
    doc = nlp(text)
    
    entities = []
    entity_counts = {}
    
    for ent in doc.ents:
        entities.append({
            'text': ent.text,
            'label': ent.label_,
            'start': ent.start_char,
            'end': ent.end_char
        })
        
        entity_counts[ent.label_] = entity_counts.get(ent.label_, 0) + 1
    
    # Group entities by type
    entity_groups = {}
    for ent in entities:
        label = ent['label']
        if label not in entity_groups:
            entity_groups[label] = []
        entity_groups[label].append(ent['text'])
    
    return {
        'text': text,
        'entities': entities,
        'entity_count': len(entities),
        'entity_types': entity_counts,
        'unique_types': len(entity_counts),
        'entity_groups': entity_groups,
        'persons': [e['text'] for e in entities if e['label'] == 'PERSON'],
        'organizations': [e['text'] for e in entities if e['label'] == 'ORG'],
        'locations': [e['text'] for e in entities if e['label'] in ['GPE', 'LOC']],
        'dates': [e['text'] for e in entities if e['label'] == 'DATE'],
        'money': [e['text'] for e in entities if e['label'] == 'MONEY'],
        'word_count': len(text.split())
    }""",
        "demo_texts": [
            "Apple Inc. was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in Cupertino, California on April 1, 1976. The company is now worth over $2 trillion.",
            "The United Nations headquarters is located in New York City. Antonio Guterres serves as the current Secretary-General.",
            "Amazon CEO Jeff Bezos announced a $10 billion investment in climate change initiatives on February 17, 2020."
        ]
    }
}

def generate_improved_app(app_num, config):
    """Generate improved app.py content"""
    
    app_dir = BASE_DIR / f"app_{app_num:03d}_{config['title'].lower().replace(' ', '_')}"
    app_file = app_dir / "app.py"
    
    if not app_file.exists():
        print(f"⚠️  App {app_num:03d} file not found: {app_file}")
        return False
    
    # Read current content
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already improved
    if 'def process_text(text):' not in content:
        print(f"✅ App {app_num:03d} already improved or has custom implementation")
        return True
    
    print(f"🔧 Improving App {app_num:03d}: {config['title']}...")
    
    # Update imports (add after existing imports)
    import_section_match = re.search(r'(import.*?\n)+', content, re.MULTILINE)
    if import_section_match and config.get('imports'):
        existing_imports = import_section_match.group(0)
        new_imports = existing_imports + config['imports'] + "\n"
        content = content.replace(existing_imports, new_imports)
    
    # Replace process_text function
    old_function_pattern = r'def process_text\(text\):.*?return results'
    if config.get('function'):
        content = re.sub(old_function_pattern, config['function'], content, flags=re.DOTALL)
    
    # Update title emoji if specified
    if config.get('emoji'):
        content = re.sub(r'page_icon="🔤"', f'page_icon="{config["emoji"]}"', content)
        content = re.sub(r'st\.title\("🔤', f'st.title("{config["emoji"]}', content)
    
    # Update demo texts if provided
    if config.get('demo_texts'):
        demo_text_pattern = r'sample_texts = \[.*?\]'
        new_demo_texts = "sample_texts = [\n        " + ",\n        ".join([f'"{text}"' for text in config['demo_texts']]) + "\n    ]"
        content = re.sub(demo_text_pattern, new_demo_texts, content, flags=re.DOTALL)
    
    # Write updated content
    try:
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully improved App {app_num:03d}")
        return True
    except Exception as e:
        print(f"❌ Error improving App {app_num:03d}: {e}")
        return False

def main():
    print("=" * 70)
    print("🚀 Batch App Improvement Script")
    print("=" * 70)
    print()
    
    improved_count = 0
    skipped_count = 0
    error_count = 0
    
    for app_num, config in APP_IMPROVEMENTS.items():
        if config.get('skip'):
            print(f"⏭️  Skipping App {app_num:03d} (already manually improved)")
            skipped_count += 1
            continue
        
        result = generate_improved_app(app_num, config)
        if result:
            improved_count += 1
        else:
            error_count += 1
        print()
    
    print("=" * 70)
    print(f"📊 Summary:")
    print(f"   ✅ Improved: {improved_count}")
    print(f"   ⏭️  Skipped: {skipped_count}")
    print(f"   ❌ Errors: {error_count}")
    print("=" * 70)
    print()
    print("💡 Note: For the remaining apps, consider using similar patterns")
    print("   or create category-specific batch improvements.")

if __name__ == "__main__":
    main()
