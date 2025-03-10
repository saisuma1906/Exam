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

# 1. **Total Applications, Admissions, and Enrollments per Term**
st.subheader(f"Total Applications, Admissions, and Enrollments for {term_selection} Term")
term_data = data[data['Term'] == term_selection]

total_apps = term_data['Applications'].sum()
total_admitted = term_data['Admitted'].sum()
total_enrolled = term_data['Enrolled'].sum()

st.metric("Total Applications", f"{total_apps:,}")
st.metric("Total Admissions", f"{total_admitted:,}")
st.metric("Total Enrolled", f"{total_enrolled:,}")

# 2. **Retention Rate Trends Over Time**
st.subheader("Retention Rate Trends Over Time")
retention_data = data.groupby('Year')['Retention Rate (%)'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=retention_data, x='Year', y='Retention Rate (%)', ax=ax)
ax.set_title("Retention Rate Trends Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Retention Rate (%)")
st.pyplot(fig)

# 3. **Student Satisfaction Scores Over Time** - Using a Bar Plot
st.subheader("Student Satisfaction Scores Over Time (Bar Plot)")
satisfaction_data = data.groupby('Year')['Student Satisfaction (%)'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=satisfaction_data, x='Year', y='Student Satisfaction (%)', ax=ax, palette='viridis')
ax.set_title("Student Satisfaction Scores Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Satisfaction (%)")
st.pyplot(fig

# 4. **Enrollment Breakdown by Department**
st.subheader(f"Enrollment Breakdown by Department ({term_selection} Term)")
department_enrollment = term_data[['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']].sum()

fig, ax = plt.subplots(figsize=(8, 8))
department_enrollment.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90, colors=sns.color_palette("Set2"))
ax.set_title(f"Enrollment Distribution by Department - {term_selection} Term")
st.pyplot(fig)

# 5. **Comparison Between Spring vs. Fall Term Trends** - Using Stacked Bar Chart
st.subheader("Comparison Between Spring vs. Fall Term Trends (Stacked Bar Chart)")
term_comparison_data = data.groupby(['Year', 'Term'])[['Applications', 'Admitted', 'Enrolled']].sum().reset_index()

# Pivot the data for stacking
term_comparison_pivot = term_comparison_data.pivot_table(index='Year', columns='Term', values=['Applications', 'Admitted', 'Enrolled'])

fig, ax = plt.subplots(figsize=(10, 6))
term_comparison_pivot['Applications'].plot(kind='bar', stacked=True, ax=ax, color=['#66b3ff', '#ff9999'])
ax.set_title("Applications Over Time (Spring vs Fall)")
ax.set_xlabel("Year")
ax.set_ylabel("Applications")
st.pyplot(fig)

# 3. **Heatmap for Student Satisfaction Scores by Year and Term**
st.subheader("Heatmap: Student Satisfaction by Year and Term")
heatmap_data = data.pivot_table(index='Year', columns='Term', values='Student Satisfaction (%)', aggfunc='mean')

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', ax=ax, cbar_kws={'label': 'Satisfaction (%)'})
ax.set_title("Student Satisfaction Scores Heatmap (Year vs Term)")
st.pyplot(fig)
# Plot retention rates
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=department_comparison_data, x='Year', y='Retention Rate (%)', ax=ax)
ax.set_title("Retention Rate Trends Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Retention Rate (%)")
st.pyplot(fig)

# Plot satisfaction scores
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=department_comparison_data, x='Year', y='Student Satisfaction (%)', ax=ax)
ax.set_title("Student Satisfaction Trends Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Satisfaction (%)")
st.pyplot(fig)

# Key Findings & Insights
st.subheader("Key Findings and Actionable Insights")
st.write("""
    - **Total Applications, Admissions, and Enrollments**: Visualize trends in admissions, helping to identify peak periods.
    - **Retention Rate Trends**: Analyze retention rates over the years to see the overall success of keeping students enrolled.
    - **Satisfaction Scores**: Show satisfaction trends, which could point to areas needing attention for improving student experience.
    - **Department Enrollment Breakdown**: Quickly visualize the distribution of enrollments by department to identify growing or shrinking areas.
    - **Term Comparison**: Identify whether Spring or Fall terms tend to have more applications, admissions, and enrollments.
    - **Trends Across Departments**: Compare how enrollments, retention, and satisfaction evolve across departments.
""")
