import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Education & Career Success Dashboard", layout="wide", page_icon="📊")
st.title("📊 Education & Career Success Dashboard")

# === Caching and shared data ===
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# === SECTION 1: Career Path Sunburst ===
with st.expander("🌞 Career Path Sunburst", expanded=True):
    sunburst_df = df.copy()

    def categorize_salary(salary):
        if salary < 30000:
            return '<30K'
        elif salary < 50000:
            return '30K–50K'
        elif salary < 70000:
            return '50K–70K'
        else:
            return '70K+'

    sunburst_df['Salary_Group'] = sunburst_df['Starting_Salary'].apply(categorize_salary)

    sunburst_data = sunburst_df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')
    total_count = sunburst_data['Count'].sum()
    sunburst_data['Percentage'] = (sunburst_data['Count'] / total_count * 100).round(2)

    ent_totals = sunburst_data.groupby('Entrepreneurship')['Count'].sum()
    sunburst_data['Ent_Label'] = sunburst_data['Entrepreneurship'].map(
        lambda x: f"{x}<br>{round(ent_totals[x] / total_count * 100, 2)}%"
    )

    field_totals = sunburst_data.groupby(['Entrepreneurship', 'Field_of_Study'])['Count'].sum()
    sunburst_data['Field_Label'] = sunburst_data.apply(
        lambda row: f"{row['Field_of_Study']}<br>{round(field_totals[(row['Entrepreneurship'], row['Field_of_Study'])] / total_count * 100, 2)}%",
        axis=1
    )

    sunburst_data['Salary_Label'] = sunburst_data['Salary_Group'] + '<br>' + sunburst_data['Percentage'].astype(str) + '%'
    sunburst_data['Ent_Field'] = sunburst_data['Entrepreneurship'] + " - " + sunburst_data['Field_of_Study']

    yes_colors = {
        'Engineering': '#aedea7',
        'Business': '#dbf1d5',
        'Arts': '#0c7734',
        'Computer Science': '#73c375',
        'Medicine': '#00441b',
        'Law': '#f7fcf5',
        'Mathematics': '#37a055'
    }

    no_colors = {
        'Engineering': '#005b96',
        'Business': '#03396c',
        'Arts': '#009ac7',
        'Computer Science': '#8ed2ed',
        'Medicine': '#b3cde0',
        'Law': '#5dc4e1',
        'Mathematics': '#0a70a9'
    }

    # Tạo color_map: vòng trong (Ent_Label) màu vàng, vòng giữa (Ent_Field) giữ như cũ
    color_map = {}

    # Màu vàng cho Yes / No (vòng trong)
    for status in ['Yes', 'No']:
        label = f"{status}<br>{round(ent_totals[status] / total_count * 100, 2)}%"
        color_map[label] = '#FFD700'

    # Màu riêng cho từng ngành trong vòng giữa
    for field, color in yes_colors.items():
        color_map[f"Yes - {field}"] = color
    for field, color in no_colors.items():
        color_map[f"No - {field}"] = color

    fig1 = px.sunburst(
        sunburst_data,
        path=['Ent_Label', 'Field_Label', 'Salary_Label'],
        values='Count',
        color='Ent_Field',  # dùng vòng giữa để gán màu
        color_discrete_map=color_map,
        custom_data=['Percentage'],
        title='Career Path Insights: Education, Salary & Entrepreneurship'
    )

    fig1.update_traces(
        insidetextorientation='radial',
        maxdepth=2,
        branchvalues="total",
        textinfo='label+text',
        hovertemplate="<b>%{label}</b><br>Value: %{value}<br>"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.markdown("### 💡 How to use")
        st.markdown("""
- **Inner ring**: Entrepreneurship  
- **Middle**: Field of Study  
- **Outer**: Salary group  
- Labels include percentage share  
- Click to zoom into segments  
        """)

with st.expander("📊 Entrepreneurship by Age & Job Level", expanded=True):
    job_df = df[df['Entrepreneurship'].isin(['Yes', 'No'])].copy()
    grouped = job_df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
    grouped['Percentage'] = grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

    st.sidebar.title("Filters")
    job_levels = sorted(grouped['Current_Job_Level'].unique())
    selected_levels = st.sidebar.multiselect("Select Job Levels", job_levels, default=job_levels)
    age_min, age_max = int(grouped['Age'].min()), int(grouped['Age'].max())
    age_range = st.sidebar.slider("Select Age Range", min_value=age_min, max_value=age_max, value=(age_min, age_max))
    selected_statuses = st.sidebar.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'])

    filtered = grouped[
        (grouped['Current_Job_Level'].isin(selected_levels)) &
        (grouped['Entrepreneurship'].isin(selected_statuses)) &
        (grouped['Age'].between(age_range[0], age_range[1]))
    ]

    color_map = {'Yes': '#FFD700', 'No': '#004080'}
    level_order = ['Entry', 'Executive', 'Mid', 'Senior']
    visible_levels = [lvl for lvl in level_order if lvl in selected_levels]

    for level in visible_levels:
        data = filtered[filtered['Current_Job_Level'] == level]
        if data.empty:
            st.write(f"### {level} – No data available")
            continue

        ages = sorted(data['Age'].unique())
        chart_width = max(400, min(1200, 50 * len(ages) + 100))

        # --- Stacked Bar Chart ---
        fig_bar = px.bar(
            data, x='Age', y='Percentage', color='Entrepreneurship', barmode='stack',
            color_discrete_map=color_map, height=450, width=chart_width,
            title=f"{level} Level – Entrepreneurship by Age (%)"
        )

        for status in ['Yes', 'No']:
            subset = data[data['Entrepreneurship'] == status]
            for _, row in subset.iterrows():
                y_pos = row['Percentage'] / 2 if status == 'No' else 1 - (row['Percentage'] / 2)
                fig_bar.add_annotation(
                    x=row['Age'],
                    y=y_pos,
                    text=f"{row['Percentage']:.0%}",
                    showarrow=False,
                    font=dict(color="white", size=12),
                    xanchor="center",
                    yanchor="middle"
                )

        fig_bar.update_layout(
            margin=dict(t=40, l=40, r=40, b=40),
            xaxis_tickangle=90,
            bargap=0.1,
            yaxis_tickformat=".0%",
            yaxis_title="Percentage",
            legend_title_text="Entrepreneurship"
        )

        # --- Line Chart (instead of Area) ---
        fig_line = px.line(
            data, x='Age', y='Count', color='Entrepreneurship', markers=True,
            color_discrete_map=color_map, height=450, width=chart_width,
            title=f"{level} Level – Entrepreneurship by Age (Count)"
        )
        fig_line.update_layout(
            hovermode='x unified',
            xaxis_title="Age",
            yaxis_title="Count",
            legend_title_text="Entrepreneurship",
            margin=dict(t=40, l=40, r=40, b=40)
        )
        fig_line.update_traces(line=dict(width=2), marker=dict(size=8))

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            st.plotly_chart(fig_line, use_container_width=True)

