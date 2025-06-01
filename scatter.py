import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("🎓 University GPA vs. Starting Salary")

# 🚫 Bỏ file_uploader, dùng dữ liệu giả lập cho test/demo
uploaded_file = None  # comment this out when using real file

# Sample data để test
df = pd.DataFrame({
    "University_GPA": [2.2, 2.8, 3.1, 3.7, 3.9, 3.3, 2.5],
    "Starting_Salary": [30000, 35000, 42000, 48000, 55000, 39000, 33000]
})

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
mask = (df["Starting_Salary"].between(*salary_range))
if selected_gpa != "All":
    mask &= (df["GPA_Group"] == selected_gpa)
filtered_df = df[mask]

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
sns.regplot(x='University_GPA', y='Starting_Salary', data=filtered_df, ax=ax, scatter_kws={'alpha': 0.7})
ax.set_xlabel('University GPA')
ax.set_ylabel('Starting Salary')

# Custom background
fig.patch.set_facecolor('#eaf0f7')
ax.set_facecolor('#eaf0f7')
ax.grid(True, color='white', linewidth=2)
ax.set_axisbelow(True)
ax.set_xticks([2.0, 2.5, 3.0, 3.5, 4.0])
ax.set_yticks(range(salary_min, salary_max + 1000, 5000))

st.pyplot(fig)
