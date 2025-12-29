"""
Baseball Dashboard - Complete Code Examples
For embedding in WordPress article via GitHub Gist
"""

# ============================================================================
# EXAMPLE 1: Testing pybaseball
# ============================================================================

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


# ============================================================================
# EXAMPLE 2: Basic Shiny App Structure
# ============================================================================

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
# NOTE: The styling (ui.tags.head) goes INSIDE ui.page_fluid, as the FIRST element
app_ui = ui.page_fluid(
    # ===== ADD STYLING HERE (inside page_fluid, at the top) =====
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
    ),
    # ===== END OF STYLING =====
    
    # Now add your UI content
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


# ============================================================================
# NOTE: Professional Styling is Already Included!
# ============================================================================

# The code in Example 2 above already includes professional styling.
# Look for the ui.tags.head() section at the top of app_ui - that's where
# the styling lives:
#
# - Custom fonts (Inter from Google Fonts)
# - Gradient backgrounds
# - Styled metric cards
# - Professional color scheme
#
# If you want to customize the styling, modify the CSS inside ui.tags.style()
# You can change colors, fonts, spacing, and more!
#
# To remove styling and start with a basic version, simply remove the
# ui.tags.head() section from app_ui.

