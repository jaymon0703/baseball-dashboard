from shiny import App, render, ui, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pybaseball as pyb
import numpy as np
from datetime import datetime

# Data loading functions with caching
_data_cache = {}

def load_player_stats(player_fg_id, year):
    """Load player statistics for a given year using FanGraphs ID"""
    cache_key = f"player_{player_fg_id}_{year}"
    if cache_key in _data_cache:
        return _data_cache[cache_key]
    
    try:
        stats = pyb.batting_stats(year, year)
        player_stats = stats[stats['IDfg'] == player_fg_id]
        _data_cache[cache_key] = player_stats
        return player_stats
    except Exception as e:
        print(f"Error loading player stats: {e}")
        return pd.DataFrame()

def load_team_stats(year):
    """Load team statistics for a given year"""
    cache_key = f"team_{year}"
    if cache_key in _data_cache:
        return _data_cache[cache_key]
    
    try:
        team_stats = pyb.team_batting(year)
        _data_cache[cache_key] = team_stats
        return team_stats
    except Exception as e:
        print(f"Error loading team stats: {e}")
        return pd.DataFrame()

def load_league_leaders(year, stat='HR'):
    """Load league leaders for a given stat and year"""
    cache_key = f"leaders_{year}_{stat}"
    if cache_key in _data_cache:
        return _data_cache[cache_key]
    
    try:
        leaders = pyb.batting_stats(year, year)
        leaders = leaders.sort_values(stat, ascending=False).head(20)
        _data_cache[cache_key] = leaders
        return leaders
    except Exception as e:
        print(f"Error loading league leaders: {e}")
        return pd.DataFrame()

def load_game_logs(player_mlb_id, year):
    """Load game logs for a player using MLB ID"""
    cache_key = f"logs_{player_mlb_id}_{year}"
    if cache_key in _data_cache:
        return _data_cache[cache_key]
    
    try:
        logs = pyb.season_game_logs(player_mlb_id, year)
        _data_cache[cache_key] = logs
        return logs
    except Exception as e:
        print(f"Error loading game logs: {e}")
        return pd.DataFrame()

# UI Definition
app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"),
        ui.tags.style("""
            * {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            }
            body {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                min-height: 100vh;
            }
            .main-header {
                font-size: 3.5rem;
                font-weight: 700;
                color: #1a365d;
                text-align: center;
                margin-bottom: 2.5rem;
                margin-top: 1rem;
                text-shadow: 2px 2px 8px rgba(0,0,0,0.1);
                letter-spacing: -0.02em;
            }
            .metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s, box-shadow 0.2s;
                border: none;
                font-weight: 600;
            }
            .metric-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            }
            .metric-card h3 {
                font-size: 0.875rem;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.5rem;
                opacity: 0.9;
            }
            .metric-card .value {
                font-size: 2rem;
                font-weight: 700;
                margin: 0;
            }
            .sidebar {
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                padding: 1.5rem;
            }
            .main-content {
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                padding: 2rem;
                margin-left: 1rem;
            }
            h2, h3, h4 {
                color: #1a365d;
                font-weight: 600;
                margin-top: 1.5rem;
                margin-bottom: 1rem;
            }
            h2 {
                font-size: 2rem;
            }
            h3 {
                font-size: 1.5rem;
            }
            h4 {
                font-size: 1.25rem;
            }
            .nav-tabs {
                border-bottom: 2px solid #e2e8f0;
                margin-bottom: 2rem;
            }
            .nav-tabs .nav-link {
                color: #64748b;
                font-weight: 500;
                border: none;
                border-bottom: 3px solid transparent;
                padding: 0.75rem 1.5rem;
                transition: all 0.2s;
            }
            .nav-tabs .nav-link:hover {
                color: #1a365d;
                border-bottom-color: #cbd5e1;
            }
            .nav-tabs .nav-link.active {
                color: #1a365d;
                border-bottom-color: #667eea;
                background: transparent;
            }
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                border-radius: 8px;
                padding: 0.75rem 1.5rem;
                font-weight: 600;
                transition: all 0.2s;
                box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
            }
            .btn-primary:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
            }
            .form-control, .form-select {
                border-radius: 8px;
                border: 2px solid #e2e8f0;
                padding: 0.75rem;
                transition: all 0.2s;
            }
            .form-control:focus, .form-select:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            table {
                border-radius: 8px;
                overflow: hidden;
            }
            .table {
                background: white;
            }
            .table thead {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .table thead th {
                border: none;
                font-weight: 600;
                text-transform: uppercase;
                font-size: 0.875rem;
                letter-spacing: 0.05em;
            }
            .table tbody tr {
                transition: background 0.2s;
            }
            .table tbody tr:hover {
                background: #f8fafc;
            }
        """)
    ),
    ui.tags.h1("⚾ Baseball Stats Dashboard", class_="main-header"),
    
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
                    ui.input_action_button("search_player", "Search Player", class_="btn-primary"),
                    width=300
                ),
                ui.output_ui("player_results")
            )
        ),
        
        ui.nav_panel("Team Stats",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.h3("Team Analysis"),
                    ui.input_select("team_year", "Select Year",
                                   choices={str(y): y for y in range(2020, 2026)},
                                   selected="2024"),
                    ui.input_action_button("load_teams", "Load Team Stats", class_="btn-primary"),
                    width=300
                ),
                ui.output_ui("team_results")
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
                                       "R": "Runs",
                                       "H": "Hits",
                                       "AVG": "Batting Average",
                                       "OPS": "OPS",
                                       "SB": "Stolen Bases"
                                   },
                                   selected="HR"),
                    ui.input_action_button("load_leaders", "Load League Leaders", class_="btn-primary"),
                    width=300
                ),
                ui.output_ui("leaders_results")
            )
        ),
        
        ui.nav_panel("About",
            ui.h2("ℹ️ About This Dashboard"),
            ui.markdown("""
            ## Baseball Stats Dashboard
            
            This interactive dashboard provides comprehensive baseball statistics and analysis using the **pybaseball** library.
            
            ### Features:
            
            #### 🔍 Player Stats
            - Search for any MLB player by name
            - View detailed batting statistics
            - Interactive performance visualizations
            - Key metrics display (HR, RBI, AVG, OPS)
            
            #### 🏟️ Team Stats
            - Team performance comparisons
            - League-wide team rankings
            - Interactive team selection and comparison charts
            
            #### 🏆 League Leaders
            - Top performers in various categories
            - Interactive leaderboards with visualizations
            
            ### Technology Stack:
            - **Shiny for Python**: Web application framework
            - **Plotly**: Interactive visualizations
            - **Pandas**: Data manipulation and analysis
            - **pybaseball**: Baseball data collection
            """)
        )
    )
)

