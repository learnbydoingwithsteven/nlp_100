# 🚀 Deployment Guide - 100 NLP Applications

Complete guide for deploying and running all 100 NLP applications.

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Running Applications](#running-applications)
5. [Deployment Options](#deployment-options)
6. [Troubleshooting](#troubleshooting)

## 🎯 Quick Start

### Run a Single App (Example: Sentiment Analysis)

```bash
# Navigate to app folder
cd app_001_sentiment_analysis

# Install dependencies
pip install -r requirements.txt

# Download required NLTK data (if needed)
python -c "import nltk; nltk.download('punkt')"

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 5GB for all apps and dependencies
- **Internet**: Required for initial package downloads

### Recommended Requirements
- **Python**: 3.10+
- **RAM**: 16GB for transformer-based models
- **GPU**: CUDA-compatible GPU for deep learning apps (optional)
- **Disk Space**: 10GB+ for model caches

## 📦 Installation

### 1. Global Setup

```bash
# Create virtual environment (recommended)
python -m venv nlp_env

# Activate virtual environment
# Windows:
nlp_env\Scripts\activate
# macOS/Linux:
source nlp_env/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

### 2. Install App Dependencies

#### Option A: Install for Single App
```bash
cd app_XXX_name
pip install -r requirements.txt
```

#### Option B: Install for Multiple Apps
```bash
# Create a master requirements file
python create_master_requirements.py

# Install all dependencies
pip install -r requirements_master.txt
```

### 3. Download NLP Resources

Many apps require additional resources:

```bash
# NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# spaCy models
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md

# TextBlob corpora
python -m textblob.download_corpora
```

## 🏃 Running Applications

### Local Development

```bash
# Basic run
streamlit run app.py

# Custom port
streamlit run app.py --server.port 8502

# Custom host (for network access)
streamlit run app.py --server.address 0.0.0.0
```

### Production Mode

```bash
# Disable file watcher for better performance
streamlit run app.py --server.fileWatcherType none

# Set max upload size (default 200MB)
streamlit run app.py --server.maxUploadSize 500
```

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Free)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Add NLP app"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select the app file (app.py)
   - Click "Deploy"

3. **Configuration**
   Create `.streamlit/config.toml`:
   ```toml
   [theme]
   primaryColor = "#FF4B4B"
   backgroundColor = "#FFFFFF"
   secondaryBackgroundColor = "#F0F2F6"
   textColor = "#262730"
   font = "sans serif"
   ```

### Option 2: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t nlp-app .
docker run -p 8501:8501 nlp-app
```

### Option 3: Heroku Deployment

1. **Create Heroku files**

`Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

`setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

2. **Deploy**
```bash
heroku create your-app-name
git push heroku main
```

### Option 4: AWS EC2 Deployment

```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip
pip3 install streamlit

# Clone repository
git clone your-repo-url
cd your-app

# Install requirements
pip3 install -r requirements.txt

# Run with nohup
nohup streamlit run app.py --server.port 8501 &
```

### Option 5: Azure App Service

```bash
# Install Azure CLI
az login

# Create app service
az webapp up --name your-app-name --runtime "PYTHON:3.10"

# Configure startup command
az webapp config set --name your-app-name --startup-file "streamlit run app.py"
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Problem: ModuleNotFoundError
# Solution: Install missing package
pip install package-name

# Or reinstall requirements
pip install -r requirements.txt --force-reinstall
```

#### 2. NLTK Data Not Found
```python
# Problem: LookupError: Resource punkt not found
# Solution: Download NLTK data
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

#### 3. Memory Errors
```bash
# Problem: MemoryError or killed process
# Solution: Increase system swap or use smaller models

# For transformer models, use smaller variants:
# Instead of: model = "bert-base-uncased"
# Use: model = "distilbert-base-uncased"
```

#### 4. Port Already in Use
```bash
# Problem: Port 8501 is already in use
# Solution: Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Linux/macOS:
lsof -ti:8501 | xargs kill -9
```

#### 5. Slow Performance
```bash
# Enable caching in Streamlit
# Add to app.py:
@st.cache_data
def expensive_function():
    # Your code here
    pass

# Reduce model size
# Use quantized or distilled models
```

### Performance Optimization

#### 1. Caching
```python
import streamlit as st

@st.cache_data
def load_model():
    # Load model once and cache
    return model

@st.cache_resource
def load_large_resource():
    # Cache resources that shouldn't be copied
    return resource
```

#### 2. Lazy Loading
```python
# Load models only when needed
if st.button("Process"):
    model = load_model()  # Load on demand
    result = model.process(text)
```

#### 3. Batch Processing
```python
# Process in batches for large datasets
batch_size = 100
for i in range(0, len(data), batch_size):
    batch = data[i:i+batch_size]
    process_batch(batch)
```

## 📊 Monitoring and Logging

### Enable Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("App started")
```

### Track Usage
```python
# Add analytics
import streamlit as st

# Track button clicks
if st.button("Process"):
    st.session_state.clicks = st.session_state.get('clicks', 0) + 1
    logger.info(f"Process button clicked {st.session_state.clicks} times")
```

## 🔐 Security Best Practices

### 1. Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
```

### 2. Input Validation
```python
def validate_input(text):
    if len(text) > 10000:
        raise ValueError("Text too long")
    if not text.strip():
        raise ValueError("Empty text")
    return text.strip()
```

### 3. Rate Limiting
```python
import time

if 'last_request' not in st.session_state:
    st.session_state.last_request = 0

current_time = time.time()
if current_time - st.session_state.last_request < 1:
    st.warning("Please wait before making another request")
else:
    st.session_state.last_request = current_time
    # Process request
```

## 📱 Mobile Optimization

```toml
# .streamlit/config.toml
[server]
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
base = "light"
```

## 🧪 Testing

### Unit Tests
```python
# test_app.py
import pytest
from app import process_text

def test_process_text():
    result = process_text("Hello world")
    assert result is not None
    assert len(result) > 0
```

Run tests:
```bash
pytest test_app.py
```

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [NLP Libraries Documentation](https://nlp.seas.harvard.edu)

## 🆘 Support

For issues or questions:
1. Check the app's README.md
2. Review this deployment guide
3. Search [Streamlit Forum](https://discuss.streamlit.io)
4. Open an issue on GitHub

---

**Happy Deploying! 🚀**
