import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
# Display the column names to check if 'Department' exists
st.write("Column names in dataset:", df.columns)
# Streamlit layout
st.set_page_config(page_title="University Admissions and Student Satisfaction Dashboard", layout="wide")
st.title("University Admissions and Student Satisfaction Dashboard")
# Sidebar filters
st.sidebar.header("Filters")
# Check if 'Department' column exists and use it, otherwise print an error message
if 'Department' in df.columns:
    department_filter = st.sidebar.multiselect("Select Departments", df['Department'].unique(), default=df['Department'].unique())
else:
    st.error("The 'Department' column is not found in the dataset. Please check the column name.")

term_filter = st.sidebar.multiselect("Select Terms", df['Term'].unique(), default=df['Term'].unique())
year_filter = st.sidebar.slider("Select Year Range", min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=(int(df['Year'].min()), int(df['Year'].max())))
# Filter dataset based on selected filters
filtered_data = df[(df['Department'].isin(department_filter)) & 
                   (df['Term'].isin(term_filter)) & 
                   (df['Year'].between(year_filter[0], year_filter[1]))]
# KPI Section
st.header("Key Performance Indicators (KPIs)")
# Total applications, admissions, and enrollments per term
total_apps = filtered_data.groupby('Term')['Applications'].sum()
total_adm = filtered_data.groupby('Term')['Admitted'].sum()
total_enr = filtered_data.groupby('Term')['Enrolled'].sum()
# Display KPIs as a table
kpi_data = pd.DataFrame({
    'Total Applications': total_apps,
    'Total Admissions': total_adm,
    'Total Enrollments': total_enr
})
st.write(kpi_data)
# Retention Rate Trends Over Time
st.header("Retention Rate Trends Over Time")
retention_data = filtered_data.groupby(['Year', 'Term'])['Retention Rate (%)'].mean().reset_index()
# Plot retention trends
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=retention_data, x='Year', y='Retention Rate (%)', hue='Term', marker='o', ax=ax)
plt.title("Retention Rate Trends Over Time")
plt.xlabel("Year")
plt.ylabel("Retention Rate (%)")
st.pyplot(fig)
# Student Satisfaction Scores Over the Years
st.header("Student Satisfaction Scores Over the Years")
satisfaction_data = filtered_data.groupby(['Year', 'Term'])['Student Satisfaction (%)'].mean().reset_index()
# Plot satisfaction scores trends
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=satisfaction_data, x='Year', y='Student Satisfaction (%)', hue='Term', marker='o', ax=ax)
plt.title("Student Satisfaction Scores Over the Years")
plt.xlabel("Year")
plt.ylabel("Satisfaction Score (%)")
st.pyplot(fig)
# Enrollment Breakdown by Department
st.header("Enrollment Breakdown by Department")
enrollment_data = filtered_data.groupby(['Year', 'Department'])['Enrolled'].sum().reset_index()
# Plot Enrollment Breakdown
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=enrollment_data, x='Year', y='Enrolled', hue='Department', ax=ax)
plt.title("Enrollment Breakdown by Department")
plt.xlabel("Year")
plt.ylabel("Number of Enrollments")
st.pyplot(fig)
# Comparison Between Spring vs. Fall Term Trends
st.header("Spring vs. Fall Term Trends")
term_comparison = filtered_data.groupby(['Year', 'Term'])[['Applications', 'Admitted', 'Enrolled']].sum().reset_index()
# Plot Comparison
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=term_comparison, x='Year', y='Applications', hue='Term', marker='o', label="Applications", ax=ax)
sns.lineplot(data=term_comparison, x='Year', y='Admitted', hue='Term', marker='s', label="Admissions", ax=ax)
sns.lineplot(data=term_comparison, x='Year', y='Enrolled',
