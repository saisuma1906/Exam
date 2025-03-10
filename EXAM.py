import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset from GitHub repository (Replace with your actual raw URL)
file_url = "https://raw.githubusercontent.com/your-username/your-repository/main/university_student_dashboard_data.csv"
df = pd.read_csv(file_url)

# Check and clean column names (Remove any leading/trailing spaces)
df.columns = [col.strip() for col in df.columns]

# Display the column names to check
st.write("Column names in dataset:", df.columns)

# Streamlit layout
st.set_page_config(page_title="University Admissions and Student Satisfaction Dashboard", layout="wide")
st.title("University Admissions and Student Satisfaction Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

# Filters based on 'Year' and 'Term' columns
term_filter = st.sidebar.multiselect("Select Terms", df['Term'].unique(), default=df['Term'].unique())
year_filter = st.sidebar.slider("Select Year Range", min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=(int(df['Year'].min()), int(df['Year'].max())))

# Filter dataset based on selected filters
filtered_data = df[(df['Term'].isin(term_filter)) & 
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

# Enrollment Breakdown by Department (Engineering, Business, Arts, Science)
st.header("Enrollment Breakdown by Department")
dept_columns = ['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']
enrollment_data = filtered_data[['Year'] + dept_columns].set_index('Year').stack().reset_index()
enrollment_data.columns = ['Year', 'Department', 'Enrolled']

# Plot Enrollment Breakdown by Department
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
sns.lineplot(data=term_comparison, x='Year', y='Enrolled', hue='Term', marker='^', label="Enrollments", ax=ax)
plt.title("Comparison Between Spring vs. Fall Term Trends")
plt.xlabel("Year")
plt.ylabel("Count")
plt.legend(title="Metrics")
st.pyplot(fig)

# Compare Trends Between Retention Rates, Satisfaction Levels, and Departments
st.header("Compare Trends Between Retention Rates, Satisfaction Levels, and Departments")

# Create a line plot for retention and satisfaction rates by department
dept_comparison = filtered_data.groupby(['Year'])[['Retention Rate (%)', 'Student Satisfaction (%)']].mean().reset_index()

# Plot Retention Rates and Satisfaction Scores
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=dept_comparison, x='Year', y='Retention Rate (%)', marker='o', label="Retention Rate", ax=ax)
sns.lineplot(data=dept_comparison, x='Year', y='Student Satisfaction (%)', marker='s', label="Satisfaction Score", ax=ax)
plt.title("Retention Rates and Satisfaction Scores")
plt.xlabel("Year")
plt.ylabel("Value (%) / Score")
plt.legend(title="Metrics")
st.pyplot(fig)

# Key Findings and Actionable Insights
st.header("Key Findings and Actionable Insights")
