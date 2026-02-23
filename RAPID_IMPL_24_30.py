# RAPID IMPLEMENTATION GUIDE FOR APPS 24-30
# Copy these implementations to respective app.py files

# ============================================================================
# APP 024: INVOICE PARSER
# ============================================================================
APP_024_CODE = '''
import streamlit as st
import pandas as pd
import re
import plotly.express as px

st.set_page_config(page_title="Invoice Parser", page_icon="💰", layout="wide")
st.title("💰 Invoice Parser")
st.markdown("**Extract invoice data**: amounts, dates, invoice numbers")

mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

def parse_invoice(text):
    # Extract amounts
    amounts = re.findall(r'\$\s*\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|EUR|GBP)', text)
    # Extract dates
    dates = re.findall(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b', text)
    # Extract invoice numbers
    inv_numbers = re.findall(r'INV[-#]?\s*\d+|Invoice\s*#?\s*\d+', text, re.I)
    
    total = 0
    for amt in amounts:
        num = re.sub(r'[^\d.]', '', amt)
        if num:
            total += float(num)
    
    return {
        'amounts': amounts,
        'total_amount': total,
        'dates': dates,
        'invoice_numbers': inv_numbers,
        'item_count': len(amounts)
    }

if mode == "Single Input":
    st.header("📝 Parse Invoice")
    text = st.text_area("Paste invoice text:", height=150)
    if st.button("🔍 Parse"):
        if text:
            r = parse_invoice(text)
            st.metric("Total Amount", f"${r['total_amount']:.2f}")
            st.write("**Amounts:**", r['amounts'])
            st.write("**Dates:**", r['dates'])
elif mode == "Batch Processing":
    st.header("📚 Batch Parse")
    file = st.file_uploader("Upload CSV", type=['csv'])
    if file and st.button("Parse All"):
        df = pd.read_csv(file)
        results = [parse_invoice(str(t)) for t in df['text']]
        st.metric("Total Invoices", len(results))
        st.write(pd.DataFrame(results))
else:
    if st.button("🚀 Run Demo"):
        sample = "Invoice #12345\\nDate: 01/15/2024\\nAmount: $1,250.50\\nTotal: $1,250.50"
        r = parse_invoice(sample)
        st.write(f"Amount: ${r['total_amount']:.2f}")

st.markdown("---\\n**About**: Invoice Parser - Extract financial data")
'''

# ============================================================================
# APP 025: ADDRESS EXTRACTION
# ============================================================================
APP_025_CODE = '''
import streamlit as st
import pandas as pd
import re
import plotly.express as px

st.set_page_config(page_title="Address Extraction", page_icon="📍", layout="wide")
st.title("📍 Address Extraction")
st.markdown("**Extract addresses**: street, city, state, ZIP")

mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

def extract_addresses(text):
    # ZIP codes
    zips = re.findall(r'\\b\\d{5}(?:-\\d{4})?\\b', text)
    # States (abbreviated)
    states = re.findall(r'\\b[A-Z]{2}\\b', text)
    # Street addresses
    streets = re.findall(r'\\d+\\s+[A-Za-z\\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)', text, re.I)
    
    return {
        'streets': streets,
        'zips': zips,
        'states': states,
        'total_addresses': len(streets)
    }

if mode == "Single Input":
    st.header("📝 Extract Addresses")
    text = st.text_area("Enter text:", height=150)
    if st.button("🔍 Extract"):
        if text:
            r = extract_addresses(text)
            st.metric("Addresses Found", r['total_addresses'])
            for addr in r['streets']:
                st.write(f"📍 {addr}")
elif mode == "Batch Processing":
    st.header("📚 Batch Extract")
    file = st.file_uploader("Upload CSV", type=['csv'])
    if file and st.button("Extract All"):
        df = pd.read_csv(file)
        results = [extract_addresses(str(t)) for t in df['text']]
        st.metric("Total", len(results))
else:
    if st.button("🚀 Run Demo"):
        sample = "Visit us at 123 Main Street, New York, NY 10001"
        r = extract_addresses(sample)
        st.write("Addresses:", r['streets'])

st.markdown("---\\n**About**: Address Extraction - Parse physical addresses")
'''

