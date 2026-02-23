"""
NLP App 023: Resume Parser
Real-world use case: CV information extraction
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(
    page_title="Resume Parser",
    page_icon="🔤",
    layout="wide"
)

st.title("📄 Resume Parser")
st.markdown("""
**Real-world Use Case**: Extract structured information from resumes/CVs
- Skills and competencies
- Education and degrees
- Work experience
- Contact information
""")

# Sidebar
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Mode", ["Single Input", "Batch Processing", "Demo"])
st.sidebar.markdown("---")
st.sidebar.markdown("**Extraction Features:**")
st.sidebar.markdown("""
- 🎓 Education
- 💼 Experience
- 🛠️ Skills
- 📧 Contact Info
- 📅 Dates
""")

# Skills database
SKILLS_DB = ['python', 'java', 'javascript', 'react', 'angular', 'vue', 'node', 'sql', 'mongodb',
             'aws', 'azure', 'docker', 'kubernetes', 'git', 'machine learning', 'deep learning',
             'data analysis', 'excel', 'powerpoint', 'communication', 'leadership', 'project management']

# Education keywords
EDUCATION_KEYWORDS = ['bachelor', 'master', 'phd', 'doctorate', 'degree', 'university', 'college',
                      'diploma', 'certificate', 'bsc', 'msc', 'ba', 'ma', 'mba', 'engineering']

def parse_resume(text):
    """Parse resume and extract key information"""
    text_lower = text.lower()
    lines = text.split('\n')

    # Extract emails
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)

    # Extract phone numbers
    phones = re.findall(r'\b(?:\+?\d{1,3}[-.\s]?)?(\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b', text)

    # Extract skills
    found_skills = []
    for skill in SKILLS_DB:
        if skill in text_lower:
            found_skills.append(skill)

    # Extract education
    education = []
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in EDUCATION_KEYWORDS):
            education.append(line.strip())

    # Extract dates (years)
    years = re.findall(r'\b(19|20)\d{2}\b', text)

    # Estimate experience years
    if years:
        years_int = [int(y) for y in years]
        experience_years = max(years_int) - min(years_int) if len(years_int) > 1 else 0
    else:
        experience_years = 0

    return {
        'text': text,
        'emails': emails,
        'phones': phones,
        'skills': found_skills,
        'skill_count': len(found_skills),
        'education': education[:5],  # Top 5
        'years_mentioned': sorted(set(years), reverse=True),
        'estimated_experience': experience_years,
        'total_lines': len(lines)
    }

# Mode: Single Input
if mode == "Single Input":
    st.header("📝 Single Text Processing")

    user_input = st.text_area(
        "Enter text to process:",
        height=150,
        placeholder="Type or paste your text here..."
    )

    if st.button("🔍 Parse Resume", type="primary"):
        if user_input.strip():
            with st.spinner("Parsing..."):
                result = parse_resume(user_input)

            st.success("✅ Parsing Complete!")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Skills Found", result['skill_count'])
            with col2:
                st.metric("Emails", len(result['emails']))
            with col3:
                st.metric("Education Lines", len(result['education']))
            with col4:
                st.metric("Est. Experience", f"{result['estimated_experience']} yrs")

            # Skills
            if result['skills']:
                st.subheader("🛠️ Identified Skills")
                skills_df = pd.DataFrame({'Skill': result['skills']})
                st.dataframe(skills_df, use_container_width=True)

            # Contact
            st.subheader("📧 Contact Information")
            if result['emails']:
                st.write("**Emails:**", ", ".join(result['emails']))
            if result['phones']:
                st.write("**Phones:**", ", ".join(result['phones']))

            # Education
            if result['education']:
                st.subheader("🎓 Education")
                for edu in result['education']:
                    st.write(f"• {edu}")
        else:
            st.warning("Please enter resume text.")

# Mode: Batch Processing
elif mode == "Batch Processing":
    st.header("📚 Batch Processing")

    uploaded_file = st.file_uploader("Upload CSV with 'text' column", type=['csv'])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} rows")

        if 'text' in df.columns:
            if st.button("🔍 Parse All", type="primary"):
                results = []
                progress_bar = st.progress(0)

                for idx, text in enumerate(df['text']):
                    result = parse_resume(str(text))
                    results.append({
                        'skills': result['skill_count'],
                        'emails': len(result['emails']),
                        'experience': result['estimated_experience']
                    })
                    progress_bar.progress((idx + 1) / len(df))

                results_df = pd.DataFrame(results)
                st.success(f"✅ Parsed {len(results_df)} resumes!")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Resumes", len(results_df))
                with col2:
                    st.metric("Avg Skills", f"{results_df['skills'].mean():.1f}")
                with col3:
                    st.metric("Avg Experience", f"{results_df['experience'].mean():.1f} yrs")

                fig = px.histogram(results_df, x='skills', title='Skills Distribution')
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

    sample = """John Doe
john.doe@email.com | (555) 123-4567

EDUCATION
Bachelor of Science in Computer Science
University of Technology, 2018-2022

EXPERIENCE
Software Engineer, Tech Corp (2022-2024)
- Developed web applications using React and Node.js
- Implemented AWS cloud solutions

SKILLS
Python, JavaScript, React, Node.js, AWS, Docker, Git, SQL, Machine Learning"""

    if st.button("🚀 Run Demo", type="primary"):
        result = parse_resume(sample)

        st.success("✅ Demo Complete!")
        st.metric("Skills Found", result['skill_count'])

        if result['skills']:
            st.write("**Skills:**", ", ".join(result['skills']))
        if result['emails']:
            st.write("**Email:**", result['emails'][0])

st.markdown("---")
st.markdown("**About**: Resume Parser - Extract structured information from CVs")
st.caption("💡 Extracts skills, education, experience, and contact information")
