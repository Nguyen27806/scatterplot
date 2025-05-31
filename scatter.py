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

# Plot: GPA_Group on x-axis, color by Salary_Group
plt.figure(figsize=(10, 6))
sns.stripplot(x="GPA_Group", y="Starting_Salary", hue="Salary_Group", data=df,
              dodge=True, jitter=True, palette="Set2", alpha=0.7)
plt.xlabel("GPA Group")
plt.ylabel("Starting Salary")
plt.title("")  # No title
plt.grid(True)
plt.legend(title="Salary Group", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