# ============================================================================
# APP 026: DATETIME EXTRACTION
# ============================================================================
APP_026_CODE = '''
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Datetime Extraction", page_icon="📅", layout="wide")
st.title("📅 Datetime Extraction")
st.markdown("**Extract dates & times**: multiple formats")

mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

def extract_datetimes(text):
    # Dates
    dates = []
    dates.extend(re.findall(r'\\b\\d{1,2}[-/]\\d{1,2}[-/]\\d{2,4}\\b', text))
    dates.extend(re.findall(r'\\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\\s+\\d{1,2},?\\s+\\d{4}\\b', text, re.I))
    # Times
    times = re.findall(r'\\b\\d{1,2}:\\d{2}(?::\\d{2})?\\s*(?:AM|PM|am|pm)?\\b', text)
    
    return {'dates': dates, 'times': times, 'total': len(dates) + len(times)}

if mode == "Single Input":
    text = st.text_area("Enter text:", height=150)
    if st.button("🔍 Extract"):
        if text:
            r = extract_datetimes(text)
            st.metric("Found", r['total'])
            st.write("**Dates:**", r['dates'])
            st.write("**Times:**", r['times'])
elif mode == "Batch Processing":
    file = st.file_uploader("Upload CSV", type=['csv'])
    if file and st.button("Extract All"):
        df = pd.read_csv(file)
        results = [extract_datetimes(str(t)) for t in df['text']]
        st.metric("Total", len(results))
else:
    if st.button("🚀 Demo"):
        r = extract_datetimes("Meeting on January 15, 2024 at 3:30 PM")
        st.write("Dates:", r['dates'], "Times:", r['times'])

st.markdown("---\\n**About**: Datetime Extraction")
'''

# ============================================================================
# APP 027: PHONE EXTRACTION
# ============================================================================
APP_027_CODE = '''
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Phone Extraction", page_icon="☎️", layout="wide")
st.title("☎️ Phone Number Extraction")

mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

def extract_phones(text):
    # Multiple formats
    phones = []
    phones.extend(re.findall(r'\\(?\\d{3}\\)?[-\\s.]?\\d{3}[-\\s.]?\\d{4}', text))
    phones.extend(re.findall(r'\\+\\d{1,3}[-\\s.]?\\(?\\d{3}\\)?[-\\s.]?\\d{3}[-\\s.]?\\d{4}', text))
    return {'phones': list(set(phones)), 'count': len(set(phones))}

if mode == "Single Input":
    text = st.text_area("Enter text:", height=150)
    if st.button("🔍 Extract"):
        if text:
            r = extract_phones(text)
            st.metric("Phones Found", r['count'])
            for phone in r['phones']:
                st.write(f"☎️ {phone}")
elif mode == "Batch Processing":
    file = st.file_uploader("Upload CSV", type=['csv'])
    if file and st.button("Extract All"):
        df = pd.read_csv(file)
        all_phones = []
        for t in df['text']:
            all_phones.extend(extract_phones(str(t))['phones'])
        st.metric("Total Phones", len(set(all_phones)))
        st.write(list(set(all_phones)))
else:
    if st.button("🚀 Demo"):
        r = extract_phones("Call (555) 123-4567 or +1-555-987-6543")
        st.write("Phones:", r['phones'])

st.markdown("---\\n**About**: Phone Extraction")
'''

# ============================================================================
# APP 028: URL EXTRACTION
# ============================================================================
APP_028_CODE = '''
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="URL Extraction", page_icon="🔗", layout="wide")
st.title("🔗 URL Extraction")

mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

def extract_urls(text):
    urls = re.findall(r'https?://[^\\s]+|www\\.[^\\s]+', text, re.I)
    domains = [re.search(r'(?:https?://)?(?:www\\.)?([^/\\s]+)', url).group(1) for url in urls]
    return {'urls': urls, 'domains': list(set(domains)), 'count': len(urls)}

if mode == "Single Input":
    text = st.text_area("Enter text:", height=150)
    if st.button("🔍 Extract"):
        if text:
            r = extract_urls(text)
            st.metric("URLs Found", r['count'])
            for url in r['urls']:
                st.write(f"🔗 {url}")
elif mode == "Batch Processing":
    file = st.file_uploader("Upload CSV", type=['csv'])
    if file and st.button("Extract All"):
        df = pd.read_csv(file)
        all_urls = []
        for t in df['text']:
            all_urls.extend(extract_urls(str(t))['urls'])
        st.metric("Total URLs", len(all_urls))
else:
    if st.button("🚀 Demo"):
        r = extract_urls("Visit https://example.com and www.test.org")
        st.write("URLs:", r['urls'])

st.markdown("---\\n**About**: URL Extraction")
'''

