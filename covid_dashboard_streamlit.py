import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="COVID-19 Analytical Dashboard", layout="wide", page_icon="🦠")

@st.cache_data
def load_data():
    # Define columns we want to keep for a more analytical dashboard
    cols = ['location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'people_fully_vaccinated', 'population']
    
    # Load data directly from OWID repository to avoid 100MB+ file size limits during deployment
    data_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    data = pd.read_csv(data_url, usecols=lambda c: c in cols)
    
    # Remove aggregate regions to only keep actual countries
    data = data[~data['location'].isin(['World', 'International', 'High income', 'Upper middle income', 'Lower middle income', 'Low income', 'Europe', 'Asia', 'North America', 'South America', 'Africa', 'European Union'])]
    
    # Convert dates
    data['date'] = pd.to_datetime(data['date'])
    
    # Sort data for proper chronological analysis
    data = data.sort_values(['location', 'date'])
    
    # Calculate 7-day rolling averages for smoother trend analysis
    data['new_cases_7d_avg'] = data.groupby('location')['new_cases'].transform(lambda x: x.rolling(7, min_periods=1).mean())
    data['new_deaths_7d_avg'] = data.groupby('location')['new_deaths'].transform(lambda x: x.rolling(7, min_periods=1).mean())
    
    # Calculate per million metrics for fair comparison
    data['cases_per_million'] = (data['total_cases'] / data['population']) * 1_000_000
    
    return data

data = load_data()

# Header
st.title("🦠 Advanced COVID-19 Analytical Dashboard")
st.markdown("Explore pandemic trends, analyze daily metrics, and compare countries using this interactive tool.")

# Create tabs for different analytical views
tab1, tab2 = st.tabs(["📊 Deep Dive: Single Country", "🌍 Global Comparison"])

with tab1:
    st.header("Country Analytics")
    
    # Controls in columns
    ctrl_col1, ctrl_col2 = st.columns([1, 2])
    with ctrl_col1:
        country = st.selectbox("Select a country to analyze:", options=data['location'].dropna().unique(), index=225) # Default to a notable one if index exists, else just selected
    
    country_data_full = data[data['location'] == country]
    min_date = country_data_full['date'].min().date()
    max_date = country_data_full['date'].max().date()
    
    with ctrl_col2:
        start_date, end_date = st.slider(
            "Select analysis timeframe:",
            min_value=min_date, max_value=max_date,
            value=(min_date, max_date), format="YYYY-MM-DD"
        )
    
    # Filter data based on date
    country_data = country_data_full[
        (country_data_full['date'].dt.date >= start_date) & 
        (country_data_full['date'].dt.date <= end_date)
    ]
    
    # Top Level KPIs
    st.markdown("### Key Performance Indicators (Timeframe)")
    
    if not country_data.empty:
        latest_data = country_data.iloc[-1]
        
        # Calculate metrics difference (start to end of selected period)
        total_cases_period = country_data['new_cases'].sum()
        total_deaths_period = country_data['new_deaths'].sum()
        
        # Overall aggregates
        overall_cases = latest_data['total_cases']
        overall_deaths = latest_data['total_deaths']
        mortality_rate = (overall_deaths / overall_cases * 100) if overall_cases > 0 else 0
        vaccination_pct = (latest_data['people_fully_vaccinated'] / latest_data['population'] * 100) if pd.notna(latest_data['people_fully_vaccinated']) and latest_data['population'] > 0 else 0
        
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Total Cases (overall)", f"{overall_cases:,.0f}", f"+{total_cases_period:,.0f} in period")
        kpi2.metric("Total Deaths (overall)", f"{overall_deaths:,.0f}", f"+{total_deaths_period:,.0f} in period", delta_color="inverse")
        kpi3.metric("Case Fatality Rate", f"{mortality_rate:.2f}%")
        kpi4.metric("Fully Vaccinated", f"{vaccination_pct:.1f}%" if vaccination_pct > 0 else "N/A")
    
    st.divider()
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Cumulative Trend: Cases & Deaths")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(country_data['date'], country_data['total_cases'], label='Total Cases', color='#1f77b4', linewidth=2)
        ax.set_ylabel("Total Cases", color='#1f77b4')
        ax.tick_params(axis='y', labelcolor='#1f77b4')
        
        # Dual axis for deaths to see both scales clearly
        ax2 = ax.twinx()
        ax2.plot(country_data['date'], country_data['total_deaths'], label='Total Deaths', color='#d62728', linewidth=2)
        ax2.set_ylabel("Total Deaths", color='#d62728')
        ax2.tick_params(axis='y', labelcolor='#d62728')
        
        fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
        plt.title(f"Cumulative Trajectory in {country}")
        fig.autofmt_xdate(rotation=45)
        st.pyplot(fig)

    with col2:
        st.subheader("Daily Trends (with 7-Day Moving Avg)")
        fig2, ax = plt.subplots(figsize=(10, 5))
        
        # Scatter for raw daily cases to show volatility, line for moving average
        ax.scatter(country_data['date'], country_data['new_cases'], color='#aec7e8', alpha=0.5, s=10, label='Daily Cases')
        ax.plot(country_data['date'], country_data['new_cases_7d_avg'], color='#1f77b4', linewidth=2, label='7-Day Avg Cases')
        
        ax.set_ylabel("Daily Cases")
        ax.legend()
        plt.title(f"New Daily Cases in {country}")
        fig2.autofmt_xdate(rotation=45)
        st.pyplot(fig2)

    # Data Table
    with st.expander("View Raw Data Table"):
        show_cols = ['date', 'total_cases', 'new_cases', 'new_cases_7d_avg', 'total_deaths', 'new_deaths', 'people_fully_vaccinated']
        st.dataframe(country_data[show_cols].sort_values('date', ascending=False).reset_index(drop=True), use_container_width=True)


with tab2:
    st.header("Compare Countries (Cases per Million)")
    st.markdown("Comparing absolute numbers can be misleading. Using **Cases per Million** allows for a fair comparison between countries of different population sizes.")
    
    # Multi-select for comparison
    countries_to_compare = st.multiselect(
        "Select countries to compare:",
        options=data['location'].dropna().unique(),
        default=["United States", "India", "Brazil", "United Kingdom", "South Africa"]
    )
    
    if len(countries_to_compare) > 0:
        comp_data = data[data['location'].isin(countries_to_compare)]
        
        fig3, ax = plt.subplots(figsize=(12, 6))
        
        for comp_country in countries_to_compare:
            subset = comp_data[comp_data['location'] == comp_country]
            ax.plot(subset['date'], subset['cases_per_million'], label=comp_country, linewidth=2)
            
        ax.set_ylabel("Cases per Million People")
        ax.set_title("COVID-19 Cases per Million Over Time")
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        ax.grid(True, linestyle='--', alpha=0.7)
        fig3.autofmt_xdate(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig3)
    else:
        st.warning("Please select at least one country to view the comparison chart.")
