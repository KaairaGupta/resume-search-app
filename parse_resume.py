import os
import json
import re
from typing import Dict, List

import pandas as pd
import pdfplumber
import docx
from openai import OpenAI

# -----------------------------
# Configuration
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESUME_DIR = os.path.join(BASE_DIR, "data", "resumes")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "parsed")

JSON_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "resumes.json")
CSV_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "resumes.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# Resume Schema
# -----------------------------
RESUME_SCHEMA = {
    "name": "",
    "email": "",
    "education": [],
    "experience_years": 0.0,
    "current_role": "",
    "current_company": "",
    "investment_approach": [],
    "markets": [],
    "sectors": [],
    "skills": []
}

# -----------------------------
# Helpers
# -----------------------------
def extract_text(file_path: str) -> str:
    """Extract text from PDF or DOCX."""
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

def build_prompt(resume_text: str) -> str:
    return f"""
You are an expert resume parser for hedge fund recruiting.

Extract the resume information and return VALID JSON ONLY
that strictly follows this schema:

{json.dumps(RESUME_SCHEMA, indent=2)}

Rules:
1. If years of experience is not explicitly written, infer it from the job dates in the resume. Estimate total experience in years (numeric)
2. If education is not explicitly written, try to extract any degrees and institutions from text.
3. Use arrays for skills, sectors, markets, and investment_approach.
4. Always return JSON only — no extra text.
5. Infer investment approach (Fundamental / Systematic / Quantitative)
6. Infer markets (US, Europe, APAC)


Resume Text:
{resume_text}
"""

def clean_json(raw_text: str) -> str:
    """Remove markdown artifacts from LLM output."""
    raw_text = re.sub(r"```json|```", "", raw_text).strip()
    return raw_text

def parse_resume_llm(text: str) -> Dict:
    """Call LLM and parse JSON safely."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": build_prompt(text)}],
        temperature=0
    )

    raw = response.choices[0].message.content
    cleaned = clean_json(raw)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {}

def normalize_candidate(data: Dict) -> Dict:
    """Normalize fields for downstream filtering."""
    data = data or {}

    # Experience
    try:
        data["experience_years"] = float(data.get("experience_years", 0))
    except:
        data["experience_years"] = 0.0

    # Normalize lists
    for field in ["skills", "sectors", "markets", "investment_approach"]:
        data[field] = list(
            {str(x).title() for x in data.get(field, []) if x}
        )

    return data

# -----------------------------
# Main Pipeline
# -----------------------------
parsed_resumes: List[Dict] = []

for file in os.listdir(RESUME_DIR):
    if file.endswith((".pdf", ".docx")):
        path = os.path.join(RESUME_DIR, file)
        print(f"Parsing: {file}")

        text = extract_text(path)
        parsed = parse_resume_llm(text)
        parsed = normalize_candidate(parsed)
        parsed["source_file"] = file

        parsed_resumes.append(parsed)

# Save JSON
with open(JSON_OUTPUT_PATH, "w") as f:
    json.dump(parsed_resumes, f, indent=2)

# Flatten for CSV
df = pd.json_normalize(parsed_resumes)

def flatten_list(x):
    if isinstance(x, list):
        return ", ".join(map(str, x))
    return ""

for col in ["skills", "sectors", "markets", "investment_approach", "education"]:
    if col in df.columns:
        df[col] = df[col].apply(flatten_list)

df.to_csv(CSV_OUTPUT_PATH, index=False)

print("Parsing complete.")
print(f"Saved JSON → {JSON_OUTPUT_PATH}")
print(f"Saved CSV  → {CSV_OUTPUT_PATH}")
