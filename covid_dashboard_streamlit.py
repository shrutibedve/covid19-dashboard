import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load and clean data (same as before)
data = pd.read_csv("owid-covid-data.csv")
data = data[['location', 'date', 'total_cases', 'total_deaths']]
data = data[~data['location'].isin(['World', 'International'])]
data['date'] = pd.to_datetime(data['date'])
data = data.dropna(subset=['total_cases', 'total_deaths'])

# Sort data to ensure proper calculation
data = data.sort_values(['location', 'date'])

# Calculate new cases and deaths for each country
data['new_cases'] = data.groupby('location')['total_cases'].diff()
data['new_deaths'] = data.groupby('location')['total_deaths'].diff()

# Fill missing values with 0
data[['new_cases', 'new_deaths']] = data[['new_cases', 'new_deaths']].fillna(0)

# Streamlit app starts here
st.title("COVID-19 Data Dashboard")

# Dropdown menu for countries
country = st.selectbox("Select a country", options=data['location'].unique())

# Filter data for selected country
country_data = data[data['location'] == country]

# Get min and max date and convert to Python date
min_date = country_data['date'].min().date()
max_date = country_data['date'].max().date()

# Create a date range slider
start_date, end_date = st.slider(
    "Select date range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

# Filter by selected date range (convert column to .date too)
country_data = country_data[
    (country_data['date'].dt.date >= start_date) &
    (country_data['date'].dt.date <= end_date)
]

# Filter data for selected country
country_data = data[data['location'] == country]

# Plot graph
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(country_data['date'], country_data['total_cases'], label='Total Cases', color='blue')
ax.plot(country_data['date'], country_data['total_deaths'], label='Total Deaths', color='red')

ax.set_xlabel("Date")
ax.set_ylabel("Count")
ax.set_title(f"COVID-19 Cases and Deaths in {country}")
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Show plot in Streamlit app
st.pyplot(fig)

# Plot new daily cases and deaths
st.subheader(f"Daily New Cases and Deaths in {country}")

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(country_data['date'], country_data['new_cases'], label='New Cases', color='orange')
ax2.plot(country_data['date'], country_data['new_deaths'], label='New Deaths', color='purple')

ax2.set_xlabel("Date")
ax2.set_ylabel("Count")
ax2.set_title(f"Daily COVID-19 Trends in {country}")
ax2.legend()
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig2)

# Show data table for selected country and date range
st.subheader(f"Data Table for {country}")
st.dataframe(country_data[['date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']].reset_index(drop=True))

#Run it in terminal using:
#  streamlit run covid_dashboard_streamlit.py
