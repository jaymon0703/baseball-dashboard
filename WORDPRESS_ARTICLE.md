# Build Your Own Baseball Stats Dashboard: Code Your Way Into America's Pastime

*Combine your love of baseball with coding skills to create something amazing*

---

## Why Baseball and Coding Are a Perfect Match

If you love baseball and want to learn programming, I have great news: they're a perfect match! Both require attention to detail, pattern recognition, and problem-solving. Plus, baseball generates tons of interesting data that's perfect for learning to code.

Inspired by professional analytics platforms like [Baseball Savant](https://baseballsavant.mlb.com/), I'll show you how to build your own interactive baseball statistics dashboard. By the end, you'll have a working web application that displays player stats, team comparisons, and league leaders - all built with Python.

**No prior coding experience?** No problem! We'll walk through everything step-by-step.

---

## What You'll Build

Your dashboard will have:
- 🔍 **Player Search**: Find any MLB player and see their stats
- 🏟️ **Team Statistics**: Compare teams and see rankings  
- 🏆 **League Leaders**: See who's leading in home runs, RBIs, and more
- 📊 **Interactive Charts**: Beautiful visualizations that make data easy to understand

And the best part? You'll learn real programming skills while building something you can actually use!

---

## Getting Started: Setting Up Your Environment

### Step 1: Install Python

First, make sure you have Python installed. Open your terminal (Mac/Linux) or command prompt (Windows) and type:

```bash
python3 --version
```

If you see a version number (like `3.8.0` or higher), you're good! If not, download Python from [python.org](https://www.python.org/downloads/).

### Step 2: Create Your Project

Create a folder for your project:

```bash
mkdir baseball-dashboard
cd baseball-dashboard
```

### Step 3: Set Up a Virtual Environment

A virtual environment keeps your project's dependencies separate. Think of it like having a separate toolbox for each project:

```bash
python3 -m venv .venv
```

**On Mac/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

You should see `(.venv)` appear in your terminal - that means it's working!

### Step 4: Install Required Packages

Create a file called `requirements.txt`:

```txt
shiny>=0.9.0
shinywidgets>=0.1.0
pybaseball>=2.2.0
pandas>=2.0.0
plotly>=5.0.0
numpy>=1.24.0
```

Then install everything:

```bash
pip install -r requirements.txt
```

**What are these?**
- **shiny**: Makes building web apps super easy
- **shinywidgets**: Enables interactive Plotly charts
- **pybaseball**: Gets baseball data from the internet
- **pandas**: Helps us work with data tables
- **plotly**: Creates beautiful, interactive charts

---

## Understanding pybaseball: Your Gateway to Baseball Data

Before building the dashboard, let's understand what pybaseball can do. It's like having access to all of baseball's statistics at your fingertips!

### What is pybaseball?

pybaseball is a Python library that fetches baseball statistics from websites like FanGraphs and Baseball Reference. Instead of manually copying data, you get it with code!

### Your First Data Query

Let's test it out. Create a file called `test.py`:

```python
import pybaseball as pyb
import pandas as pd

# Get 2023 batting statistics
print("Loading 2023 stats...")
stats = pyb.batting_stats(2023, 2023)

# Show first 5 players
print("\nFirst 5 players:")
print(stats.head())

# Find the home run leader
hr_leader = stats.nlargest(1, 'HR')[['Name', 'Team', 'HR']]
print("\n🏆 2023 Home Run Leader:")
print(hr_leader)
```

Run it:
```bash
python test.py
```

Pretty cool, right? You just pulled real baseball data with code!

---

## Building Your Dashboard: Step by Step

Now let's build the actual dashboard. We'll start simple and add features as we go.

### Step 1: Create the Basic App Structure

Create `app.py`:

```python
from shiny import App, render, ui, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pybaseball as pyb

# Data loading function with caching
_data_cache = {}

def load_batting_stats(year):
    cache_key = f"batting_{year}"
    if cache_key in _data_cache:
        return _data_cache[cache_key]
    
    stats = pyb.batting_stats(year, year)
    _data_cache[cache_key] = stats
    return stats

# UI Definition
app_ui = ui.page_fluid(
    ui.tags.h1("⚾ Baseball Stats Dashboard"),
    
    ui.navset_tab(
        ui.nav_panel("Player Stats",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.h3("Search Parameters"),
                    ui.input_select("player_year", "Select Year", 
                                   choices={str(y): y for y in range(2020, 2026)}, 
                                   selected="2024"),
                    ui.input_text("player_name", "Enter Player Name", 
                                 placeholder="e.g., Aaron Judge"),
                    ui.input_action_button("search_player", "Search Player"),
                    width=300
                ),
                ui.output_ui("player_results")
            )
        ),
        
        ui.nav_panel("League Leaders",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.h3("Leaderboard Settings"),
                    ui.input_select("leaders_year", "Select Year",
                                   choices={str(y): y for y in range(2020, 2026)},
                                   selected="2024"),
                    ui.input_select("leaders_stat", "Select Statistic",
                                   choices={
                                       "HR": "Home Runs",
                                       "RBI": "Runs Batted In",
                                       "AVG": "Batting Average",
                                       "OPS": "OPS"
                                   },
                                   selected="HR"),
                    ui.input_action_button("load_leaders", "Load League Leaders"),
                    width=300
                ),
                ui.output_ui("leaders_results")
            )
        )
    )
)

# Server Logic
def server(input, output, session):
    player_state = reactive.Value({"found": False})
    
    @reactive.Effect
    @reactive.event(input.search_player)
    def _():
        if input.player_name():
            try:
                name_parts = input.player_name().strip().split()
                if len(name_parts) >= 2:
                    last_name = name_parts[-1]
                    first_name = ' '.join(name_parts[:-1])
                    
                    search_results = pyb.playerid_lookup(last_name, first_name)
                    if not search_results.empty:
                        player_state.set({
                            "found": True,
                            "fg_id": search_results.iloc[0]['key_fangraphs'],
                            "name": f"{search_results.iloc[0]['name_first']} {search_results.iloc[0]['name_last']}"
                        })
            except Exception as e:
                player_state.set({"found": False, "error": str(e)})
    
    @output
    @render.ui
    def player_results():
        if not player_state().get("found"):
            return ui.div(ui.p("Enter a player name and click 'Search Player'."))
        
        year = int(input.player_year())
        player_fg_id = player_state()["fg_id"]
        player_name = player_state()["name"]
        
        stats = load_batting_stats(year)
        player_stats = stats[stats['IDfg'] == player_fg_id]
        
        if player_stats.empty:
            return ui.div(ui.h3(f"Statistics for {player_name}"),
                         ui.p("No statistics found for this player in the selected year."))
        
        # Display key metrics
        hr = int(player_stats['HR'].iloc[0]) if 'HR' in player_stats.columns else 0
        rbi = int(player_stats['RBI'].iloc[0]) if 'RBI' in player_stats.columns else 0
        avg = player_stats['AVG'].iloc[0] if 'AVG' in player_stats.columns else 0
        ops = player_stats['OPS'].iloc[0] if 'OPS' in player_stats.columns else 0
        
        # Create visualization
        metrics = ['AVG', 'OBP', 'SLG', 'OPS']
        available_metrics = [m for m in metrics if m in player_stats.columns]
        
        fig = go.Figure()
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe']
        
        for i, metric in enumerate(available_metrics):
            value = player_stats[metric].iloc[0]
            fig.add_trace(go.Bar(
                name=metric,
                x=[metric],
                y=[value],
                text=[f"{value:.3f}"],
                textposition='outside',
                marker=dict(color=colors[i % len(colors)], opacity=0.9)
            ))
        
        fig.update_layout(
            title="Key Performance Metrics",
            xaxis_title="Metrics",
            yaxis_title="Value",
            barmode='group',
            height=400
        )
        
        return ui.div(
            ui.h3(f"Statistics for {player_name}"),
            ui.row(
                ui.column(3, ui.div(f"Home Runs: {hr}")),
                ui.column(3, ui.div(f"RBIs: {rbi}")),
                ui.column(3, ui.div(f"Batting Average: {avg:.3f}")),
                ui.column(3, ui.div(f"OPS: {ops:.3f}"))
            ),
            ui.h4("Performance Visualization"),
            output_widget("player_chart")
        )
    
    @output
    @render_widget
    def player_chart():
        # Chart rendering logic here
        return fig

app = App(app_ui, server)
```

### Step 2: Run Your Dashboard

Run your dashboard:
```bash
shiny run app.py
```

Your browser should open automatically! If not, go to `http://localhost:8000`

---

## Making It Look Professional

The dashboard we've built is functional, but you can make it look amazing with some CSS styling. Add this to your UI:

```python
ui.tags.head(
    ui.tags.link(rel="stylesheet", 
                href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"),
    ui.tags.style("""
        * {
            font-family: 'Inter', sans-serif;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
    """)
)
```

---

## Next Steps: Taking It to the Next Level

Once you have the basics working, here are some ideas to make your dashboard even more impressive:

### 1. Add More Statistics
- Pitching stats
- Fielding stats  
- Advanced metrics (WAR, wOBA)

### 2. Enhanced Visualizations
- Scatter plots comparing players
- Heatmaps for team performance
- Time series charts showing trends

### 3. Advanced Features
- Compare two players side-by-side
- Save favorite players
- Export data to CSV

### 4. Professional Touches
- Better color schemes
- Responsive design
- Loading indicators
- Error handling

---

## Inspiration: Baseball Savant

If you want to see what's possible, check out [Baseball Savant](https://baseballsavant.mlb.com/) - MLB's official Statcast platform. It features:

- **Advanced Statcast Metrics**: Exit velocity, launch angle, barrel rate
- **Interactive Visualizations**: 3D pitch tracking, spray charts
- **Real-time Data**: Live game updates
- **Professional Design**: Clean, modern interface

While your dashboard starts with basic stats, you can gradually add more advanced features as you learn!

---

## Deploying Your Dashboard: Share It With the World!

Now that you have a working dashboard, let's deploy it to the web so you can share it with friends, family, and the world!

### Why Deploy?

Deploying your app means putting it online where anyone can access it. No need for them to install Python or run code - they just visit a URL!

### Step 1: Create a shinyapps.io Account

1. Go to [shinyapps.io](https://www.shinyapps.io/)
2. Click "Sign Up" (it's free!)
3. Choose an account name (this will be part of your app URL)
4. Verify your email

The free tier gives you 5 apps and 25 hours of usage per month - perfect for learning!

### Step 2: Install rsconnect-python

You need the `rsconnect-python` package to deploy. Install it:

```bash
pip install rsconnect-python
```

### Step 3: Get Your Deployment Token

1. Log in to [shinyapps.io](https://www.shinyapps.io/)
2. Go to **Account** → **Tokens**
3. Click **Add Token**
4. Give it a name (e.g., "My Computer")
5. Copy the command that looks like:

```bash
rsconnect add --account YOUR_ACCOUNT_NAME --name YOUR_TOKEN_NAME --token YOUR_TOKEN --secret YOUR_SECRET
```

### Step 4: Configure rsconnect

Run the command you copied in your terminal. This links your computer to your shinyapps.io account.

### Step 5: Deploy Your App

Navigate to your project directory and run:

```bash
rsconnect deploy shiny . --name baseball-dashboard --title "Baseball Stats Dashboard"
```

Replace `baseball-dashboard` with your desired app name (lowercase, no spaces).

### Step 6: Access Your Live App!

Once deployment completes (takes 2-5 minutes), your app will be live at:

```
https://YOUR_ACCOUNT_NAME.shinyapps.io/baseball-dashboard/
```

**That's it!** Share this URL with anyone. They can use your dashboard without installing anything!

### Updating Your App

To update your deployed app with new features, just run the deploy command again:

```bash
rsconnect deploy shiny . --name baseball-dashboard --title "Baseball Stats Dashboard"
```

It will automatically update your live app!

### Troubleshooting

**"Module not found" errors?**
- Make sure all dependencies are in `requirements.txt`
- Check that package versions are compatible

**Deployment fails?**
- Ensure `app.py` has `app = App(app_ui, server)` at the bottom
- Check the shinyapps.io dashboard for error logs

**App runs locally but not online?**
- Some packages may not be available on shinyapps.io
- Test with a minimal version first

---

## What You've Learned

Congratulations! You've learned:
- ✅ How to set up a Python development environment
- ✅ How to use pybaseball to get baseball data
- ✅ How to build an interactive web dashboard with Shiny
- ✅ How to create visualizations with Plotly
- ✅ How to organize code into a working application
- ✅ **How to deploy your app to the web!**

Most importantly, you've built something real that you can use and share with the world!

---

## Resources

- **Full Code**: Check out the complete project on [GitHub](https://github.com/YOUR_USERNAME/baseball-dashboard)
- **Shiny for Python Docs**: [shiny.posit.co](https://shiny.posit.co/py/)
- **pybaseball Documentation**: [GitHub](https://github.com/jldbc/pybaseball)
- **Baseball Savant**: [baseballsavant.mlb.com](https://baseballsavant.mlb.com/)

---

## Final Thoughts

Building a baseball dashboard is more than just a coding project - it's a way to combine your interests, learn valuable skills, and create something meaningful. The skills you've learned here apply to so many other projects:

- Building dashboards for other sports
- Analyzing any kind of data
- Creating web applications
- Working with APIs and data sources

Keep coding, keep learning, and most importantly - keep having fun! ⚾💻

---

*Want to share what you built? Post it on GitHub, write about it, or help others build their own dashboards. The coding community is friendly and always happy to help!*