# Server Logic
def server(input, output, session):
    # Player search state
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
                            "mlb_id": search_results.iloc[0]['key_mlbam'],
                            "fg_id": search_results.iloc[0]['key_fangraphs'],
                            "name": f"{search_results.iloc[0]['name_first']} {search_results.iloc[0]['name_last']}"
                        })
                    else:
                        player_state.set({"found": False, "error": "Player not found"})
            except Exception as e:
                player_state.set({"found": False, "error": str(e)})
    
    @output
    @render.ui
    def player_results():
        if not player_state().get("found"):
            if input.player_name():
                return ui.div(
                    ui.p("Enter a player name and click 'Search Player' to get started.", class_="text-muted")
                )
            return ui.div()
        
        year = int(input.player_year())
        player_fg_id = player_state()["fg_id"]
        player_name = player_state()["name"]
        
        player_stats = load_player_stats(player_fg_id, year)
        
        if player_stats.empty:
            return ui.div(
                ui.h3(f"Statistics for {player_name}"),
                ui.p("No statistics found for this player in the selected year.")
            )
        
        # Key metrics
        hr = int(player_stats['HR'].iloc[0]) if 'HR' in player_stats.columns else 0
        rbi = int(player_stats['RBI'].iloc[0]) if 'RBI' in player_stats.columns else 0
        avg = player_stats['AVG'].iloc[0] if 'AVG' in player_stats.columns else 0
        ops = player_stats['OPS'].iloc[0] if 'OPS' in player_stats.columns else 0
        
        # Create chart
        metrics = ['AVG', 'OBP', 'SLG', 'OPS']
        available_metrics = [m for m in metrics if m in player_stats.columns]
        
        fig = go.Figure()
        for metric in available_metrics:
            fig.add_trace(go.Bar(
                name=metric,
                x=[metric],
                y=[player_stats[metric].iloc[0]],
                text=[f"{player_stats[metric].iloc[0]:.3f}"],
                textposition='auto'
            ))
        
        fig.update_layout(
            title="Key Performance Metrics",
            xaxis_title="Metrics",
            yaxis_title="Value",
            barmode='group'
        )
        
        display_cols = ['Name', 'Team', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'BB', 'SO', 'AVG', 'OBP', 'SLG', 'OPS']
        available_cols = [col for col in display_cols if col in player_stats.columns]
        
        return ui.div(
            ui.h3(f"Statistics for {player_name}"),
            ui.row(
                ui.column(3, ui.div(
                    ui.tags.h3("Home Runs", style="font-size: 0.875rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; opacity: 0.9;"),
                    ui.tags.p(f"{hr}", class_="value", style="font-size: 2rem; font-weight: 700; margin: 0;"),
                    class_="metric-card"
                )),
                ui.column(3, ui.div(
                    ui.tags.h3("RBIs", style="font-size: 0.875rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; opacity: 0.9;"),
                    ui.tags.p(f"{rbi}", class_="value", style="font-size: 2rem; font-weight: 700; margin: 0;"),
                    class_="metric-card"
                )),
                ui.column(3, ui.div(
                    ui.tags.h3("Batting Average", style="font-size: 0.875rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; opacity: 0.9;"),
                    ui.tags.p(f"{avg:.3f}", class_="value", style="font-size: 2rem; font-weight: 700; margin: 0;"),
                    class_="metric-card"
                )),
                ui.column(3, ui.div(
                    ui.tags.h3("OPS", style="font-size: 0.875rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; opacity: 0.9;"),
                    ui.tags.p(f"{ops:.3f}", class_="value", style="font-size: 2rem; font-weight: 700; margin: 0;"),
                    class_="metric-card"
                ))
            ),
            ui.h4("Detailed Statistics"),
            ui.output_data_frame("player_table"),
            ui.h4("Performance Visualization"),
            output_widget("player_chart")
        )
    
    @output
    @render.data_frame
    def player_table():
        if not player_state().get("found"):
            return pd.DataFrame()
        
        year = int(input.player_year())
        player_fg_id = player_state()["fg_id"]
        player_stats = load_player_stats(player_fg_id, year)
        
        if player_stats.empty:
            return pd.DataFrame()
        
        display_cols = ['Name', 'Team', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'BB', 'SO', 'AVG', 'OBP', 'SLG', 'OPS']
        available_cols = [col for col in display_cols if col in player_stats.columns]
        return player_stats[available_cols]
    
    @output
    @render_widget
    def player_chart():
        if not player_state().get("found"):
            return None
        
        year = int(input.player_year())
        player_fg_id = player_state()["fg_id"]
        player_stats = load_player_stats(player_fg_id, year)
        
        if player_stats.empty:
            return None
        
        metrics = ['AVG', 'OBP', 'SLG', 'OPS']
        available_metrics = [m for m in metrics if m in player_stats.columns]
        
        # Create a more professional bar chart
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe']
        fig = go.Figure()
        
        for i, metric in enumerate(available_metrics):
            value = player_stats[metric].iloc[0]
            fig.add_trace(go.Bar(
                name=metric,
                x=[metric],
                y=[value],
                text=[f"{value:.3f}"],
                textposition='outside',
                textfont=dict(size=14, color='#1a365d', family='Inter'),
                marker=dict(
                    color=colors[i % len(colors)],
                    line=dict(color='white', width=2),
                    opacity=0.9
                ),
                hovertemplate=f'<b>{metric}</b><br>Value: {value:.3f}<extra></extra>',
            ))
        
        fig.update_layout(
            title=dict(
                text="Key Performance Metrics",
                font=dict(size=24, family='Inter', color='#1a365d', weight='bold'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title=dict(text="Metrics", font=dict(size=16, family='Inter', color='#64748b')),
                tickfont=dict(size=14, family='Inter', color='#1a365d'),
                gridcolor='#e2e8f0',
                gridwidth=1
            ),
            yaxis=dict(
                title=dict(text="Value", font=dict(size=16, family='Inter', color='#64748b')),
                tickfont=dict(size=14, family='Inter', color='#1a365d'),
                gridcolor='#e2e8f0',
                gridwidth=1,
                zeroline=False
            ),
            barmode='group',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=12),
            height=500,
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=12, family='Inter', color='#64748b')
            )
        )
        
        return fig
    
    # Team stats
    team_data = reactive.Value(pd.DataFrame())
    
    @reactive.Effect
    @reactive.event(input.load_teams)
    def _():
        year = int(input.team_year())
        team_data.set(load_team_stats(year))
    
    @output
    @render.ui
    def team_results():
        if team_data().empty:
            return ui.div(
                ui.p("Click 'Load Team Stats' to view team statistics.", class_="text-muted")
            )
        
        year = int(input.team_year())
        team_stats = team_data()
        
        top_runs = team_stats.nlargest(10, 'R')[['Team', 'R', 'G']]
        top_hr = team_stats.nlargest(10, 'HR')[['Team', 'HR', 'G']]
        top_avg = team_stats.nlargest(10, 'AVG')[['Team', 'AVG', 'G']]
        
        avg_runs = team_stats['R'].mean()
        avg_hr = team_stats['HR'].mean()
        avg_avg = team_stats['AVG'].mean()
        
        return ui.div(
            ui.h3(f"Team Statistics for {year}"),
            ui.row(
                ui.column(3, ui.div(f"Total Teams: {len(team_stats)}", class_="metric-card")),
                ui.column(3, ui.div(f"Avg Runs/Team: {avg_runs:.1f}", class_="metric-card")),
                ui.column(3, ui.div(f"Avg HR/Team: {avg_hr:.1f}", class_="metric-card")),
                ui.column(3, ui.div(f"League Avg BA: {avg_avg:.3f}", class_="metric-card"))
            ),
            ui.h4("Top 10 Teams by Runs"),
            ui.output_data_frame("top_runs_table"),
            ui.h4("Top 10 Teams by Home Runs"),
            ui.output_data_frame("top_hr_table"),
            ui.h4("Top 10 Teams by Batting Average"),
            ui.output_data_frame("top_avg_table")
        )
    
    @output
    @render.data_frame
    def top_runs_table():
        if team_data().empty:
            return pd.DataFrame()
        return team_data().nlargest(10, 'R')[['Team', 'R', 'G']]
    
    @output
    @render.data_frame
    def top_hr_table():
        if team_data().empty:
            return pd.DataFrame()
        return team_data().nlargest(10, 'HR')[['Team', 'HR', 'G']]
    
    @output
    @render.data_frame
    def top_avg_table():
        if team_data().empty:
            return pd.DataFrame()
        return team_data().nlargest(10, 'AVG')[['Team', 'AVG', 'G']]
    
    # League leaders
    leaders_data = reactive.Value(pd.DataFrame())
    selected_stat = reactive.Value("HR")
    
    @reactive.Effect
    @reactive.event(input.load_leaders)
    def _():
        year = int(input.leaders_year())
        stat = input.leaders_stat()
        selected_stat.set(stat)
        leaders_data.set(load_league_leaders(year, stat))
    
    @output
    @render.ui
    def leaders_results():
        if leaders_data().empty:
            return ui.div(
                ui.p("Select a statistic and click 'Load League Leaders' to view rankings.", class_="text-muted")
            )
        
        stat = selected_stat()
        stat_options = {
            'HR': 'Home Runs',
            'RBI': 'Runs Batted In',
            'R': 'Runs',
            'H': 'Hits',
            'AVG': 'Batting Average',
            'OPS': 'OPS',
            'SB': 'Stolen Bases'
        }
        stat_name = stat_options.get(stat, stat)
        year = int(input.leaders_year())
        
        leaders = leaders_data()
        top_15 = leaders.head(15)
        
        fig = px.bar(
            top_15,
            x='Name',
            y=stat,
            title=f"Top 15 {stat_name} Leaders",
            color=stat,
            color_continuous_scale='viridis'
        )
        fig.update_layout(xaxis_tickangle=-45)
        
        return ui.div(
            ui.h3(f"Top 20 {stat_name} Leaders - {year}"),
            output_widget("leaders_chart"),
            ui.h4("Complete Leaderboard"),
            ui.output_data_frame("leaders_table")
        )
    
    @output
    @render_widget
    def leaders_chart():
        if leaders_data().empty:
            return None
        
        stat = selected_stat()
        stat_options = {
            'HR': 'Home Runs',
            'RBI': 'Runs Batted In',
            'R': 'Runs',
            'H': 'Hits',
            'AVG': 'Batting Average',
            'OPS': 'OPS',
            'SB': 'Stolen Bases'
        }
        stat_name = stat_options.get(stat, stat)
        
        top_15 = leaders_data().head(15)
        
        fig = px.bar(
            top_15,
            x='Name',
            y=stat,
            title=f"Top 15 {stat_name} Leaders",
            color=stat,
            color_continuous_scale='Viridis',
            labels={stat: stat_name}
        )
        fig.update_layout(
            title=dict(
                text=f"Top 15 {stat_name} Leaders",
                font=dict(size=24, family='Inter', color='#1a365d', weight='bold'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title=dict(text="Player", font=dict(size=16, family='Inter', color='#64748b')),
                tickfont=dict(size=12, family='Inter', color='#1a365d'),
                tickangle=-45,
                gridcolor='#e2e8f0',
                gridwidth=1
            ),
            yaxis=dict(
                title=dict(text=stat_name, font=dict(size=16, family='Inter', color='#64748b')),
                tickfont=dict(size=14, family='Inter', color='#1a365d'),
                gridcolor='#e2e8f0',
                gridwidth=1
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=12),
            height=500,
            margin=dict(l=50, r=50, t=80, b=150),
            coloraxis_colorbar=dict(
                title=dict(text=stat_name, font=dict(size=12, family='Inter', color='#64748b')),
                tickfont=dict(size=11, family='Inter', color='#64748b')
            )
        )
        return fig
    
    @output
    @render.data_frame
    def leaders_table():
        if leaders_data().empty:
            return pd.DataFrame()
        
        stat = selected_stat()
        display_cols = ['Name', 'Team', stat, 'G', 'AB']
        available_cols = [col for col in display_cols if col in leaders_data().columns]
        return leaders_data()[available_cols]

app = App(app_ui, server)
