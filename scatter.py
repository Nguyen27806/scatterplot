import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dot Chart: GPA vs Salary", layout="centered")
st.title("🎓 University GPA vs. Starting Salary")

# Upload file
uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load sheet
    df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # Static dropdown-like labels (informational only)
    st.markdown("**X-axis:**")
    st.selectbox("University GPA", options=["University_GPA"], index=0, disabled=True)

    st.markdown("**Y-axis:**")
    st.selectbox("Starting Salary", options=["Starting_Salary"], index=0, disabled=True)

    # Plot
    st.subheader("📈 Dot Chart with Regression Line")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(x=df["University_GPA"], y=df["Starting_Salary"], ax=ax, scatter_kws={"alpha": 0.7})
    ax.set_xlabel("University GPA")
    ax.set_ylabel("Starting Salary")
    ax.set_title("University GPA vs. Starting Salary")
    ax.grid(True)
    st.pyplot(fig)

    # Insight
    st.markdown("""
    **Insight:**  
    There is a slight upward trend, suggesting that students with higher university GPAs may earn higher starting salaries.  
    However, the variation in salaries at each GPA level indicates that other factors also play a role.
    """)

else:
    st.info("👈 Please upload an Excel file with a sheet named `education_career_success`.")
