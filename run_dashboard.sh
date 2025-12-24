#!/bin/bash

# Baseball Dashboard Startup Script
echo "⚾ Starting Baseball Stats Dashboard..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies if needed
echo "Checking dependencies..."
pip install -r requirements.txt

# Start the dashboard
echo "Starting Streamlit dashboard..."
echo "The dashboard will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the dashboard"
echo ""

shiny run app.py
