import pandas as pd

# load the covid dataset (holds all the COVID-19 data)
data = pd.read_csv("owid-covid-data.csv")

# keep only needed columns (removes unnecessary columns like population, vaccinations, etc.)
data = data[['location', 'date', 'total_cases', 'total_deaths']]

# remove rows that are not country data (Keep only rows where location is NOT World or International.)
data = data[~data['location'].isin(['World', 'International'])]

# convert date column to proper date format
data['date'] = pd.to_datetime(data['date'])

# remove rows with missing cases or deaths
data = data.dropna(subset=['total_cases', 'total_deaths'])

# check the first few rows
print(data.head())

import matplotlib.pyplot as plt

# ask user to type a country name
country = input("Enter a country name : ")

# filter data for that country
country_data = data[data['location'] == country]

# plot total cases and deaths over time
plt.figure(figsize=(10, 5))
plt.plot(country_data['date'], country_data['total_cases'], label='Total Cases', color='blue')
plt.plot(country_data['date'], country_data['total_deaths'], label='Total Deaths', color='red')

# add labels and title
plt.xlabel('Date')
plt.ylabel('Count')
plt.title(f'COVID-19 in {country}')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# show the graph
plt.show()

