
# Candidate Resume Search Platform (Millennium Case Study)

LLM-powered resume parsing and candidate search platform built with Streamlit.

---

## Overview

This platform allows Business Development teams at hedge funds to:

- Parse resumes (PDF/DOCX) into structured JSON/CSV using LLMs.
- Filter candidates based on experience, sectors, markets, skills, investment approach, current role/company.
- Visualize candidate insights with charts.

---

## Features

### Core Features (MVP)
- LLM-based parsing → JSON/CSV
- Filter candidates by:
  - Sector
  - Market
  - Experience
- Streamlit web app with candidate table and visualizations

### Advanced Features
- Multi-value filtering (markets/sectors/skills/investment approach)
- Experience distribution in ranges (`0-2, 2-5, 5-10, 10+`)
- Optional filters:
  - Investment approach (Fundamental / Quant / Systematic)
  - Skills (top N)
  - Current role / company keyword search
- Visualizations:
  - Sector & Market distribution
  - Experience ranges
  - Top skills
  - Investment approach distribution

### Additional Features (if more time available)
- Improve LLM parsing for resumes with varying formats
- Extract experience from “from-to” job dates
- Store parsed resumes in a database (PostgreSQL / MongoDB) for scalability
- Deploy app via Docker or Streamlit Cloud
- Advanced analytics: skill co-occurrence networks, market-sector heatmaps, historical trends
- **Self-learning LLM prompts:**  
  Implement an LLM that adapts and improves its parsing prompts over time based on previous parsing results, handling diverse resume formats more accurately.
- **Fallback name extraction:**  
  If a candidate’s name is missing from the resume, automatically extract it from the **resume file name**.
- **Smart Keyword Search:**  
  Allow free-text search across all resume fields (skills, roles, education, company) to find candidates even if filters don’t match exactly
- **Data Privacy & Security Features:**  
  Encrypt sensitive candidate data and ensure compliance.


---

## Setup Instructions

1. Clone the repo:

git clone <your-repo-link>
cd <repo-name>

2. Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows

3. Install dependencies:

pip install -r requirements.txt

4. Run the Streamlit app:

streamlit run app.py

5. Open your browser and interact with the platform.

The app will open automatically. If not, copy the URL from the terminal

## How It Works

### Resume Parsing
- Extract text from PDF/DOCX resumes
- LLM extracts structured JSON fields
- Data normalized → saved as CSV for the app

### Streamlit App
- Loads parsed CSV
- Filters candidates with multi-value and advanced filters
- Displays table and charts for insights

## Live Demo

Check out the live demo of the Resume Search Platform here:  
[Open Streamlit App](https://demoapp-millennium.streamlit.app)
