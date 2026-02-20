# 🦠 COVID-19 Analytical Dashboard

An interactive, fast, and analytical COVID-19 Data Dashboard built with Python, Pandas, Matplotlib, and Streamlit. This project dynamically fetches live data from the official Our World in Data repository to visualize pandemic trends, compare case rates globally, and track key metrics.

## ✨ Features
- **Live Data Fetching**: Bypasses GitHub file size limits by loading the 100MB+ dataset directly from the official OWID repository.
- **Advanced Analytics**: Visualizes 7-day rolling averages to smooth out reporting noise.
- **Fair Global Benchmarking**: Instead of absolute numbers, compares countries using "Cases per Million" to ensure fairness across different population sizes.
- **Split View Interface**: 
  - *Deep Dive tab* for tracking specific country trajectories, mortality rates, and vaccination progress across custom timeframes.
  - *Global Comparison tab* for simultaneously comparing the normalized growth curves of multiple countries.
- **Optimized Performance**: Utilizes Streamlit memory caching (`@st.cache_data`) for instant data retrieval.

---

## 🚀 Getting Started in VS Code

### Prerequisites
Make sure you have Python installed on your system. You can check this by running `python --version` in your terminal.

### 1. Clone the project and open in VS Code
Open your VS Code terminal (`Ctrl` + `` ` `` or `Cmd` + `` ` ``) and clone your repository:
```bash
git clone https://github.com/shrutibedve/covid19-dashboard.git
cd covid-19-dashboard
```

### 2. Set up a Virtual Environment (Recommended but optional)
It's best practice to create an isolated environment for your project dependencies. In the VS Code terminal, run:

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

*(Note: VS Code might prompt you at the bottom right asking if you want to use this new virtual environment for the workspace. Click "Yes").*

### 3. Install Dependencies
Install the required Python packages (Streamlit, Pandas, Matplotlib):
```bash
pip install -r requirements.txt
```

### 4. Run the Dashboard locally
Launch the Streamlit server from your VS Code terminal:
```bash
streamlit run covid_dashboard_streamlit.py
```

Streamlit will automatically open a new tab in your default browser at `http://localhost:8501/` with your live dashboard!

---

## 🛠️ Built With
- **[Python](https://www.python.org/)** - Core programming logic
- **[Pandas](https://pandas.pydata.org/)** - Data ingestion, cleaning, and manipulation
- **[Streamlit](https://streamlit.io/)** - Frontend web framework and UI components
- **[Matplotlib](https://matplotlib.org/)** - Creating the custom dual-axis charts

## 📄 Data Source
- Dataset provided by **[Our World in Data](https://github.com/owid/covid-19-data/tree/master/public/data)**.

http://localhost:8501/

