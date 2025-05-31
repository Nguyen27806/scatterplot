import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("University GPA vs. Starting Salary")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load Excel data
    df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # Display a preview
    st.subheader("Data Preview")
    st.dataframe(df.head())

    # Scatter plot with regression line
    st.subheader("Dot Chart: University GPA vs. Starting Salary")

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(x='University_GPA', y='Starting_Salary', data=df, ax=ax, scatter_kws={'alpha': 0.7})
    ax.set_title('University GPA vs. Starting Salary')
    ax.set_xlabel('University GPA')
    ax.set_ylabel('Starting Salary')
    ax.grid(True)

    st.pyplot(fig)

    # Basic insight
    st.markdown("""
    **Insight:**  
    This chart shows a slight upward trend, indicating that students with higher GPAs often start with slightly higher salaries.  
    However, the wide spread also suggests GPA alone is not a strong predictor of income.
    """)

else:
    st.warning("Please upload a valid Excel file with a sheet named 'education_career_success'.")
