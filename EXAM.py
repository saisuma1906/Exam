import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('university_student_dashboard_data.csv')

# Set Streamlit page title
st.set_page_config(page_title="University Dashboard", layout="wide")

# Dashboard Title
st.title("University Dashboard: Admissions, Retention, and Satisfaction")

# Sidebar for filters
st.sidebar.header("Filters")
terms = st.sidebar.multiselect("Select Term(s)", df['Term'].unique())
years = st.sidebar.multiselect("Select Year(s)", df['Year'].unique())
departments = st.sidebar.multiselect("Select Department(s)", df['Department'].unique())

# Filter data based on user input
filtered_data = df[
    (df['Term'].isin(terms) if terms else True) &
    (df['Year'].isin(years) if years else True) &
    (df['Department'].isin(departments) if departments else True)
]

# Metrics & KPIs
st.header("Metrics & KPIs")

# Total Applications, Admissions, and Enrollments per Term
st.subheader("Total Applications, Admissions, and Enrollments")
applications = filtered_data.groupby('Term')['Applications'].sum()
admissions = filtered_data.groupby('Term')['Admissions'].sum()
enrollments = filtered_data.groupby('Term')['Enrollments'].sum()

metrics = pd.DataFrame({
    'Applications': applications,
    'Admissions': admissions,
    'Enrollments': enrollments
})

st.write(metrics)

# Retention Rate Trends over Time
st.subheader("Retention Rate Trends")
retention_rate = filtered_data.groupby('Year')['Retention Rate'].mean()
st.line_chart(retention_rate)

# Student Satisfaction Scores Over the Years
st.subheader("Student Satisfaction Scores Over the Years")
satisfaction_scores = filtered_data.groupby('Year')['Satisfaction Score'].mean()
st.line_chart(satisfaction_scores)

# Enrollment Breakdown by Department
st.subheader("Enrollment Breakdown by Department")
department_enrollments = filtered_data.groupby('Department')['Enrollments'].sum()
st.bar_chart(department_enrollments)

# Comparison between Spring vs Fall Term Trends
st.subheader("Comparison: Spring vs Fall Term")
spring_fall_comparison = filtered_data[filtered_data['Term'].isin(['Spring', 'Fall'])]
spring_fall_comparison = spring_fall_comparison.groupby(['Term', 'Year'])['Enrollments'].sum().unstack()
st.line_chart(spring_fall_comparison)

# Compare Trends Between Departments, Retention Rates, and Satisfaction Levels
st.subheader("Department Comparison: Retention Rates & Satisfaction Levels")
department_comparison = filtered_data.groupby('Department')[['Retention Rate', 'Satisfaction Score']].mean()
st.write(department_comparison)

# Key Findings
st.header("Key Findings and Actionable Insights")
st.write("""
- Use the visualizations to compare trends in admissions and enrollments across terms and departments.
- Identify patterns in retention rates over time and make adjustments to improve them.
- Analyze student satisfaction scores across years and departments to identify areas for improvement.
""")
