import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="GPA vs Salary Filtered", layout="centered")
st.title("🎯 Interactive GPA Range Slicer")

uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load file
    df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # GPA range slicer
    st.subheader("🎓 Filter by University GPA")
    min_gpa, max_gpa = float(df["University_GPA"].min()), float(df["University_GPA"].max())
    gpa_range = st.slider("Select GPA Range", min_value=round(min_gpa, 2), max_value=round(max_gpa, 2), value=(round(min_gpa, 2), round(max_gpa, 2)), step=0.01)

    # Filter dataset
    filtered_df = df[(df["University_GPA"] >= gpa_range[0]) & (df["University_GPA"] <= gpa_range[1])]

    # Plot
    st.subheader("📈 GPA vs. Starting Salary")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(x=filtered_df["University_GPA"], y=filtered_df["Starting_Salary"], ax=ax, scatter_kws={"alpha": 0.7})
    ax.set_xlabel("University GPA")
    ax.set_ylabel("Starting Salary")
    ax.set_title(f"Filtered by GPA: {gpa_range[0]}–{gpa_range[1]}")
    ax.grid(True)
    st.pyplot(fig)

    # Show filtered data
    with st.expander("🔍 View Filtered Data"):
        st.dataframe(filtered_df)

else:
    st.info("👈 Upload an Excel file with a sheet named `education_career_success`.")
