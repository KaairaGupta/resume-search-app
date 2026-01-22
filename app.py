
import streamlit as st
import pandas as pd

df = pd.read_csv("parsed_data/resumes.csv")

st.title("Candidate Resume Search Platform")
st.write(f"Total Candidates: {len(df)}")

# Filters
sectors = sorted({s.strip() for sublist in df["sectors"].dropna() for s in sublist.split(",")})
sector_filter = st.multiselect("Sector", sectors)

markets = sorted({m.strip() for sublist in df["markets"].dropna() for m in sublist.split(",")})
market_filter = st.multiselect("Market", markets)

exp_min = float(df["experience_years"].min())
exp_max = float(df["experience_years"].max())
experience = st.slider("Experience Years", exp_min, exp_max, (exp_min, exp_max), step=0.25)

filtered_df = df.copy()
if sector_filter:
    filtered_df = filtered_df[filtered_df["sectors"].str.contains("|".join(sector_filter), case=False)]
if market_filter:
    filtered_df = filtered_df[filtered_df["markets"].str.contains("|".join(market_filter), case=False)]
filtered_df = filtered_df[
    (filtered_df["experience_years"] >= experience[0]) &
    (filtered_df["experience_years"] <= experience[1])
]

st.write("### Matching Candidates")
st.dataframe(filtered_df[["name", "current_role", "current_company", "experience_years", "sectors", "markets"]])

st.write("### Sector Distribution")
st.bar_chart(filtered_df["sectors"].value_counts())

st.write("### Experience Distribution")
st.bar_chart(filtered_df["experience_years"].value_counts())
