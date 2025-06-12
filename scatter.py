import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Cấu hình layout
st.set_page_config(page_title="Heatmap Entrepreneurship", layout="centered")
st.title("🔥 Tỷ lệ Khởi nghiệp theo Tuổi và Giới tính")

# Load dữ liệu từ .xlsx
@st.cache_data
def load_data():
    file_path = "education_career_success.xlsx"
    if not os.path.exists(file_path):
        st.error(f"❌ File '{file_path}' không tồn tại.")
        st.stop()
    df = pd.read_excel(file_path)
    df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]
    df = df[df['Gender'].notna()]
    df['Age'] = df['Age'].round()  # làm tròn tuổi để dễ nhóm heatmap
    return df

df = load_data()

# Sidebar: lọc Job Level
st.sidebar.header("🎯 Bộ lọc")
job_levels = sorted(df['Current_Job_Level'].dropna().unique())

if not job_levels:
    st.warning("⚠️ Không có Job Level nào trong dữ liệu.")
    st.stop()

selected_level = st.sidebar.selectbox("Chọn Job Level", job_levels, index=0)

# Lọc dữ liệu theo Job Level
df_filtered = df[df['Current_Job_Level'] == selected_level]

# Tính tỷ lệ khởi nghiệp theo Age & Gender
heat_df = (
    df_filtered.groupby(['Age', 'Gender'])['Entrepreneurship']
    .apply(lambda x: (x == 'Yes').mean())
    .reset_index(name='Entrepreneurship_Rate')
)

# Vẽ Heatmap
fig = px.density_heatmap(
    heat_df,
    x='Age',
    y='Gender',
    z='Entrepreneurship_Rate',
    color_continuous_scale='Viridis',
    title=f"🔥 Tỷ lệ Khởi nghiệp – {selected_level} Level",
    labels={'Entrepreneurship_Rate': 'Tỷ lệ Khởi nghiệp'},
    height=400,
    width=600
)

fig.update_layout(
    margin=dict(t=50, l=40, r=40, b=40),
    xaxis_title="Tuổi",
    yaxis_title="Giới tính",
    coloraxis_colorbar=dict(title="Khởi nghiệp", tickformat=".0%")
)
fig.update_traces(contours_coloring="none")

# Hiển thị biểu đồ
st.plotly_chart(fig, use_container_width=True)
