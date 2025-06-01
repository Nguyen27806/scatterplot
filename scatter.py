import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("🎓 University GPA vs. Starting Salary")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # Group GPA
    gpa_labels = ["2.0–2.5", "2.5–3.0", "3.0–3.5", "3.5–4.0"]
    df["GPA_Group"] = pd.cut(
        df["University_GPA"],
        bins=[2.0, 2.5, 3.0, 3.5, 4.0],
        labels=gpa_labels,
        include_lowest=True
    )

    selected_gpa = st.selectbox("Select GPA Group", ["All"] + gpa_labels)
    salary_min, salary_max = int(df["Starting_Salary"].min()), int(df["Starting_Salary"].max())
    salary_range = st.slider("Select Starting Salary Range", salary_min, salary_max, (salary_min, salary_max), 1000)

    # Filter
    filtered_df = df[df["Starting_Salary"].between(*salary_range)]
    if selected_gpa != "All":
        filtered_df = filtered_df[filtered_df["GPA_Group"] == selected_gpa]

    # Plot with colors by GPA group
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=filtered_df,
        x="University_GPA",
        y="Starting_Salary",
        hue="GPA_Group",
        palette="Set2",
        alpha=0.7,
        ax=ax
    )
    ax.set_xlabel("University GPA")
    ax.set_ylabel("Starting Salary")
    ax.grid(True)
    st.pyplot(fig)

else:
    st.warning("Please upload a valid Excel file with a sheet named 'education_career_success'.")