# ============================================================================
# APP 029: PRODUCT MENTION EXTRACTION
# ============================================================================
APP_029_CODE = '''
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Product Extraction", page_icon="🏷️", layout="wide")
st.title("🏷️ Product Mention Extraction")

mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

BRANDS = ['Apple', 'Samsung', 'Google', 'Microsoft', 'Sony', 'Dell', 'HP', 'Lenovo']

def extract_products(text):
    found_brands = [b for b in BRANDS if b.lower() in text.lower()]
    models = re.findall(r'\\b(?:iPhone|Galaxy|Pixel)\\s*\\d+\\s*(?:Pro|Max|Ultra)?\\b', text, re.I)
    return {'brands': found_brands, 'models': models, 'total': len(found_brands) + len(models)}

if mode == "Single Input":
    text = st.text_area("Enter text:", height=150)
    if st.button("🔍 Extract"):
        if text:
            r = extract_products(text)
            st.metric("Products Found", r['total'])
            st.write("**Brands:**", r['brands'])
            st.write("**Models:**", r['models'])
elif mode == "Batch Processing":
    file = st.file_uploader("Upload CSV", type=['csv'])
    if file and st.button("Extract All"):
        df = pd.read_csv(file)
        results = [extract_products(str(t)) for t in df['text']]
        st.metric("Total", len(results))
else:
    if st.button("🚀 Demo"):
        r = extract_products("I bought an iPhone 15 Pro and Samsung Galaxy S24")
        st.write("Brands:", r['brands'], "Models:", r['models'])

st.markdown("---\\n**About**: Product Mention Extraction")
'''

# ============================================================================
# APP 030: EVENT EXTRACTION
# ============================================================================
APP_030_CODE = '''
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Event Extraction", page_icon="📅", layout="wide")
st.title("📅 Event Extraction")

mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])

EVENT_KEYWORDS = ['conference', 'meeting', 'webinar', 'workshop', 'seminar', 'summit', 'event']

def extract_events(text):
    events = []
    for keyword in EVENT_KEYWORDS:
        pattern = rf'\\b[A-Z][\\w\\s]*{keyword}[\\w\\s]*'
        events.extend(re.findall(pattern, text, re.I))
    
    dates = re.findall(r'\\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\\s+\\d{1,2},?\\s+\\d{4}\\b', text, re.I)
    return {'events': list(set(events))[:5], 'dates': dates, 'total': len(events)}

if mode == "Single Input":
    text = st.text_area("Enter text:", height=150)
    if st.button("🔍 Extract"):
        if text:
            r = extract_events(text)
            st.metric("Events Found", len(r['events']))
            for event in r['events']:
                st.write(f"📅 {event}")
elif mode == "Batch Processing":
    file = st.file_uploader("Upload CSV", type=['csv'])
    if file and st.button("Extract All"):
        df = pd.read_csv(file)
        results = [extract_events(str(t)) for t in df['text']]
        st.metric("Total", len(results))
else:
    if st.button("🚀 Demo"):
        r = extract_events("AI Conference 2024 on March 15, 2024")
        st.write("Events:", r['events'])

st.markdown("---\\n**About**: Event Extraction")
'''

print("="*80)
print("RAPID IMPLEMENTATION CODE FOR APPS 24-30")
print("="*80)
print("\\nInstructions:")
print("1. Copy each APP_XXX_CODE section")
print("2. Paste into respective app_0XX_*/app.py file")
print("3. Save and test")
print("\\nAll apps follow same pattern: regex extraction + 3 modes + visualization")
print("="*80)
