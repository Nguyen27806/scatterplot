import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Interactive Dot Chart", layout="centered")
st.title("📊 Interactive Dot Chart with Regression Line")

# Upload file
uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load sheet
    df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # Filter for numeric columns only
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    # Select x and y axes
    st.subheader("🔧 Select Variables")
    x_axis = st.selectbox("X-axis (e.g., University GPA)", numeric_columns, index=numeric_columns.index("University_GPA") if "University_GPA" in numeric_columns else 0)
    y_axis = st.selectbox("Y-axis (e.g., Starting Salary)", numeric_columns, index=numeric_columns.index("Starting_Salary") if "Starting_Salary" in numeric_columns else 1)

    # Plot
    st.subheader(f"📈 Dot Chart: {x_axis} vs. {y_axis}")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(x=df[x_axis], y=df[y_axis], ax=ax, scatter_kws={"alpha": 0.6})
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f"{x_axis} vs. {y_axis}")
    ax.grid(True)
    st.pyplot(fig)

    # Summary
    st.markdown(f"**Interpretation:** This chart helps explore the relationship between `{x_axis}` and `{y_axis}`. A visible slope in the regression line suggests a trend; the tighter the dots around the line, the stronger the relationship.")

else:
    st.info("👈 Please upload an Excel file with a sheet named `education_career_success`.")
