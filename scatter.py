import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="GPA vs. Starting Salary", layout="centered", page_icon="📊")
st.title("📊 GPA vs. Starting Salary Scatter Plot")

# Upload hoặc dùng file mặc định
uploaded_file = st.file_uploader("Upload your Excel file (sheet: education_career_success)", type=["xlsx"])

@st.cache_data
def load_data(file=None):
    if file is not None:
        return pd.read_excel(file, sheet_name="education_career_success")
    else:
        return pd.read_excel("education_career_success.xlsx", sheet_name="education_career_success")

if uploaded_file or st.checkbox("Use default demo file instead"):
    df = load_data(uploaded_file)

    # Group GPA
    df["GPA_Group"] = pd.cut(
        df["University_GPA"],
        bins=[2.0, 2.5, 3.0, 3.5, 4.0],
        labels=["2.0–2.5", "2.5–3.0", "3.0–3.5", "3.5–4.0"],
        include_lowest=True
    )

    selected_gpa = st.selectbox("Select GPA Group", ["All"] + df["GPA_Group"].cat.categories.tolist())
    salary_min, salary_max = int(df["Starting_Salary"].min()), int(df["Starting_Salary"].max())
    salary_range = st.slider("Select Starting Salary Range", salary_min, salary_max, (salary_min, salary_max), 1000)

    # Filter
    mask = df["Starting_Salary"].between(*salary_range)
    if selected_gpa != "All":
        mask &= df["GPA_Group"] == selected_gpa
    filtered_df = df[mask]

    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(
        x='University_GPA',
        y='Starting_Salary',
        data=filtered_df,
        ax=ax,
        scatter_kws={'alpha': 0.7}
    )
    ax.set_xlabel('University GPA')
    ax.set_ylabel('Starting Salary')

    # Nền giống sunburst background (màu nhẹ, có lưới)
    fig.patch.set_facecolor('#eaf0f7')
    ax.set_facecolor('#eaf0f7')
    ax.grid(True, color='white', linewidth=2)
    ax.set_axisbelow(True)
    ax.set_xticks([2.0, 2.5, 3.0, 3.5, 4.0])
    ax.set_yticks(range(salary_min, salary_max + 1, 5000))

    st.pyplot(fig)

else:
    st.info("📁 Please upload an Excel file or tick 'Use default demo file'.")
