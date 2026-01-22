import os
import pandas as pd
import streamlit as st

# -----------------------------
# Paths & Config
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "parsed", "resumes.csv")

st.set_page_config(
    page_title="Candidate Resume Search",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df.fillna("", inplace=True)
    return df

df = load_data()

# -----------------------------
# Helper Functions
# -----------------------------
def multi_filter(df, column, selected_values):
    """Filter DataFrame column (comma-separated strings) by selected values"""
    if not selected_values:
        return df
    return df[df[column].apply(
        lambda x: any(v.lower() in [i.strip().lower() for i in x.split(",")] for v in selected_values)
    )]

# -----------------------------
# Title & Summary
# -----------------------------
st.title("Candidate Resume Search Platform")
st.write(f"**Total Candidates:** {len(df)}")

# -----------------------------
# Filters
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    sectors = sorted({s.strip() for row in df["sectors"] for s in row.split(",") if s})
    sector_filter = st.multiselect("Sector", sectors)

with col2:
    markets = sorted({m.strip() for row in df["markets"] for m in row.split(",") if m})
    market_filter = st.multiselect("Market", markets)

with col3:
    exp_min = float(df["experience_years"].min())
    exp_max = float(df["experience_years"].max())
    exp_range = st.slider(
        "Experience (Years)",
        exp_min,
        exp_max,
        (exp_min, exp_max),
        step=0.5
    )

# Advanced filters in an expander
with st.expander("Advanced Filters"):
    # Investment Approach
    investment_options = sorted({i.strip() for row in df["investment_approach"] for i in row.split(",") if i})
    investment_filter = st.multiselect("Investment Approach", investment_options)
    # Skills
    skills_options = sorted({s.strip() for row in df["skills"] for s in row.split(",") if s})
    skills_filter = st.multiselect("Skills", skills_options)
    # Current role/company keyword
    role_filter = st.text_input("Current Role contains")
    company_filter = st.text_input("Current Company contains")

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df.copy()

filtered_df = multi_filter(filtered_df, "sectors", sector_filter)
filtered_df = multi_filter(filtered_df, "markets", market_filter)
filtered_df = filtered_df[(filtered_df["experience_years"] >= exp_range[0]) & (filtered_df["experience_years"] <= exp_range[1])]
filtered_df = multi_filter(filtered_df, "investment_approach", investment_filter)

if skills_filter:
    filtered_df = filtered_df[filtered_df["skills"].apply(lambda x: any(s.lower() in x.lower() for s in skills_filter))]
if role_filter:
    filtered_df = filtered_df[filtered_df["current_role"].str.contains(role_filter, case=False)]
if company_filter:
    filtered_df = filtered_df[filtered_df["current_company"].str.contains(company_filter, case=False)]

# -----------------------------
# Tabs for Candidates & Visualizations
# -----------------------------
tab1, tab2 = st.tabs(["Candidates", "Visualizations"])

with tab1:
    st.subheader("Matching Candidates")
    st.dataframe(
        filtered_df[
            [
                "name",
                "current_role",
                "current_company",
                "experience_years",
                "sectors",
                "markets",
                "investment_approach",
                "skills"
            ]
        ],
        use_container_width=True
    )

with tab2:
    st.subheader("Candidate Insights")
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Sector Distribution**")
        sector_counts = filtered_df["sectors"].str.split(", ").explode().value_counts()
        st.bar_chart(sector_counts)

    with col2:
        st.markdown("**Market Distribution**")
        market_counts = filtered_df["markets"].str.split(", ").explode().value_counts()
        st.bar_chart(market_counts)

    # Experience distribution with ranges
    st.markdown("**Experience Distribution**")
    bins = [0, 2, 5, 10, 20]
    labels = ["0-2", "2-5", "5-10", "10+"]
    filtered_df["exp_range"] = pd.cut(filtered_df["experience_years"], bins=bins, labels=labels, right=False)
    st.bar_chart(filtered_df["exp_range"].value_counts().sort_index())

    # Top skills
    st.markdown("**Top Skills**")
    skills_counts = filtered_df["skills"].str.split(", ").explode().value_counts().head(10)
    st.bar_chart(skills_counts)

    # Investment Approach distribution
    st.markdown("**Investment Approach Distribution**")
    investment_counts = filtered_df["investment_approach"].str.split(", ").explode().value_counts()
    st.bar_chart(investment_counts)
