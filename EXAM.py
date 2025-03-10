import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('university_student_dashboard_data.csv')

# Clean column names (strip extra spaces)
df.columns = df.columns.str.strip()

# Sidebar for filters
st.sidebar.header("Filters")
terms = st.sidebar.multiselect("Select Term(s)", df['Term'].dropna().unique())
years = st.sidebar.multiselect("Select Year(s)", df['Year'].dropna().unique())

# Filter data based on user input
filtered_data = df[
    (df['Term'].isin(terms) if terms else True) &
    (df['Year'].isin(years) if years else True)
]

# Display filtered data
st.write(filtered_data)

# Show key metrics
st.header("Key Metrics")
total_applications = filtered_data['Applications'].sum()
total_admitted = filtered_data['Admitted'].sum()
total_enrolled = filtered_data['Enrolled'].sum()
avg_retention_rate = filtered_data['Retention Rate (%)'].mean()
avg_satisfaction = filtered_data['Student Satisfaction (%)'].mean()

st.write(f"**Total Applications**: {total_applications}")
st.write(f"**Total Admitted**: {total_admitted}")
st.write(f"**Total Enrolled**: {total_enrolled}")
st.write(f"**Average Retention Rate**: {avg_retention_rate:.2f}%")
st.write(f"**Average Student Satisfaction**: {avg_satisfaction:.2f}%")

# Visualization 1: Total Enrolled by Department
department_columns = ['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']
department_data = filtered_data[department_columns].sum()

fig, ax = plt.subplots()
department_data.plot(kind='bar', ax=ax, color=['blue', 'green', 'red', 'purple'])
ax.set_title("Total Enrolled by Department")
ax.set_xlabel("Department")
ax.set_ylabel("Number of Enrolled Students")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Visualization 2: Retention Rate Trend Over Time
fig, ax = plt.subplots()
sns.lineplot(data=filtered_data, x='Year', y='Retention Rate (%)', ax=ax, marker='o')
ax.set_title("Retention Rate Trend Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Retention Rate (%)")
st.pyplot(fig)

# Visualization 3: Student Satisfaction Trend Over Time
fig, ax = plt.subplots()
sns.lineplot(data=filtered_data, x='Year', y='Student Satisfaction (%)', ax=ax, marker='o', color='orange')
ax.set_title("Student Satisfaction Trend Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Satisfaction (%)")
st.pyplot(fig)

# Visualization 4: Comparison of Enrollment by Term
term_enrollment_data = filtered_data.groupby('Term')[['Applications', 'Admitted', 'Enrolled']].sum()

fig, ax = plt.subplots()
term_enrollment_data.plot(kind='bar', ax=ax)
ax.set_title("Comparison of Applications, Admissions, and Enrollments by Term")
ax.set_xlabel("Term")
ax.set_ylabel("Count")
plt.xticks(rotation=0)
st.pyplot(fig)

# Visualization 5: Retention Rate vs Satisfaction per Department
department_data = filtered_data[['Retention Rate (%)', 'Student Satisfaction (%)', 'Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']]

fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=department_data, x='Retention Rate (%)', y='Student Satisfaction (%)', hue='Engineering Enrolled', size='Engineering Enrolled', sizes=(20, 200), ax=ax)
ax.set_title("Retention Rate vs Satisfaction per Department")
ax.set_xlabel("Retention Rate (%)")
ax.set_ylabel("Student Satisfaction (%)")
st.pyplot(fig)
