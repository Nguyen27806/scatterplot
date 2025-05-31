import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# App config
st.set_page_config(page_title="GPA Group vs. Starting Salary", layout="centered")
st.title("📊 GPA Group vs. Starting Salary")

# Upload file
uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load Excel file
    df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # Group GPA
    gpa_bins = [2.0, 2.5, 3.0, 3.5, 4.0]
    gpa_labels = ["2.0–2.5", "2.5–3.0", "3.0–3.5", "3.5–4.0"]
    df["GPA_Group"] = pd.cut(df["University_GPA"], bins=gpa_bins, labels=gpa_labels, include_lowest=True)

    # Plot
    st.subheader("📈 Scatter Plot")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.stripplot(
        x="GPA_Group",
        y="Starting_Salary",
        data=df,
        jitter=True,
        alpha=0.7,
        palette="Set2",
        ax=ax
    )
    ax.set_xlabel("GPA Group")
    ax.set_ylabel("Starting Salary")
    ax.set_title("")  # No title
    ax.grid(True)
    st.pyplot(fig)

    # Optional: View grouped data
    with st.expander("📄 View Data Table"):
        st.dataframe(df[["University_GPA", "Starting_Salary", "GPA_Group"]])
else:
    st.info("👈 Please upload a valid Excel file.")
