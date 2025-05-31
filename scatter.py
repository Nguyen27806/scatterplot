import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="🎯 GPA & Salary Slicers", layout="centered")
st.title("📊 GPA vs. Starting Salary with Filters")

uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load data
    df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # ---- GPA Slicer ----
    st.subheader("🎓 Filter by University GPA")
    gpa_min, gpa_max = float(df["University_GPA"].min()), float(df["University_GPA"].max())
    gpa_range = st.slider(
        "Select GPA Range",
        min_value=round(gpa_min, 2),
        max_value=round(gpa_max, 2),
        value=(round(gpa_min, 2), round(gpa_max, 2)),
        step=0.01
    )

    # ---- Salary Slicer ----
    st.subheader("💰 Filter by Starting Salary")
    salary_min, salary_max = int(df["Starting_Salary"].min()), int(df["Starting_Salary"].max())
    salary_range = st.slider(
        "Select Salary Range",
        min_value=salary_min,
        max_value=salary_max,
        value=(salary_min, salary_max),
        step=1000
    )

    # ---- Filter dataset ----
    filtered_df = df[
        (df["University_GPA"] >= gpa_range[0]) & (df["University_GPA"] <= gpa_range[1]) &
        (df["Starting_Salary"] >= salary_range[0]) & (df["Starting_Salary"] <= salary_range[1])
    ]

    # ---- Plot ----
    st.subheader("📈 GPA vs. Starting Salary (Filtered)")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(
        x=filtered_df["University_GPA"],
        y=filtered_df["Starting_Salary"],
        ax=ax,
        scatter_kws={"alpha": 0.7}
    )
    ax.set_xlabel("University GPA")
    ax.set_ylabel("Starting Salary")
    ax.set_title(f"GPA: {gpa_range[0]}–{gpa_range[1]} | Salary: {salary_range[0]}–{salary_range[1]}")
    ax.grid(True)
    st.pyplot(fig)

    # ---- Optional Table ----
    with st.expander("📄 View Filtered Data Table"):
        st.dataframe(filtered_df)

else:
    st.info("👈 Upload the Excel file with sheet `education_career_success` to begin.")
