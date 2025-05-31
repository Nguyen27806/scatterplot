import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = "/mnt/data/education_career_success.xlsx"
df = pd.read_excel(file_path, sheet_name="education_career_success")

# Group GPA
gpa_bins = [2.0, 2.5, 3.0, 3.5, 4.0]
gpa_labels = ["2.0–2.5", "2.5–3.0", "3.0–3.5", "3.5–4.0"]
df["GPA_Group"] = pd.cut(df["University_GPA"], bins=gpa_bins, labels=gpa_labels, include_lowest=True)

# Group Starting Salary
salary_bins = [0, 30000, 50000, 70000, 90000, float("inf")]
salary_labels = ["<30K", "30K–50K", "50K–70K", "70K–90K", ">90K"]
df["Salary_Group"] = pd.cut(df["Starting_Salary"], bins=salary_bins, labels=salary_labels, include_lowest=True)

# Count the combinations
group_counts = df.groupby(["GPA_Group", "Salary_Group"]).size().reset_index(name="Count")

# Plot as heatmap
pivot_table = group_counts.pivot(index="Salary_Group", columns="GPA_Group", values="Count")

plt.figure(figsize=(8, 6))
sns.heatmap(pivot_table, annot=True, fmt="d", cmap="YlGnBu", cbar=False)
plt.xlabel("GPA Group")
plt.ylabel("Salary Group")
plt.title("Heatmap: Number of Students by GPA and Salary Group")
plt.tight_layout()
plt.show()
