# ⚾ Baseball Stats Dashboard

A comprehensive, interactive dashboard for visualizing baseball statistics using pybaseball and Streamlit.

![Baseball Dashboard](https://img.shields.io/badge/Baseball-Stats%20Dashboard-blue?style=for-the-badge&logo=baseball)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge&logo=streamlit)

## 🚀 Features

### 🔍 Player Statistics
- **Player Search**: Find any MLB player by name
- **Comprehensive Stats**: View detailed batting statistics including HR, RBI, AVG, OPS
- **Interactive Visualizations**: Performance charts and metrics
- **Historical Data**: View stats from 2020-2024

### 🏟️ Team Statistics
- **Team Comparisons**: Compare multiple teams side-by-side
- **League Rankings**: Top 10 teams in various categories
- **Performance Metrics**: Runs, home runs, batting average analysis
- **Interactive Charts**: Multi-panel team comparison visualizations

### 🏆 League Leaders
- **Multiple Categories**: HR, RBI, Runs, Hits, Batting Average, OPS, Stolen Bases
- **Top 20 Rankings**: Comprehensive leaderboards
- **Visual Charts**: Interactive bar charts for top performers
- **Detailed Stats**: Complete statistical breakdowns

### 📊 Game Logs
- **Game-by-Game Analysis**: Individual player performance tracking
- **Cumulative Statistics**: Performance trends over time
- **Time Series Charts**: Visual representation of season progression
- **Detailed Logs**: Complete game-by-game statistics

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start (Recommended)

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd baseball-dashboard
   ```

2. **Run the startup script**
   ```bash
   ./run_dashboard.sh
   ```
   
   This script will:
   - Create a virtual environment (if it doesn't exist)
   - Install all dependencies
   - Start the dashboard

3. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL manually

### Manual Setup

1. **Create and activate virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📦 Dependencies

- **streamlit** (1.28.1): Web application framework
- **pybaseball** (2.2.7): Baseball data collection and analysis
- **pandas** (2.1.3): Data manipulation and analysis
- **plotly** (5.17.0): Interactive visualizations
- **numpy** (1.24.3): Numerical computing
- **requests** (2.31.0): HTTP library for data fetching
- **beautifulsoup4** (4.12.2): Web scraping
- **lxml** (4.9.3): XML and HTML processing

## 🎯 Usage Guide

### Getting Started
1. **Launch the app** using `./run_dashboard.sh` or `streamlit run app.py`
2. **Navigate** using the sidebar menu
3. **Search for players** using their full name (e.g., "Aaron Judge")
4. **Select years** to view historical data (2020-2024)
5. **Explore** interactive charts and visualizations

### Player Search Tips
- Use full names: "Aaron Judge", "Mike Trout", "Mookie Betts"
- First name and last name are required
- The search will find the most recent active player with that name

### Data Caching
- Data is cached for 1 hour to improve performance
- If you need fresh data, restart the application
- Some queries may take a few seconds to load initially

## 📊 Data Sources

This dashboard uses data from:
- **FanGraphs**: Comprehensive baseball statistics
- **Baseball Reference**: Historical and current player data
- **MLB Official Data**: Through pybaseball's data collection

## 🎨 Features Overview

### Interactive Elements
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live data fetching and caching
- **Custom Styling**: Modern, baseball-themed UI
- **Multi-page Navigation**: Easy switching between features

### Visualizations
- **Bar Charts**: League leaders and team comparisons
- **Line Charts**: Performance trends over time
- **Multi-panel Charts**: Comprehensive team analysis
- **Interactive Tables**: Sortable and filterable data

### Performance
- **Data Caching**: 1-hour cache for improved speed
- **Lazy Loading**: Data loaded only when needed
- **Error Handling**: Graceful handling of data issues
- **Loading Indicators**: User feedback during data fetching

## 🔧 Customization

### Adding New Statistics
1. Modify the `stat_options` dictionary in the League Leaders section
2. Update the display columns in relevant functions
3. Add new visualization types as needed

### Styling Changes
- Modify the CSS in the `st.markdown()` section at the top
- Update colors, fonts, and layout as desired
- Customize the page configuration in `st.set_page_config()`

### Data Sources
- pybaseball supports many additional data sources
- Check the [pybaseball documentation](https://github.com/jldbc/pybaseball) for more options
- Add new data collection functions as needed

## 🐛 Troubleshooting

### Common Issues

**"Player not found" error**
- Ensure you're using the player's full name
- Try different variations (nickname vs. full name)
- Check if the player was active in the selected year

**Slow loading times**
- Data fetching can take 10-30 seconds for large queries
- The app caches data for 1 hour to improve subsequent loads
- Consider using more recent years for faster results

**Missing statistics**
- Some players may not have complete statistics for certain years
- Try different years or check if the player was active
- Minor league or international players may have limited MLB data

**Installation issues**
- Ensure you have Python 3.8 or higher
- Try upgrading pip: `pip install --upgrade pip`
- Install dependencies one by one if batch installation fails

**Virtual Environment Issues**
- Make sure you're in the project directory
- Activate the virtual environment: `source .venv/bin/activate`
- Use the startup script: `./run_dashboard.sh`

## 🚀 Development

### Project Structure
```
baseball-dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── run_dashboard.sh      # Startup script
├── README.md             # This file
└── .venv/                # Virtual environment (created automatically)
```

### Running in Development Mode
```bash
# Activate virtual environment
source .venv/bin/activate

# Run with auto-reload
streamlit run app.py --server.runOnSave true
```

## 🤝 Contributing

Contributions are welcome! Here are some ways to help:

1. **Bug Reports**: Report issues with detailed descriptions
2. **Feature Requests**: Suggest new functionality
3. **Code Improvements**: Submit pull requests for enhancements
4. **Documentation**: Help improve this README or add comments

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **pybaseball**: For providing comprehensive baseball data access
- **Streamlit**: For the excellent web app framework
- **Plotly**: For beautiful interactive visualizations
- **MLB and FanGraphs**: For the underlying baseball data

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the pybaseball documentation
3. Open an issue in the repository
4. Check Streamlit's documentation for UI-related questions

---

**Happy Baseball Analytics! ⚾📊**
