import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="GPA vs Salary Filtered", layout="centered")
st.title("🎯 Filtered Dot Chart: University GPA vs. Starting Salary")

uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load Excel
    df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # Dropdowns with unique GPA and Salary values
    gpa_options = sorted(df['University_GPA'].unique())
    salary_options = sorted(df['Starting_Salary'].unique())

    selected_gpa = st.selectbox("🎓 Filter by University GPA", options=["All"] + list(gpa_options))
    selected_salary = st.selectbox("💰 Filter by Starting Salary", options=["All"] + list(salary_options))

    # Filter dataset
    filtered_df = df.copy()
    if selected_gpa != "All":
        filtered_df = filtered_df[filtered_df['University_GPA'] == selected_gpa]
    if selected_salary != "All":
        filtered_df = filtered_df[filtered_df['Starting_Salary'] == selected_salary]

    # Plot
    st.subheader("📈 Dot Chart")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(x=filtered_df["University_GPA"], y=filtered_df["Starting_Salary"], ax=ax, scatter_kws={"alpha": 0.7})
    ax.set_xlabel("University GPA")
    ax.set_ylabel("Starting Salary")
    ax.set_title("University GPA vs. Starting Salary")
    ax.grid(True)
    st.pyplot(fig)

    # Optional: Show filtered data
    with st.expander("🔎 View Filtered Data"):
        st.dataframe(filtered_df)

else:
    st.info("👈 Please upload an Excel file with a sheet named `education_career_success`.")
