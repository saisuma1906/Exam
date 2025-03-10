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

# 1. **Bar Chart: Comparison of applications, admissions, and enrollments over years**
st.subheader("Comparison of Applications, Admissions, and Enrollments Over Years")
comparison_data = data.groupby('Year')[['Applications', 'Admitted', 'Enrolled']].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
comparison_data.plot(kind='bar', x='Year', ax=ax)
ax.set_title("Applications, Admissions, and Enrollments Over Years")
ax.set_xlabel("Year")
ax.set_ylabel("Count")
st.pyplot(fig)

# 2. **Heatmap: Correlation matrix between numerical features**
st.subheader("Correlation Heatmap")
corr_data = data[['Retention Rate (%)', 'Student Satisfaction (%)', 'Applications', 'Admitted', 'Enrolled', 
                  'Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']]
corr_matrix = corr_data.corr()

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
ax.set_title("Correlation Heatmap")
st.pyplot(fig)

# 3. **Pie Chart: Enrollment Distribution by Department**
st.subheader(f"Enrollment Distribution by Department ({term_selection} Term)")
department_enrollment = data[data['Term'] == term_selection][['Engineering Enrolled', 'Business Enrolled', 
                                                             'Arts Enrolled', 'Science Enrolled']].sum()

fig, ax = plt.subplots(figsize=(8, 8))
department_enrollment.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90, colors=sns.color_palette("Set2"))
ax.set_title(f"Enrollment Distribution by Department - {term_selection} Term")
st.pyplot(fig)

# 4. **Area Chart: Cumulative Enrollment Trends Over Time by Department**
st.subheader("Cumulative Enrollment Trends by Department")
department_data_cumsum = data[['Year', 'Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']]
department_data_cumsum = department_data_cumsum.set_index('Year').cumsum()

fig, ax = plt.subplots(figsize=(10, 6))
department_data_cumsum.plot(kind='area', ax=ax, alpha=0.5)
ax.set_title("Cumulative Enrollment Trends Over Time by Department")
ax.set_xlabel("Year")
ax.set_ylabel("Cumulative Enrollments")
st.pyplot(fig)

# 5. **Box Plot: Distribution of Satisfaction Scores by Department**
st.subheader("Student Satisfaction Distribution by Department")
satisfaction_data = data[['Year', 'Student Satisfaction (%)', 'Engineering Enrolled', 'Business Enrolled', 
                          'Arts Enrolled', 'Science Enrolled']]

# Choose department based on the user's selection
department_col = f'{department_selection} Enrolled'
department_satisfaction_data = satisfaction_data[satisfaction_data[department_col] > 0]

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=department_satisfaction_data, x=department_selection, y="Student Satisfaction (%)", ax=ax)
ax.set_title(f"Student Satisfaction Distribution for {department_selection}")
ax.set_xlabel(department_selection)
ax.set_ylabel("Satisfaction (%)")
st.pyplot(fig)

# Key Findings & Insights
st.subheader("Key Findings and Actionable Insights")
st.write("""
    - **Bar Chart** shows the overall trends in admissions and enrollments.
    - **Heatmap** highlights relationships between different variables.
    - **Pie Chart** provides a quick glance at the share of enrollments in each department for the selected term.
    - **Area Chart** illustrates cumulative enrollment trends, which can indicate long-term growth in departments.
    - **Box Plot** helps to assess the distribution of student satisfaction across departments, highlighting outliers.
""")
