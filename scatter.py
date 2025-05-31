import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Setup
st.set_page_config(page_title="GPA Slicer with Grouped Display", layout="centered")
st.title("🎯 GPA Value Slicer → Grouped GPA Chart")

# Upload file
uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load data
    df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # GPA slicer (dùng GPA thật)
    gpa_min = round(float(df["University_GPA"].min()), 2)
    gpa_max = round(float(df["University_GPA"].max()), 2)
    selected_range = st.slider("🎓 Select GPA Range", min_value=gpa_min, max_value=gpa_max, value=(gpa_min, gpa_max), step=0.01)

    # Filter theo GPA gốc
    df_filtered = df[(df["University_GPA"] >= selected_range[0]) & (df["University_GPA"] <= selected_range[1])]

    # Group lại GPA cho biểu đồ
    gpa_bins = [2.0, 2.5, 3.0, 3.5, 4.0]
    gpa_labels = ["2.0–2.5", "2.5–3.0", "3.0–3.5", "3.5–4.0"]
    df_filtered["GPA_Group"] = pd.cut(df_filtered["University_GPA"], bins=gpa_bins, labels=gpa_labels, include_lowest=True)

    # Vẽ biểu đồ
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.stripplot(
        x="GPA_Group",
        y="Starting_Salary",
        data=df_filtered,
        jitter=True,
        alpha=0.7,
        palette="Set2",
        ax=ax
    )
    ax.set_xlabel("GPA Group")
    ax.set_ylabel("Starting Salary")
    ax.set_title("")  # Không tiêu đề
    ax.grid(True)
    st.pyplot(fig)

else:
    st.info("👈 Upload file Excel có sheet `education_career_success`.")
