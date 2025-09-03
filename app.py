import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pybaseball as pyb
import numpy as np
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="Baseball Stats Dashboard",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">⚾ Baseball Stats Dashboard</h1>', unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Player Stats", "Team Stats", "League Leaders", "Game Logs", "About"]
)

# Cache data loading functions
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_player_stats(player_fg_id, year):
    """Load player statistics for a given year using FanGraphs ID"""
    try:
        # Use batting_stats for season-level data
        stats = pyb.batting_stats(year, year)
        # Filter by FanGraphs ID
        player_stats = stats[stats['IDfg'] == player_fg_id]
        return player_stats
    except Exception as e:
        st.error(f"Error loading player stats: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_team_stats(year):
    """Load team statistics for a given year"""
    try:
        # Use team_batting for team stats
        team_stats = pyb.team_batting(year)
        return team_stats
    except Exception as e:
        st.error(f"Error loading team stats: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_league_leaders(year, stat='HR'):
    """Load league leaders for a given stat and year"""
    try:
        # Use batting_stats for league-wide stats
        leaders = pyb.batting_stats(year, year)
        # Sort by the selected stat and get top 20
        leaders = leaders.sort_values(stat, ascending=False).head(20)
        return leaders
    except Exception as e:
        st.error(f"Error loading league leaders: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_game_logs(player_mlb_id, year):
    """Load game logs for a player using MLB ID"""
    try:
        # Use season_game_logs for individual player game logs
        logs = pyb.season_game_logs(player_mlb_id, year)
        return logs
    except Exception as e:
        st.error(f"Error loading game logs: {e}")
        return pd.DataFrame()

# Main content based on selected page
if page == "Player Stats":
    st.header("🔍 Player Statistics")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Search Parameters")
        year = st.selectbox("Select Year", range(2020, 2026), index=5)  # Updated to include 2025
        
        # Player search
        player_name = st.text_input("Enter Player Name (e.g., 'Aaron Judge')")
        
        if st.button("Search Player"):
            if player_name:
                with st.spinner("Searching for player..."):
                    try:
                        # Split name and search for player ID
                        name_parts = player_name.strip().split()
                        if len(name_parts) >= 2:
                            last_name = name_parts[-1]
                            first_name = ' '.join(name_parts[:-1])
                            
                            # Search for player ID
                            search_results = pyb.playerid_lookup(last_name, first_name)
                            if not search_results.empty:
                                player_mlb_id = search_results.iloc[0]['key_mlbam']
                                player_fg_id = search_results.iloc[0]['key_fangraphs']
                                player_name_found = f"{search_results.iloc[0]['name_first']} {search_results.iloc[0]['name_last']}"
                                st.session_state.player_mlb_id = player_mlb_id
                                st.session_state.player_fg_id = player_fg_id
                                st.session_state.player_name = player_name_found
                                st.success(f"Found player: {player_name_found}")
                            else:
                                st.error("Player not found. Please try a different name.")
                        else:
                            st.error("Please enter both first and last name.")
                    except Exception as e:
                        st.error(f"Error searching for player: {e}")
    
    with col2:
        if hasattr(st.session_state, 'player_fg_id'):
            st.subheader(f"Statistics for {st.session_state.player_name}")
            
            # Load player stats using FanGraphs ID
            player_stats = load_player_stats(st.session_state.player_fg_id, year)
            
            if not player_stats.empty:
                # Key metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    hr = player_stats['HR'].iloc[0] if 'HR' in player_stats.columns else 0
                    st.metric("Home Runs", int(hr))
                with col2:
                    rbi = player_stats['RBI'].iloc[0] if 'RBI' in player_stats.columns else 0
                    st.metric("RBIs", int(rbi))
                with col3:
                    avg = player_stats['AVG'].iloc[0] if 'AVG' in player_stats.columns else 0
                    st.metric("Batting Average", f"{avg:.3f}")
                with col4:
                    ops = player_stats['OPS'].iloc[0] if 'OPS' in player_stats.columns else 0
                    st.metric("OPS", f"{ops:.3f}")
                
                # Add games played metric for 2025
                if year == 2025:
                    col5, col6 = st.columns(2)
                    with col5:
                        games = player_stats['G'].iloc[0] if 'G' in player_stats.columns else 0
                        st.metric("Games Played", int(games))
                    with col6:
                        st.info("📅 2025 season data (current season)")
                
                # Detailed stats table
                st.subheader("Detailed Statistics")
                display_cols = ['Name', 'Team', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'BB', 'SO', 'AVG', 'OBP', 'SLG', 'OPS']
                available_cols = [col for col in display_cols if col in player_stats.columns]
                st.dataframe(player_stats[available_cols], use_container_width=True)
                
                # Performance charts
                st.subheader("Performance Visualization")
                
                # Create performance metrics chart
                metrics = ['AVG', 'OBP', 'SLG', 'OPS']
                available_metrics = [m for m in metrics if m in player_stats.columns]
                
                if available_metrics:
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
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No statistics found for this player in the selected year.")

elif page == "Team Stats":
    st.header("🏟️ Team Statistics")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Team Analysis")
        year = st.selectbox("Select Year", range(2020, 2026), index=5, key="team_year")  # Updated to include 2025
        
        if st.button("Load Team Stats"):
            with st.spinner("Loading team statistics..."):
                team_stats = load_team_stats(year)
                st.session_state.team_stats = team_stats
    
    with col2:
        if hasattr(st.session_state, 'team_stats') and not st.session_state.team_stats.empty:
            st.subheader(f"Team Statistics for {year}")
            
            # Add note for 2025
            if year == 2025:
                st.info("📅 2025 season data (current season)")
            
            # Team performance metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Teams", len(st.session_state.team_stats))
            with col2:
                avg_runs = st.session_state.team_stats['R'].mean()
                st.metric("Avg Runs/Team", f"{avg_runs:.1f}")
            with col3:
                avg_hr = st.session_state.team_stats['HR'].mean()
                st.metric("Avg HR/Team", f"{avg_hr:.1f}")
            with col4:
                avg_avg = st.session_state.team_stats['AVG'].mean()
                st.metric("League Avg BA", f"{avg_avg:.3f}")
            
            # Team rankings
            st.subheader("Team Rankings")
            
            # Top 10 teams by different metrics
            tab1, tab2, tab3 = st.tabs(["Runs", "Home Runs", "Batting Average"])
            
            with tab1:
                top_runs = st.session_state.team_stats.nlargest(10, 'R')[['Team', 'R', 'G']]
                st.dataframe(top_runs, use_container_width=True)
            
            with tab2:
                top_hr = st.session_state.team_stats.nlargest(10, 'HR')[['Team', 'HR', 'G']]
                st.dataframe(top_hr, use_container_width=True)
            
            with tab3:
                top_avg = st.session_state.team_stats.nlargest(10, 'AVG')[['Team', 'AVG', 'G']]
                st.dataframe(top_avg, use_container_width=True)
            
            # Team comparison chart
            st.subheader("Team Performance Comparison")
            
            # Select teams to compare
            teams = st.multiselect(
                "Select teams to compare:",
                options=st.session_state.team_stats['Team'].tolist(),
                default=st.session_state.team_stats['Team'].head(5).tolist()
            )
            
            if teams:
                team_data = st.session_state.team_stats[st.session_state.team_stats['Team'].isin(teams)]
                
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('Runs', 'Home Runs', 'Batting Average', 'OPS'),
                    specs=[[{"secondary_y": False}, {"secondary_y": False}],
                           [{"secondary_y": False}, {"secondary_y": False}]]
                )
                
                fig.add_trace(
                    go.Bar(x=team_data['Team'], y=team_data['R'], name='Runs'),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Bar(x=team_data['Team'], y=team_data['HR'], name='Home Runs'),
                    row=1, col=2
                )
                
                fig.add_trace(
                    go.Bar(x=team_data['Team'], y=team_data['AVG'], name='Batting Average'),
                    row=2, col=1
                )
                
                fig.add_trace(
                    go.Bar(x=team_data['Team'], y=team_data['OPS'], name='OPS'),
                    row=2, col=2
                )
                
                fig.update_layout(height=600, showlegend=False, title_text="Team Performance Comparison")
                st.plotly_chart(fig, use_container_width=True)

elif page == "League Leaders":
    st.header("🏆 League Leaders")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Leaderboard Settings")
        year = st.selectbox("Select Year", range(2020, 2026), index=5, key="leaders_year")  # Updated to include 2025
        
        stat_options = {
            'HR': 'Home Runs',
            'RBI': 'Runs Batted In',
            'R': 'Runs',
            'H': 'Hits',
            'AVG': 'Batting Average',
            'OPS': 'OPS',
            'SB': 'Stolen Bases'
        }
        
        selected_stat = st.selectbox("Select Statistic", list(stat_options.keys()), 
                                   format_func=lambda x: stat_options[x])
        
        if st.button("Load League Leaders"):
            with st.spinner("Loading league leaders..."):
                leaders = load_league_leaders(year, selected_stat)
                st.session_state.leaders = leaders
                st.session_state.selected_stat = selected_stat
    
    with col2:
        if hasattr(st.session_state, 'leaders') and not st.session_state.leaders.empty:
            st.subheader(f"Top 20 {stat_options[st.session_state.selected_stat]} Leaders - {year}")
            
            # Add note for 2025
            if year == 2025:
                st.info("📅 2025 season data (current season)")
            
            # Display top 10 in a nice format
            top_10 = st.session_state.leaders.head(10)
            
            for i, (_, player) in enumerate(top_10.iterrows(), 1):
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.markdown(f"**#{i}**")
                with col2:
                    st.markdown(f"**{player['Name']}** ({player.get('Team', 'N/A')})")
                with col3:
                    stat_value = player[st.session_state.selected_stat]
                    if st.session_state.selected_stat in ['AVG', 'OPS']:
                        st.markdown(f"**{stat_value:.3f}**")
                    else:
                        st.markdown(f"**{int(stat_value)}**")
                st.divider()
            
            # Full leaderboard table
            st.subheader("Complete Leaderboard")
            display_cols = ['Name', 'Team', st.session_state.selected_stat, 'G', 'AB']
            available_cols = [col for col in display_cols if col in st.session_state.leaders.columns]
            st.dataframe(st.session_state.leaders[available_cols], use_container_width=True)
            
            # Visualization
            st.subheader("Leaderboard Visualization")
            
            fig = px.bar(
                st.session_state.leaders.head(15),
                x='Name',
                y=st.session_state.selected_stat,
                title=f"Top 15 {stat_options[st.session_state.selected_stat]} Leaders",
                color=st.session_state.selected_stat,
                color_continuous_scale='viridis'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

elif page == "Game Logs":
    st.header("📊 Game Logs")
    
    st.info("Game logs feature requires player search. Use the Player Stats page to find a player first.")
    
    if hasattr(st.session_state, 'player_mlb_id'):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Game Log Settings")
            year = st.selectbox("Select Year", range(2020, 2026), index=5, key="logs_year")  # Updated to include 2025
            
            if st.button("Load Game Logs"):
                with st.spinner("Loading game logs..."):
                    logs = load_game_logs(st.session_state.player_mlb_id, year)
                    st.session_state.game_logs = logs
        
        with col2:
            if hasattr(st.session_state, 'game_logs') and not st.session_state.game_logs.empty:
                st.subheader(f"Game Logs for {st.session_state.player_name} - {year}")
                
                # Add note for 2025
                if year == 2025:
                    st.info("📅 2025 season data (current season)")
                
                # Summary statistics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Games Played", len(st.session_state.game_logs))
                with col2:
                    total_hits = st.session_state.game_logs['H'].sum()
                    st.metric("Total Hits", int(total_hits))
                with col3:
                    total_hr = st.session_state.game_logs['HR'].sum()
                    st.metric("Total HR", int(total_hr))
                with col4:
                    total_rbi = st.session_state.game_logs['RBI'].sum()
                    st.metric("Total RBI", int(total_rbi))
                
                # Game log table
                st.subheader("Detailed Game Logs")
                display_cols = ['Date', 'Team', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'BB', 'SO']
                available_cols = [col for col in display_cols if col in st.session_state.game_logs.columns]
                st.dataframe(st.session_state.game_logs[available_cols], use_container_width=True)
                
                # Performance over time
                st.subheader("Performance Over Time")
                
                if 'Date' in st.session_state.game_logs.columns:
                    # Convert date column and create cumulative stats
                    logs_with_date = st.session_state.game_logs.copy()
                    logs_with_date['Date'] = pd.to_datetime(logs_with_date['Date'])
                    logs_with_date = logs_with_date.sort_values('Date')
                    
                    # Create cumulative statistics
                    logs_with_date['Cumulative_HR'] = logs_with_date['HR'].cumsum()
                    logs_with_date['Cumulative_RBI'] = logs_with_date['RBI'].cumsum()
                    logs_with_date['Cumulative_H'] = logs_with_date['H'].cumsum()
                    
                    fig = make_subplots(
                        rows=2, cols=1,
                        subplot_titles=('Cumulative Home Runs', 'Cumulative RBIs'),
                        vertical_spacing=0.1
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=logs_with_date['Date'], y=logs_with_date['Cumulative_HR'], 
                                 name='HR', line=dict(color='red', width=3)),
                        row=1, col=1
                    )
                    
                    fig.add_trace(
                        go.Scatter(x=logs_with_date['Date'], y=logs_with_date['Cumulative_RBI'], 
                                 name='RBI', line=dict(color='blue', width=3)),
                        row=2, col=1
                    )
                    
                    fig.update_layout(height=600, title_text="Cumulative Performance Over Time")
                    st.plotly_chart(fig, use_container_width=True)

else:  # About page
    st.header("ℹ️ About This Dashboard")
    
    st.markdown("""
    ## Baseball Stats Dashboard
    
    This interactive dashboard provides comprehensive baseball statistics and analysis using the **pybaseball** library.
    
    ### Features:
    
    #### 🔍 Player Stats
    - Search for any MLB player by name
    - View detailed batting statistics
    - Interactive performance visualizations
    - Key metrics display (HR, RBI, AVG, OPS)
    - **NEW**: 2025 season data included!
    
    #### 🏟️ Team Stats
    - Team performance comparisons
    - League-wide team rankings
    - Interactive team selection and comparison charts
    - Multiple statistical categories
    - **NEW**: 2025 season data included!
    
    #### 🏆 League Leaders
    - Top performers in various categories
    - Home runs, RBIs, batting average, and more
    - Interactive leaderboards with visualizations
    - Top 20 rankings with detailed stats
    - **NEW**: 2025 season data included!
    
    #### 📊 Game Logs
    - Individual player game-by-game performance
    - Cumulative statistics over time
    - Performance trends and analysis
    - **NEW**: 2025 season data included!
    
    ### Data Source:
    - **pybaseball**: A Python package for baseball data analysis
    - Data from FanGraphs and Baseball Reference
    - Real-time statistics and historical data
    - **Updated**: Now includes 2025 season data
    
    ### Technology Stack:
    - **Streamlit**: Web application framework
    - **Plotly**: Interactive visualizations
    - **Pandas**: Data manipulation and analysis
    - **pybaseball**: Baseball data collection
    
    ### Getting Started:
    1. Navigate through the different pages using the sidebar
    2. Search for players using their full name (e.g., "Aaron Judge")
    3. Select different years to view historical data (2020-2025)
    4. Explore interactive charts and visualizations
    
    ### Note:
    - Data is cached for 1 hour to improve performance
    - Some features may take a moment to load due to data fetching
    - All statistics are sourced from official baseball databases
    - **2025 data**: Current season statistics (updated regularly)
    """)
    
    st.markdown("---")
    st.markdown("**Built with ❤️ using Streamlit and pybaseball**")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Baseball Stats Dashboard | Powered by pybaseball and Streamlit | Now with 2025 data!
    </div>
    """,
    unsafe_allow_html=True
)
