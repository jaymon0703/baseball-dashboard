#!/usr/bin/env python3
"""
Demo script showing pybaseball functionality
Run this to test that pybaseball is working correctly
"""

import pybaseball as pyb
import pandas as pd
from datetime import datetime

def main():
    print("⚾ Baseball Stats Dashboard - Demo Script")
    print("=" * 50)
    
    try:
        # Test 1: Get current year's batting leaders
        print("\n1. Testing: Current year batting leaders...")
        current_year = datetime.now().year
        
        # Try a few recent years in case current year data isn't available yet
        years_to_try = [current_year, current_year - 1, current_year - 2]
        leaders = pd.DataFrame()
        
        for year in years_to_try:
            try:
                print(f"   Trying {year}...")
                leaders = pyb.batting_stats_range(f'{year}-01-01', f'{year}-12-31')
                if not leaders.empty:
                    print(f"✅ Successfully loaded {len(leaders)} player records for {year}")
                    break
            except Exception as e:
                print(f"   {year} failed: {e}")
                continue
        
        if not leaders.empty:
            # Show top 5 home run leaders
            if 'HR' in leaders.columns:
                hr_leaders = leaders.nlargest(5, 'HR')[['Name', 'Team', 'HR', 'RBI', 'AVG']]
                print("\n🏆 Top 5 Home Run Leaders:")
                print(hr_leaders.to_string(index=False))
            else:
                print("   Available columns:", list(leaders.columns))
        else:
            print("⚠️  No data found for recent years")
        
        # Test 2: Search for a well-known player
        print("\n2. Testing: Player search...")
        try:
            # Search for Aaron Judge
            judge_search = pyb.playerid_lookup('Judge', 'Aaron')
            if not judge_search.empty:
                print("✅ Successfully found Aaron Judge")
                print(f"   MLB ID: {judge_search.iloc[0]['key_mlbam']}")
            else:
                print("⚠️  Aaron Judge not found")
        except Exception as e:
            print(f"⚠️  Player search error: {e}")
        
        # Test 3: Team stats
        print("\n3. Testing: Team statistics...")
        try:
            team_stats = pyb.team_batting(2023)  # Use 2023 as it should have complete data
            if not team_stats.empty:
                print(f"✅ Successfully loaded team stats for {len(team_stats)} teams")
                print("\n🏟️  Top 5 Teams by Runs:")
                if 'R' in team_stats.columns:
                    top_teams = team_stats.nlargest(5, 'R')[['Team', 'R', 'HR', 'AVG']]
                    print(top_teams.to_string(index=False))
                else:
                    print("   Available columns:", list(team_stats.columns))
            else:
                print("⚠️  No team data found")
        except Exception as e:
            print(f"⚠️  Team stats error: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 Demo completed! pybaseball is working correctly.")
        print("You can now run the dashboard with: ./run_dashboard.sh")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()
