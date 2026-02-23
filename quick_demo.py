"""
Quick Demo Launcher for Improved NLP Apps
Easily launch and test improved applications
"""

import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent

# List of improved apps with their details
IMPROVED_APPS = {
    1: {
        'name': 'Sentiment Analysis',
        'folder': 'app_001_sentiment_analysis',
        'description': 'Product review sentiment classification with TextBlob and VADER',
        'features': ['Polarity analysis', 'Subjectivity scoring', 'Emotion detection', 'Word clouds']
    },
    2: {
        'name': 'Spam Detection',
        'folder': 'app_002_spam_detection',
        'description': 'Email/SMS spam filtering with keyword and pattern detection',
        'features': ['Spam probability', 'Keyword detection', 'Pattern analysis', 'Confidence scoring']
    },
    3: {
        'name': 'Text Summarization',
        'folder': 'app_003_text_summarization',
        'description': 'Automatic document summarization using TextRank',
        'features': ['Extractive summarization', 'Compression ratio', 'Sentence selection', 'Length control']
    },
    4: {
        'name': 'Language Detection',
        'folder': 'app_004_language_detection',
        'description': 'Multi-language identification with confidence scores',
        'features': ['50+ languages', 'Confidence scoring', 'Probability distribution', 'Language names']
    },
    5: {
        'name': 'Toxicity Detection',
        'folder': 'app_005_toxicity_detection',
        'description': 'Multi-category content moderation for online platforms',
        'features': ['6 toxicity categories', 'Risk assessment', 'Pattern detection', 'Content filtering']
    },
    6: {
        'name': 'Emotion Classification',
        'folder': 'app_006_emotion_classification',
        'description': 'Multi-emotion detection for customer feedback analysis',
        'features': ['6 emotions', 'Intensity scoring', 'Radar charts', 'Keyword detection']
    },
    7: {
        'name': 'Intent Classification',
        'folder': 'app_007_intent_classification',
        'description': 'Chatbot intent recognition for customer service',
        'features': ['10 intent categories', 'Multi-intent detection', 'Confidence scoring', 'Query routing']
    },
    8: {
        'name': 'Topic Modeling',
        'folder': 'app_008_topic_modeling',
        'description': 'Document topic extraction and clustering',
        'features': ['8 topic categories', 'Key term extraction', 'Topic distribution', 'Document organization']
    },
    9: {
        'name': 'Fake News Detection',
        'folder': 'app_009_fake_news_detection',
        'description': 'News article credibility analysis',
        'features': ['Credibility scoring', 'Fake vs credible indicators', 'Risk assessment', 'Pattern recognition']
    },
    10: {
        'name': 'Readability Analysis',
        'folder': 'app_010_readability_analysis',
        'description': 'Text complexity assessment with multiple formulas',
        'features': ['Flesch Reading Ease', 'Grade level', 'SMOG Index', 'Reading time']
    }
}

def display_menu():
    """Display the main menu"""
    print("\n" + "="*80)
    print("🚀 Quick Demo Launcher - Improved NLP Apps")
    print("="*80)
    print("\n✅ Available Improved Apps:\n")
    
    for app_id, details in IMPROVED_APPS.items():
        print(f"  {app_id}. {details['name']}")
        print(f"     📝 {details['description']}")
        print(f"     ✨ Features: {', '.join(details['features'][:2])}")
        print()
    
    print("  0. Exit")
    print("\n" + "="*80)

def launch_app(app_id):
    """Launch a specific app"""
    if app_id not in IMPROVED_APPS:
        print(f"❌ App {app_id} not found or not yet improved.")
        return False
    
    app = IMPROVED_APPS[app_id]
    app_dir = BASE_DIR / app['folder']
    app_file = app_dir / 'app.py'
    
    if not app_file.exists():
        print(f"❌ Error: App file not found at {app_file}")
        return False
    
    print(f"\n{'='*80}")
    print(f"🚀 Launching: {app['name']}")
    print(f"📂 Location: {app_dir}")
    print(f"📝 {app['description']}")
    print(f"\n✨ Features:")
    for feature in app['features']:
        print(f"   • {feature}")
    print(f"\n🌐 Opening at: http://localhost:8501")
    print(f"{'='*80}")
    print("\n⌨️  Press Ctrl+C to stop the app and return to menu\n")
    
    try:
        subprocess.run(
            ['streamlit', 'run', str(app_file)],
            cwd=str(app_dir)
        )
    except KeyboardInterrupt:
        print("\n\n✅ App stopped. Returning to menu...")
    except FileNotFoundError:
        print("\n❌ Error: Streamlit not installed.")
        print("   Install with: pip install streamlit")
    except Exception as e:
        print(f"\n❌ Error launching app: {e}")
    
    return True

def show_status():
    """Show improvement status"""
    print("\n" + "="*80)
    print("🎉 20% MILESTONE REACHED! 🎉")
    print("="*80)
    print(f"\n✅ Apps Improved: {len(IMPROVED_APPS)} / 100")
    print(f"📈 Progress: {len(IMPROVED_APPS)}%")
    print(f"\n🎯 Completed First 20 Apps:")
    print("IMPROVED_APPS = {")
    print("    1: \"Sentiment Analysis\",")
    print("    2: \"Spam Detection\",")
    print("    3: \"Text Summarization\",")
    print("    4: \"Language Detection\",")
    print("    5: \"Toxicity Detection\",")
    print("    6: \"Emotion Classification\",")
    print("    7: \"Intent Classification\",")
    print("    8: \"Topic Modeling\",")
    print("    9: \"Fake News Detection\",")
    print("    10: \"Readability Analysis\",")
    print("    11: \"Plagiarism Detection\",")
    print("    12: \"Genre Classification\",")
    print("    13: \"Urgency Detection\",")
    print("    14: \"Sarcasm Detection\",")
    print("    15: \"Hate Speech Detection\",")
    print("    16: \"Age Group Classification\",")
    print("    17: \"Gender Classification\",")
    print("    18: \"Political Bias Detection\",")
    print("    19: \"Clickbait Detection\",")
    print("    20: \"Review Authenticity\"")
    print("}")
    print(f"\n🚀 Next Target: Apps 21-30 to reach 30%")
    print("="*80)

def main():
    """Main program loop"""
    while True:
        display_menu()
        
        try:
            choice = input("\n👉 Enter your choice (0-10 or 's' for status): ").strip().lower()
            
            if choice == '0':
                print("\n👋 Thank you for using Quick Demo Launcher!")
                print("="*80 + "\n")
                break
            
            elif choice == 's' or choice == 'status':
                show_status()
                input("\nPress Enter to continue...")
            
            elif choice.isdigit():
                app_id = int(choice)
                launch_app(app_id)
            
            else:
                print("\n❌ Invalid choice. Please enter a number between 0-10 or 's'.")
                input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🎯 NLP 100 Apps - Quick Demo Launcher")
    print("="*80)
    print("\n📌 This tool helps you quickly test improved NLP applications")
    print("📌 Each app demonstrates real NLP functionality with visualizations")
    print("📌 All apps support: Single Input | Batch Processing | Demo Mode")
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("\n✅ Streamlit is installed and ready!")
    except ImportError:
        print("\n⚠️  Warning: Streamlit not found!")
        print("   Install with: pip install streamlit")
        print("   Or install all requirements: pip install -r app_001_sentiment_analysis/requirements.txt")
    
    input("\nPress Enter to continue...")
    main()
