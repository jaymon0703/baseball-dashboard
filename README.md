# ⚾ Baseball Stats Dashboard

A comprehensive, interactive dashboard for visualizing baseball statistics using pybaseball and Streamlit.

![Baseball Dashboard](https://img.shields.io/badge/Baseball-Stats%20Dashboard-blue?style=for-the-badge&logo=baseball)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Shiny](https://img.shields.io/badge/Shiny%20for%20Python-1.5+-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

## 🚀 Features

### 🔍 Player Statistics
- **Player Search**: Find any MLB player by name
- **Comprehensive Stats**: View detailed batting statistics including HR, RBI, AVG, OPS
- **Interactive Visualizations**: Performance charts and metrics
- **Historical Data**: View stats from 2020-2025 (including current season!)

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

1. **Clone this repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/baseball-dashboard.git
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
   shiny run app.py
   ```

## 📦 Dependencies

- **shiny** (>=0.9.0): Web application framework
- **shinywidgets** (>=0.1.0): Interactive Plotly chart support
- **pybaseball** (>=2.2.0): Baseball data collection and analysis
- **pandas** (>=2.0.0): Data manipulation and analysis
- **plotly** (>=5.0.0): Interactive visualizations
- **numpy** (>=1.24.0): Numerical computing
- **requests** (>=2.30.0): HTTP library for data fetching
- **beautifulsoup4** (>=4.12.0): Web scraping
- **lxml** (>=4.9.0): XML and HTML processing

## 🎯 Usage Guide

### Getting Started
1. **Launch the app** using `./run_dashboard.sh` or `shiny run app.py`
2. **Navigate** using the sidebar menu
3. **Search for players** using their full name (e.g., "Aaron Judge")
4. **Select years** to view historical data (2020-2025)
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
├── .gitignore            # Git ignore file
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

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **pybaseball**: For providing comprehensive baseball data access
- **Shiny for Python**: For the excellent web app framework
- **Plotly**: For beautiful interactive visualizations
- **MLB and FanGraphs**: For the underlying baseball data

## 🚀 Deployment

Want to share your dashboard with the world? Deploy it to [shinyapps.io](https://www.shinyapps.io/)!

### Quick Deployment Steps:

1. **Install rsconnect-python**:
   ```bash
   pip install rsconnect-python
   ```

2. **Create a shinyapps.io account** (free tier available)

3. **Get your deployment token** from shinyapps.io account settings

4. **Configure rsconnect**:
   ```bash
   rsconnect add --account YOUR_ACCOUNT --name NAME --token TOKEN --secret SECRET
   ```

5. **Deploy your app**:
   ```bash
   rsconnect deploy shiny . --name baseball-dashboard --title "Baseball Stats Dashboard"
   ```

6. **Share your app**: `https://YOUR_ACCOUNT.shinyapps.io/baseball-dashboard/`

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

---

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the [pybaseball documentation](https://github.com/jldbc/pybaseball)
3. Open an issue in the repository
4. Check [Shiny for Python documentation](https://shiny.posit.co/py/) for UI-related questions

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/baseball-dashboard&type=Date)](https://star-history.com/#YOUR_USERNAME/baseball-dashboard&Date)

---

**Happy Baseball Analytics! ⚾📊**

*Built with ❤️ using Shiny for Python and pybaseball*
