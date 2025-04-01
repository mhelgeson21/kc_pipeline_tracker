import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_utils import load_data, add_project

st.set_page_config(page_title="KC Multifamily Pipeline", layout="wide")
st.title("Kansas City Metro Multifamily Construction Pipeline")

data = load_data()
df = pd.DataFrame(data)

st.sidebar.header("Filter Projects")

if not df.empty:
    status_filter = st.sidebar.multiselect("Status", df["status"].unique(), default=df["status"].unique())
    submarket_filter = st.sidebar.multiselect("Submarket", df["submarket"].unique(), default=df["submarket"].unique())

    filtered_df = df[
        (df["status"].isin(status_filter)) &
        (df["submarket"].isin(submarket_filter))
    ]

    st.subheader(f"Filtered Projects ({len(filtered_df)})")
    st.dataframe(filtered_df)

    st.subheader("Units by Submarket")
    if not filtered_df.empty:
        st.bar_chart(filtered_df.groupby("submarket")["units"].sum())
else:
    st.info("No projects found. Add a new one below.")

st.subheader("Add New Project")
with st.form("add_project"):
    project_name = st.text_input("Project Name")
    developer = st.text_input("Developer")
    address = st.text_input("Address")
    submarket = st.text_input("Submarket")
    proj_type = st.selectbox("Type", ["Multifamily", "Build-to-Rent", "Townhome"])
    units = st.number_input("Units", min_value=0)
    status = st.selectbox("Status", ["Planned", "Approved", "Under Construction", "Delivered"])
    completion = st.date_input("Expected Completion")
    notes = st.text_area("Notes")

    if st.form_submit_button("Add Project"):
        add_project({
            "project_name": project_name,
            "developer": developer,
            "address": address,
            "submarket": submarket,
            "type": proj_type,
            "units": units,
            "status": status,
            "expected_completion": completion.isoformat(),
            "notes": notes
        })
        st.success(f"Added {project_name}")
        st.experimental_rerun()