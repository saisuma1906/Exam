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

# 1. **Total Applications, Admissions, and Enrollments per Term (Bar Chart)**
st.subheader(f"Total Applications, Admissions, and Enrollments for {term_selection} Term")
term_data = data[data['Term'] == term_selection]

total_apps = term_data['Applications'].sum()
total_admitted = term_data['Admitted'].sum()
total_enrolled = term_data['Enrolled'].sum()

# Bar plot for the metrics
fig, ax = plt.subplots(figsize=(10, 6))
metrics = ['Total Applications', 'Total Admissions', 'Total Enrolled']
values = [total_apps, total_admitted, total_enrolled]
sns.barplot(x=metrics, y=values, ax=ax, palette='Set2')
ax.set_title(f"Applications, Admissions, and Enrollments ({term_selection} Term)")
ax.set_ylabel("Count")
st.pyplot(fig)

# 2. **Retention Rate Trends Over Time (Area Plot)**
st.subheader("Retention Rate Trends Over Time (Area Plot)")
retention_data = data.groupby('Year')['Retention Rate (%)'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
ax.fill_between(retention_data['Year'], retention_data['Retention Rate (%)'], color='skyblue', alpha=0.5)
ax.set_title("Retention Rate Trends Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Retention Rate (%)")
st.pyplot(fig)

# 3. **Student Satisfaction Scores Over Time (Bar Plot)**
st.subheader("Student Satisfaction Scores Over Time")
satisfaction_data = data.groupby('Year')['Student Satisfaction (%)'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=satisfaction_data, x='Year', y='Student Satisfaction (%)', ax=ax, palette='viridis')
ax.set_title("Student Satisfaction Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Satisfaction (%)")
st.pyplot(fig)

# 4. **Enrollment Breakdown by Department (Pie Chart)**
st.subheader(f"Enrollment Breakdown by Department ({term_selection} Term)")
department_enrollment = term_data[['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']].sum()

fig, ax = plt.subplots(figsize=(8, 8))
department_enrollment.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90, colors=sns.color_palette("Set2"))
ax.set_title(f"Enrollment Distribution by Department - {term_selection} Term")
st.pyplot(fig)

# 5. **Comparison Between Spring vs. Fall Term Trends (Stacked Bar Chart)**
st.subheader("Comparison Between Spring vs. Fall Term Trends")
term_comparison_data = data.groupby(['Year', 'Term'])[['Applications', 'Admitted', 'Enrolled']].sum().reset_index()

# Pivot the data for stacking
term_comparison_pivot = term_comparison_data.pivot_table(index='Year', columns='Term', values=['Applications', 'Admitted', 'Enrolled'])

fig, ax = plt.subplots(figsize=(10, 6))
term_comparison_pivot['Applications'].plot(kind='bar', stacked=True, ax=ax, color=['#66b3ff', '#ff9999'])
ax.set_title("Applications Over Time (Spring vs Fall)")
ax.set_xlabel("Year")
ax.set_ylabel("Applications")
st.pyplot(fig)

# 6. **Compare Trends Between Departments, Retention Rates, and Satisfaction Levels (Heatmap)**
st.subheader("Compare Trends Between Departments, Retention Rates, and Satisfaction Levels")

# Department comparison for heatmap
department_comparison_data = data[['Year', 'Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled', 
                                   'Retention Rate (%)', 'Student Satisfaction (%)']]

# Plot heatmap for satisfaction and retention
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(department_comparison_data.corr(), annot=True, cmap='coolwarm', ax=ax, cbar_kws={'label': 'Correlation'})
ax.set_title("Correlation Heatmap Between Departments, Retention, and Satisfaction")
st.pyplot(fig)

# Key Findings & Insights
st.subheader("Key Findings and Actionable Insights")
st.write("""
    - **Bar Chart of Applications, Admissions, and Enrollments**: Provides an easy-to-read comparison of metrics for a specific term.
    - **Area Plot for Retention Rates**: Visualizes trends in retention rates over time, allowing for better understanding of student retention.
    - **Bar Plot for Satisfaction Scores**: Offers a clearer way to compare satisfaction scores by year.
    - **Pie Chart for Department Enrollment**: Displays the distribution of enrollments by department.
    - **Stacked Bar Chart for Term Comparison**: Highlights the differences in key metrics like applications and enrollments between the Spring and Fall terms.
    - **Heatmap for Departmental Trends and Correlations**: Helps identify relationships between different departments, retention rates, and satisfaction levels.
""")
