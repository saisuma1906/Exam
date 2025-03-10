import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
@st.cache
def load_data():
    data = pd.read_csv('university_student_dashboard_data.csv')
    data['Year'] = pd.to_datetime(data['Year'], format='%Y')
    return data

data = load_data()

# Sidebar for user selection
st.sidebar.title("University Dashboard")
term_selection = st.sidebar.selectbox("Select Term", ['Spring', 'Fall'])
department_selection = st.sidebar.selectbox("Select Department", ['Engineering', 'Business', 'Arts', 'Science'])

# Metrics & KPIs
st.title("University Dashboard")
st.header("Admissions, Retention, and Satisfaction Insights")

# Total applications, admissions, and enrollments per term
total_apps = data[data['Term'] == term_selection]['Applications'].sum()
total_admitted = data[data['Term'] == term_selection]['Admitted'].sum()
total_enrolled = data[data['Term'] == term_selection]['Enrolled'].sum()

st.metric("Total Applications", f"{total_apps:,}")
st.metric("Total Admissions", f"{total_admitted:,}")
st.metric("Total Enrolled", f"{total_enrolled:,}")

# Retention rate trends over time
st.subheader("Retention Rate Trends Over Time")
retention_data = data.groupby('Year')['Retention Rate (%)'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=retention_data, x='Year', y='Retention Rate (%)', ax=ax)
ax.set_title("Retention Rate Trends")
ax.set_xlabel("Year")
ax.set_ylabel("Retention Rate (%)")
st.pyplot(fig)

# Student satisfaction scores over the years
st.subheader("Student Satisfaction Scores Over Time")
satisfaction_data = data.groupby('Year')['Student Satisfaction (%)'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=satisfaction_data, x='Year', y='Student Satisfaction (%)', ax=ax)
ax.set_title("Student Satisfaction Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Satisfaction (%)")
st.pyplot(fig)

# Enrollment breakdown by department
st.subheader(f"Enrollment Breakdown by {department_selection}")
department_data = data.groupby('Year')[f'{department_selection} Enrolled'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=department_data, x='Year', y=f'{department_selection} Enrolled', ax=ax)
ax.set_title(f"{department_selection} Enrollment Over Time")
ax.set_xlabel("Year")
ax.set_ylabel(f"{department_selection} Enrolled")
st.pyplot(fig)

# Comparison between Spring vs Fall term trends
st.subheader("Comparison between Spring vs Fall Term Trends")
term_comparison_data = data.groupby(['Year', 'Term'])[['Applications', 'Admitted', 'Enrolled']].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=term_comparison_data, x='Year', y='Applications', hue='Term', ax=ax)
ax.set_title("Applications Over Time (Spring vs Fall)")
ax.set_xlabel("Year")
ax.set_ylabel("Applications")
st.pyplot(fig)

# Compare trends between departments, retention rates, and satisfaction levels
st.subheader("Department Trends Comparison")
department_comparison_data = data[['Year', 'Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']]
department_comparison_data = department_comparison_data.set_index('Year')

fig, ax = plt.subplots(figsize=(10, 6))
department_comparison_data.plot(kind='line', ax=ax)
ax.set_title("Department Enrollment Trends Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Enrollment")
st.pyplot(fig)

# Key Findings & Insights
st.subheader("Key Findings and Actionable Insights")
st.write("""
    - The total applications, admissions, and enrollments can help identify seasonal peaks and valleys.
    - Retention rate trends reveal the stability of the student body over the years.
    - Satisfaction scores are important for identifying areas for improvement in the student experience.
    - Department enrollment trends indicate which areas are growing or declining in popularity.
    - The comparison of Spring and Fall term trends can show differences in student behavior and course preferences.
""")

