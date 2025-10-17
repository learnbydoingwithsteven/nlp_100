# ⚡ Quick Start Guide - 100 NLP Applications

## 🚀 Get Started in 3 Steps

### Step 1: Choose Your App
```bash
# Interactive browser
python app_manager.py

# Or list all apps
python app_manager.py list
```

### Step 2: Install Dependencies
```bash
cd app_001_sentiment_analysis
pip install -r requirements.txt
```

### Step 3: Run the App
```bash
streamlit run app.py
```

**That's it!** Your app opens at `http://localhost:8501`

---

## 🎯 Popular Apps to Try First

### 1. Sentiment Analysis (App 001)
```bash
cd app_001_sentiment_analysis
pip install -r requirements.txt
streamlit run app.py
```
**Use Case**: Analyze customer reviews, social media sentiment

### 2. Spam Detection (App 002)
```bash
cd app_002_spam_detection
pip install -r requirements.txt
streamlit run app.py
```
**Use Case**: Filter spam emails and messages

### 3. Text Summarization (App 003)
```bash
cd app_003_text_summarization
pip install -r requirements.txt
streamlit run app.py
```
**Use Case**: Summarize long documents automatically

### 4. Named Entity Recognition (App 021)
```bash
cd app_021_named_entity_recognition
pip install -r requirements.txt
streamlit run app.py
```
**Use Case**: Extract names, organizations, locations

### 5. Question Answering (App 062)
```bash
cd app_062_question_answering
pip install -r requirements.txt
streamlit run app.py
```
**Use Case**: Answer questions from documents

---

## 📋 Command Cheat Sheet

### Using App Manager
```bash
# Interactive mode
python app_manager.py

# List all apps
python app_manager.py list

# Search apps
python app_manager.py search "sentiment"

# Launch app by ID
python app_manager.py launch 1

# Install dependencies
python app_manager.py install 1

# View app details
python app_manager.py help
```

### Direct App Launch
```bash
# Navigate to app
cd app_XXX_name

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py

# Run on custom port
streamlit run app.py --server.port 8502

# Run for network access
streamlit run app.py --server.address 0.0.0.0
```

---

## 🔧 One-Time Setup

### Create Virtual Environment
```bash
python -m venv nlp_env

# Windows
nlp_env\Scripts\activate

# macOS/Linux
source nlp_env/bin/activate
```

### Install Common NLP Resources
```bash
# NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# spaCy model
python -m spacy download en_core_web_sm

# TextBlob corpora
python -m textblob.download_corpora
```

---

## 📚 Find the Right App

### By Category

**Text Analysis** (Apps 1-20)
- Sentiment, spam, toxicity, emotion detection
- Topic modeling, readability analysis

**Information Extraction** (Apps 21-40)
- Named entities, emails, resumes, invoices
- Dates, URLs, keywords, citations

**Text Generation** (Apps 41-60)
- Text generation, paraphrasing, translation
- Headlines, questions, summaries

**Semantic Analysis** (Apps 61-80)
- Semantic search, similarity, clustering
- Question answering, duplicate detection

**Domain-Specific** (Apps 81-100)
- Legal, medical, financial analysis
- Customer support, job matching, SEO

### By Use Case

**E-commerce**: Apps 1, 20, 53, 65, 90  
**Customer Service**: Apps 7, 52, 87, 94  
**Content Creation**: Apps 41, 47, 53, 54  
**Data Extraction**: Apps 21-40  
**Search & Discovery**: Apps 61-65, 70  

---

## 💡 Tips

### Performance
- Use smaller models for faster processing
- Enable caching with `@st.cache_data`
- Process in batches for large datasets

### Troubleshooting
```bash
# Port already in use?
streamlit run app.py --server.port 8502

# Module not found?
pip install -r requirements.txt --force-reinstall

# NLTK data missing?
python -c "import nltk; nltk.download('all')"
```

### Best Practices
- Start with demo/sample data
- Test with single inputs first
- Use batch processing for multiple files
- Export results as CSV for analysis

---

## 📖 Documentation

- **README.md** - Main project overview
- **APP_CATALOG.md** - Complete app reference (all 100 apps)
- **DEPLOYMENT_GUIDE.md** - Deployment instructions
- **PROJECT_SUMMARY.md** - Project completion summary
- **QUICK_START.md** - This file

---

## 🎓 Learning Path

### Beginner
1. Start with **App 001** (Sentiment Analysis)
2. Try **App 002** (Spam Detection)
3. Explore **App 003** (Text Summarization)

### Intermediate
1. **App 021** (Named Entity Recognition)
2. **App 032** (Keyword Extraction)
3. **App 062** (Question Answering)

### Advanced
1. **App 041** (Text Generation)
2. **App 061** (Semantic Search)
3. **App 087** (Customer Support Automation)

---

## 🆘 Need Help?

### Quick Answers
- **Q**: App won't start?  
  **A**: Check Python version (3.8+) and install requirements

- **Q**: Import errors?  
  **A**: Run `pip install -r requirements.txt`

- **Q**: Slow performance?  
  **A**: Use smaller models or enable caching

- **Q**: Port 8501 in use?  
  **A**: Use `--server.port 8502`

### Get Support
1. Check app's README.md
2. Review DEPLOYMENT_GUIDE.md
3. Search Streamlit documentation
4. Open GitHub issue

---

## 🎯 Next Steps

1. ✅ Run your first app
2. ✅ Try batch processing
3. ✅ Export results
4. ✅ Explore more apps
5. ✅ Deploy to cloud

---

**Ready to start? Run:**
```bash
python app_manager.py
```

**Happy NLP Processing! 🚀**
