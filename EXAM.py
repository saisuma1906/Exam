import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv('university_student_dashboard_data.csv')

# Set up Streamlit layout
st.set_page_config(page_title="University Admissions Dashboard", layout="wide")

# Dashboard Title
st.title("University Admissions and Student Satisfaction Dashboard")

# Sidebar for Filters
st.sidebar.header("Filters")
department_filter = st.sidebar.multiselect("Select Departments", data['department'].unique(), default=data['department'].unique())
term_filter = st.sidebar.multiselect("Select Terms", data['term'].unique(), default=data['term'].unique())
year_filter = st.sidebar.slider("Select Year Range", min_value=int(data['year'].min()), max_value=int(data['year'].max()), value=(int(data['year'].min()), int(data['year'].max())))

# Filter data based on user selection
filtered_data = data[(data['department'].isin(department_filter)) & 
                     (data['term'].isin(term_filter)) & 
                     (data['year'].between(year_filter[0], year_filter[1]))]

# KPI Section
st.header("Key Performance Indicators (KPIs)")

# Total applications, admissions, and enrollments per term
total_apps = filtered_data.groupby('term')['applications'].sum()
total_adm = filtered_data.groupby('term')['admissions'].sum()
total_enr = filtered_data.groupby('term')['enrollments'].sum()

# Display KPIs as a table
kpi_data = pd.DataFrame({
    'Total Applications': total_apps,
    'Total Admissions': total_adm,
    'Total Enrollments': total_enr
})

st.write(kpi_data)

# Retention Rate Trends Over Time
st.header("Retention Rate Trends Over Time")
retention_data = filtered_data.groupby(['year', 'term'])['retention_rate'].mean().reset_index()

# Plot retention trends
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=retention_data, x='year', y='retention_rate', hue='term', marker='o', ax=ax)
plt.title("Retention Rate Trends Over Time")
plt.xlabel("Year")
plt.ylabel("Retention Rate (%)")
st.pyplot(fig)

# Student Satisfaction Scores Over the Years
st.header("Student Satisfaction Scores Over the Years")
satisfaction_data = filtered_data.groupby(['year', 'term'])['satisfaction_score'].mean().reset_index()

# Plot satisfaction scores trends
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=satisfaction_data, x='year', y='satisfaction_score', hue='term', marker='o', ax=ax)
plt.title("Student Satisfaction Scores Over the Years")
plt.xlabel("Year")
plt.ylabel("Satisfaction Score")
st.pyplot(fig)

# Enrollment Breakdown by Department
st.header("Enrollment Breakdown by Department")
enrollment_data = filtered_data.groupby(['year', 'department'])['enrollments'].sum().reset_index()

# Plot Enrollment Breakdown
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=enrollment_data, x='year', y='enrollments', hue='department', ax=ax)
plt.title("Enrollment Breakdown by Department")
plt.xlabel("Year")
plt.ylabel("Number of Enrollments")
st.pyplot(fig)

# Comparison Between Spring vs. Fall Term Trends
st.header("Spring vs. Fall Term Trends")
term_comparison = filtered_data.groupby(['year', 'term'])[['applications', 'admissions', 'enrollments']].sum().reset_index()

# Plot Comparison
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=term_comparison, x='year', y='applications', hue='term', marker='o', label="Applications", ax=ax)
sns.lineplot(data=term_comparison, x='year', y='admissions', hue='term', marker='s', label="Admissions", ax=ax)
sns.lineplot(data=term_comparison, x='year', y='enrollments', hue='term', marker='^', label="Enrollments", ax=ax)
plt.title("Comparison Between Spring vs. Fall Term Trends")
plt.xlabel("Year")
plt.ylabel("Count")
plt.legend(title="Metrics")
st.pyplot(fig)

# Compare Trends Between Departments, Retention Rates, and Satisfaction Levels
st.header("Compare Trends Between Departments, Retention Rates, and Satisfaction Levels")

# Create a line plot for retention and satisfaction rates by department
dept_comparison = filtered_data.groupby(['year', 'department'])[['retention_rate', 'satisfaction_score']].mean().reset_index()

# Plot Retention Rates and Satisfaction Scores by Department
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=dept_comparison, x='year', y='retention_rate', hue='department', marker='o', label="Retention Rate", ax=ax)
sns.lineplot(data=dept_comparison, x='year', y='satisfaction_score', hue='department', marker='s', label="Satisfaction Score", ax=ax)
plt.title("Retention Rates and Satisfaction Scores by Department")
plt.xlabel("Year")
plt.ylabel("Value (%) / Score")
plt.legend(title="Metrics")
st.pyplot(fig)

# Key Findings and Actionable Insights
st.header("Key Findings and Actionable Insights")

# Display insights based on trends
if total_apps.max() > 10000:
    st.write("🔔 **Actionable Insight**: The university has seen a significant increase in applications, especially in certain terms. Focus on improving admissions efficiency during peak times.")
    
if retention_data['retention_rate'].mean() < 75:
    st.write("🔔 **Actionable Insight**: Retention rates are lower than expected. It might be valuable to focus on improving student support and engagement to reduce drop-out rates.")

if satisfaction_data['satisfaction_score'].mean() < 3.5:
    st.write("🔔 **Actionable Insight**: Student satisfaction is below average. Consider enhancing student services, academic offerings, and campus life to improve satisfaction.")

