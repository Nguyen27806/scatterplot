import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="GPA vs Salary Filtered", layout="centered")
st.title("🎯 Interactive Dot Chart: GPA vs. Salary with Age Filter")

uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load the Excel file
    df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # Age range slicer
    st.subheader("🎚️ Filter by Age Range")
    min_age, max_age = int(df["Age"].min()), int(df["Age"].max())
    age_range = st.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))
    
    # Filter based on selected range
    filtered_df = df[(df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1])]

    # Plot
    st.subheader("📈 Dot Chart: University GPA vs. Starting Salary")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(x=filtered_df["University_GPA"], y=filtered_df["Starting_Salary"], ax=ax, scatter_kws={"alpha": 0.7})
    ax.set_xlabel("University GPA")
    ax.set_ylabel("Starting Salary")
    ax.set_title(f"Filtered by Age {age_range[0]}–{age_range[1]}")
    ax.grid(True)
    st.pyplot(fig)

    # Optional: Show filtered data
    with st.expander("🔍 View Filtered Data"):
        st.dataframe(filtered_df)

else:
    st.info("👈 Upload an Excel file with a sheet named `education_career_success`.")
