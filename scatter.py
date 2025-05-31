import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set up page
st.set_page_config(page_title="GPA Group Slicer", layout="centered")
st.title("🎓 GPA Group Slicer vs. Starting Salary")

# Upload file
uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load data
    df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # Group GPA
    gpa_bins = [2.0, 2.5, 3.0, 3.5, 4.0]
    gpa_labels = ["2.0–2.5", "2.5–3.0", "3.0–3.5", "3.5–4.0"]
    df["GPA_Group"] = pd.cut(df["University_GPA"], bins=gpa_bins, labels=gpa_labels, include_lowest=True)

    # GPA Group slicer
    selected_group = st.selectbox("🎯 Select GPA Group", options=gpa_labels)

    # Filter data based on selected group
    filtered_df = df[df["GPA_Group"] == selected_group]

    # Plot
    st.subheader(f"📈 Starting Salary for GPA Group: {selected_group}")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.stripplot(
        x="GPA_Group",
        y="Starting_Salary",
        data=filtered_df,
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

    # Optional: Show table
    with st.expander("📄 View Filtered Data"):
        st.dataframe(filtered_df[["University_GPA", "Starting_Salary", "GPA_Group"]])

else:
    st.info("👈 Upload your Excel file with sheet `education_career_success`.")
