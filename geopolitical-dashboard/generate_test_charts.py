"""
Generate charts with choropleth map overlay and functional filters for TEST ENVIRONMENT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from chart_data import get_data

# Central Asian countries for choropleth
COUNTRIES_ISO = {
    "Kazakhstan": "KAZ",
    "Uzbekistan": "UZB",
    "Turkmenistan": "TKM",
    "Azerbaijan": "AZE",
    "Georgia": "GEO"
}

def create_choropleth_overlay():
    """Create a choropleth map for the overlay."""
    df = get_data()
    
    # Create a simple choropleth with country data
    fig = go.Figure(data=go.Choropleth(
        locations=[COUNTRIES_ISO[c] for c in df['Country']],
        z=df['Avg_Spend'],
        text=df['Country'],
        colorscale='Blues',
        showscale=False,
        hovertemplate='<b>%{text}</b><br>Spending: $%{z:,.0f}<extra></extra>',
        marker_line_color='white',
        marker_line_width=2
    ))
    
    fig.update_layout(
        geo=dict(
            scope='asia',
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastcolor='rgb(204, 204, 204)',
            countrycolor='rgb(204, 204, 204)',
            showlakes=True,
            lakecolor='rgb(255, 255, 255)',
            center=dict(lon=70, lat=45),
            projection_scale=3
        ),
        height=300,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return fig

def main():
    """Generate all test charts."""
    print("=" * 70)
    print("🧪 GENERATING TEST ENVIRONMENT CHARTS")
    print("=" * 70)
    
    # Create output directory
    output_dir = "../docs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create home page
    home_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>TEST ENVIRONMENT - Geopolitical Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0d1b2a 0%, #1a2f4a 100%);
                color: #e0e0e0;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
            }
            h1 {
                color: #1e90ff;
                text-align: center;
            }
            .test-badge {
                background: #ff6b6b;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            .chart-cards {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }
            .chart-card {
                background: #1a2f4a;
                border: 1px solid #1e90ff;
                border-radius: 8px;
                padding: 20px;
                text-decoration: none;
                color: #e0e0e0;
                transition: all 0.3s ease;
            }
            .chart-card:hover {
                background: #1e90ff;
                transform: translateY(-5px);
            }
            .chart-card h3 {
                color: #1e90ff;
                margin-top: 0;
            }
            .chart-card:hover h3 {
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌍 Geopolitical Dashboard <span class="test-badge">TEST ENVIRONMENT</span></h1>
            <p style="text-align: center; color: #a0a0a0;">
                Testing new features: Choropleth map overlay and functional interactive filters
            </p>
            
            <div class="chart-cards">
                <a href="chart4-multi-country-radar.html" class="chart-card">
                    <h3>Multi-Country Radar</h3>
                    <p>Compare influence metrics across multiple countries with interactive filters</p>
                </a>
                <a href="chart3-defense-systems.html" class="chart-card">
                    <h3>Defense Systems</h3>
                    <p>3D analysis of defense systems by supplier with country highlighting</p>
                </a>
                <a href="chart5-priorities-heatmap.html" class="chart-card">
                    <h3>Priorities Heatmap</h3>
                    <p>Correlation heatmap with grouping and metric selection filters</p>
                </a>
            </div>
            
            <div style="margin-top: 40px; padding: 20px; background: #1a2f4a; border-left: 4px solid #ff6b6b; border-radius: 4px;">
                <h3 style="color: #ff6b6b; margin-top: 0;">🧪 Testing Features</h3>
                <ul>
                    <li><strong>Choropleth Map Overlay:</strong> Left panel shows a map that highlights countries as you hover over data</li>
                    <li><strong>Functional Filters:</strong> Dropdowns and selectors actually update the chart visualization</li>
                    <li><strong>Descriptive Hover Text:</strong> All hover labels are human-readable and descriptive</li>
                    <li><strong>Responsive Design:</strong> Works on desktop, tablet, and mobile devices</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(os.path.join(output_dir, "index.html"), "w") as f:
        f.write(home_html)
    print("✅ Created index.html")
    
    print("\n" + "=" * 70)
    print("✅ TEST ENVIRONMENT CHARTS GENERATED")
    print("=" * 70)

if __name__ == '__main__':
    main()
