"""
Generate charts with functional filters and hover synchronization
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
from chart_data import get_data

COUNTRIES_ISO = {
    "Kazakhstan": "KAZ",
    "Uzbekistan": "UZB",
    "Turkmenistan": "TKM",
    "Azerbaijan": "AZE",
    "Georgia": "GEO"
}

def create_choropleth_html():
    """Create a choropleth map HTML with main countries and neighboring countries."""
    import re
    df = get_data()
    
    # Main countries (5)
    main_countries = ['Kazakhstan', 'Uzbekistan', 'Turkmenistan', 'Azerbaijan', 'Georgia']
    main_locations = [COUNTRIES_ISO[c] for c in main_countries]
    main_z = [100000000, 100000000, 100000000, 100000000, 100000000]  # Consistent baseline for all 5 countries
    
    # Neighboring countries (neutral gray styling) - expanded for geographic context
    neighboring_countries = {
        # Direct neighbors
        'RUS': 'Russia',
        'CHN': 'China',
        'AFG': 'Afghanistan',
        'IRN': 'Iran',
        'TUR': 'Turkey',
        'ARM': 'Armenia',
        'KGZ': 'Kyrgyzstan',
        'TJK': 'Tajikistan',
        # Extended context
        'PAK': 'Pakistan',
        'IND': 'India',
        'MNG': 'Mongolia',
        # European context
        'ROU': 'Romania',
        'BGR': 'Bulgaria',
        'GRC': 'Greece',
        'UKR': 'Ukraine',
        'POL': 'Poland',
        # Middle East context
        'SYR': 'Syria',
        'IRQ': 'Iraq',
        'SAU': 'Saudi Arabia',
        'ARE': 'UAE',
        'OMN': 'Oman',
        'QAT': 'Qatar',
        'BHR': 'Bahrain',
        'KWT': 'Kuwait',
        'JOR': 'Jordan',
        'ISR': 'Israel',
        'PSE': 'Palestine',
        'LBN': 'Lebanon',
    }
    
    fig = go.Figure()
    
    # Add main countries trace (with color)
    fig.add_trace(go.Choropleth(
        locations=main_locations,
        z=main_z,
        text=main_countries,
        colorscale='Blues',
        showscale=False,
        hovertemplate='<b>%{text}</b><br>Spending: $%{z:,.0f}<extra></extra>',
        marker_line_color='white',
        marker_line_width=2,
        name='Main Countries'
    ))
    
    # Add neighboring countries trace (neutral gray)
    fig.add_trace(go.Choropleth(
        locations=list(neighboring_countries.keys()),
        z=[50000000] * len(neighboring_countries),  # Neutral value
        text=list(neighboring_countries.values()),
        colorscale=[[0, 'rgb(220, 220, 220)'], [1, 'rgb(200, 200, 200)']],
        showscale=False,
        hovertemplate='<b>%{text}</b> (Neighboring)<extra></extra>',
        marker_line_color='white',
        marker_line_width=1,
        name='Neighboring Countries'
    ))
    
    fig.update_layout(
        geo=dict(
            scope='asia',
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            countrycolor='rgb(204, 204, 204)',
            showlakes=True,
            lakecolor='rgb(255, 255, 255)',
            center=dict(lon=70, lat=45),
            projection_scale=3
        ),
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    
    html_full = fig.to_html(include_plotlyjs=False, div_id="choropleth-overlay")
    
    # Extract just the body content, removing the outer html/head/body tags
    body_match = re.search(r'<body>(.*?)</body>', html_full, re.DOTALL)
    if body_match:
        return body_match.group(1).strip()
    else:
        return html_full

def create_radar_variations():
    """Create multiple radar chart variations."""
    df = get_data()
    variations = {}
    
    countries_list = df['Country'].unique().tolist()
    
    for metric in ["influence", "matrix"]:
        for num_countries in [3, 5]:
            selected_countries = countries_list[:num_countries]
            
            if metric == "influence":
                metric_columns = ['Influence_US_numeric', 'Influence_Russia_numeric', 
                                'Influence_China_numeric', 'Influence_Turkiye_Israel_numeric']
                metric_labels = ['US Influence', 'Russia Influence', 'China Influence', 'Türkiye/Israel Influence']
            else:
                metric_columns = ['Matrix_US_numeric', 'Matrix_Russia_numeric', 
                                'Matrix_China_numeric', 'Matrix_Turkiye_Israel_numeric']
                metric_labels = ['US Matrix', 'Russia Matrix', 'China Matrix', 'Türkiye/Israel Matrix']
            
            fig = go.Figure()
            
            for country in selected_countries:
                country_data = df[df['Country'] == country]
                if len(country_data) == 0:
                    continue
                
                row = country_data.iloc[0]
                values = []
                for col in metric_columns:
                    val = row.get(col, np.nan)
                    if pd.isna(val):
                        val = 0
                    values.append(float(val))
                
                values_closed = values + [values[0]]
                labels_closed = metric_labels + [metric_labels[0]]
                
                fig.add_trace(go.Scatterpolar(
                    r=values_closed,
                    theta=labels_closed,
                    fill='toself',
                    name=country,
                    line=dict(width=2),
                    opacity=0.7,
                    customdata=[country] * len(values_closed),
                    hovertemplate="<b>%{fullData.name}</b><br>" +
                                  "Supplier: %{theta}<br>" +
                                  "Level: %{r:.1f}<br>" +
                                  "<extra></extra>"
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 3],
                        tickvals=[1, 2, 3],
                        ticktext=['Low', 'Medium', 'High']
                    )
                ),
                showlegend=True,
                height=700,
                legend=dict(
                    x=1.05,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                    bgcolor='rgba(255, 255, 255, 0.8)',
                    bordercolor='rgba(0, 0, 0, 0.2)',
                    borderwidth=1
                ),
                margin=dict(r=200)  # Add right margin for legend
            )
            
            key = f"{metric}_{num_countries}countries"
            variations[key] = fig
    
    return variations

def create_defense_systems_variations():
    """Create multiple defense systems chart variations."""
    df = get_data()
    variations = {}
    
    suppliers = ['all', 'US', 'Russia', 'China', 'Turkiye_Israel']
    
    for supplier_filter in suppliers:
        plot_data = []
        
        for _, row in df.iterrows():
            country = row['Country']
            suppliers_data = [
                ('US', row.get('Systems_US'), row.get('Influence_US_numeric', 0)),
                ('Russia', row.get('Systems_Russia'), row.get('Influence_Russia_numeric', 0)),
                ('China', row.get('Systems_China'), row.get('Influence_China_numeric', 0)),
                ('Turkiye_Israel', row.get('Systems_Turkiye_Israel'), row.get('Influence_Turkiye_Israel_numeric', 0))
            ]
            
            for supplier, systems, influence in suppliers_data:
                if pd.isna(systems) or systems == '' or systems == 'N/A':
                    continue
                if supplier_filter != "all" and supplier != supplier_filter:
                    continue
                system_count = len([s.strip() for s in str(systems).replace(';', ',').split(',') if s.strip()])
                plot_data.append({
                    'Country': country,
                    'Supplier': supplier,
                    'System_Count': system_count,
                    'Influence': influence if not pd.isna(influence) else 0,
                    'Systems': systems
                })
        
        if not plot_data:
            fig = go.Figure()
            fig.add_annotation(text="No data available")
            variations[supplier_filter] = fig
            continue
        
        plot_df = pd.DataFrame(plot_data)
        countries = plot_df['Country'].unique()
        country_mapping = {country: i for i, country in enumerate(countries)}
        plot_df['Country_Z'] = plot_df['Country'].map(country_mapping)
        
        supplier_colors = {
            'US': '#1f77b4',
            'Russia': '#d62728',
            'China': '#ff7f0e',
            'Turkiye_Israel': '#2ca02c'
        }
        
        fig = go.Figure()
        
        for supplier in plot_df['Supplier'].unique():
            supplier_data = plot_df[plot_df['Supplier'] == supplier]
            supplier_display = {
                'US': 'United States',
                'Russia': 'Russia',
                'China': 'China',
                'Turkiye_Israel': 'Türkiye/Israel'
            }.get(supplier, supplier)
            
            fig.add_trace(go.Scatter3d(
                x=supplier_data['System_Count'],
                y=supplier_data['Influence'],
                z=supplier_data['Country_Z'],
                mode='markers',
                marker=dict(
                    size=supplier_data['Influence'] * 3 + 5,
                    color=supplier_colors.get(supplier, '#636EFA'),
                    opacity=0.8,
                    line=dict(width=1, color='white')
                ),
                name=supplier_display,
                text=supplier_data['Country'],
                customdata=supplier_data['Country'].values,
                hovertemplate="<b>%{text}</b><br>" +
                              f"Supplier: {supplier_display}<br>" +
                              "System Count: %{x}<br>" +
                              "Influence Level: %{y}<br>" +
                              "<extra></extra>"
            ))
        
        fig.update_layout(
            scene=dict(
                xaxis_title="Number of Defense Systems",
                yaxis_title="Influence Level (1-3)",
                zaxis_title="Countries",
                zaxis=dict(
                    tickmode='array',
                    tickvals=list(range(len(countries))),
                    ticktext=countries
                ),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
            ),
            height=700
        )
        
        variations[supplier_filter] = fig
    
    return variations

def create_heatmap_variations():
    """Create multiple heatmap variations."""
    df = get_data()
    variations = {}
    
    for grouping in ["country", "supplier"]:
        for intensity_metric in ["influence", "matrix"]:
            if intensity_metric == "influence":
                metric_cols = ['Influence_US_numeric', 'Influence_Russia_numeric', 
                             'Influence_China_numeric', 'Influence_Turkiye_Israel_numeric']
                metric_labels = ['US', 'Russia', 'China', 'Türkiye/Israel']
            else:
                metric_cols = ['Matrix_US_numeric', 'Matrix_Russia_numeric', 
                             'Matrix_China_numeric', 'Matrix_Turkiye_Israel_numeric']
                metric_labels = ['US', 'Russia', 'China', 'Türkiye/Israel']
            
            if grouping == "country":
                countries = df['Country'].unique()
                z_data = []
                for country in countries:
                    country_data = df[df['Country'] == country]
                    row = []
                    for col in metric_cols:
                        val = country_data[col].iloc[0] if len(country_data) > 0 else 0
                        row.append(float(val) if pd.notna(val) else 0)
                    z_data.append(row)
                
                fig = go.Figure(data=go.Heatmap(
                    z=z_data,
                    x=metric_labels,
                    y=countries,
                    colorscale='RdYlBu_r',
                    colorbar=dict(title="Level"),
                    customdata=[[c] for c in countries],
                    hovertemplate="<b>Country: %{y}</b><br>" +
                                  "Supplier: %{x}<br>" +
                                  f"{intensity_metric.capitalize()} Level: %{{z:.1f}}<br>" +
                                  "<extra></extra>"
                ))
                fig.update_layout(
                    xaxis_title="Supplier",
                    yaxis_title="Country",
                    height=600
                )
            else:
                suppliers = metric_labels
                z_data = []
                for i, supplier in enumerate(suppliers):
                    row = []
                    for country in df['Country'].unique():
                        country_data = df[df['Country'] == country]
                        val = country_data[metric_cols[i]].iloc[0] if len(country_data) > 0 else 0
                        row.append(float(val) if pd.notna(val) else 0)
                    z_data.append(row)
                
                fig = go.Figure(data=go.Heatmap(
                    z=z_data,
                    x=df['Country'].unique(),
                    y=suppliers,
                    colorscale='RdYlBu_r',
                    colorbar=dict(title="Level"),
                    customdata=[[c] for c in df['Country'].unique()],
                    hovertemplate="<b>Supplier: %{y}</b><br>" +
                                  "Country: %{x}<br>" +
                                  f"{intensity_metric.capitalize()} Level: %{{z:.1f}}<br>" +
                                  "<extra></extra>"
                ))
                fig.update_layout(
                    xaxis_title="Country",
                    yaxis_title="Supplier",
                    height=600
                )
            
            key = f"{grouping}_{intensity_metric}"
            variations[key] = fig
    
    return variations

def create_page_with_functional_filters(chart_title, chart_id, variations_dict, filter_config):
    """Create a page with functional filters and hover sync."""
    
    choropleth_html = create_choropleth_html()
    
    # Convert variations to JSON using Plotly's JSON serialization
    variations_json = {}
    for key, fig in variations_dict.items():
        # Use Plotly's to_json() which handles numpy arrays
        fig_json = json.loads(fig.to_json())
        variations_json[key] = fig_json
    
    # Create filter HTML
    filters_html = '<div class="filters">'
    for filter_name, filter_options in filter_config.items():
        filter_id = f"{chart_id}_{filter_name.lower().replace(' ', '_')}"
        filters_html += f'''
        <div class="filter-group">
            <label>{filter_name}:</label>
            <select class="filter-select" id="{filter_id}" onchange="updateChart()">
        '''
        for option in filter_options:
            filters_html += f'<option value="{option}">{option}</option>'
        filters_html += '</select></div>'
    
    # Add test country highlight filter (for debugging)
    filters_html += f'''
    <div class="filter-group">
        <label>Test Country Highlight:</label>
        <select class="filter-select" id="{chart_id}_test_country" onchange="testHighlightCountry()">
            <option value="">-- Select a country --</option>
            <option value="Kazakhstan">Kazakhstan</option>
            <option value="Uzbekistan">Uzbekistan</option>
            <option value="Turkmenistan">Turkmenistan</option>
            <option value="Azerbaijan">Azerbaijan</option>
            <option value="Georgia">Georgia</option>
        </select>
    </div>
    '''
    filters_html += '</div>'
    
    # Create JavaScript for functional filters and hover sync
    filter_js = f'''
    <script>
    window.chartVariations = {json.dumps(variations_json)};
    window.filterConfig = {json.dumps(filter_config)};
    window.chartId = '{chart_id}';
    
    function attachChartHoverListeners() {{
        const chartDiv = document.getElementById('{chart_id}-chart');
        console.log('🔍 Attaching hover listeners to chart...');
        
        // Create handlers
        window.chartHoverHandler = function(data) {{
            console.log('✅ Hover event fired!', data);
            if (data.points && data.points[0].customdata) {{
                let country = data.points[0].customdata;
                // Handle both string and array customdata
                if (Array.isArray(country)) {{
                    country = country[0];
                }}
                console.log('✅ Country from customdata:', country);
                highlightCountryInChoropleth(country);
            }}
        }};
        
        window.chartUnhoverHandler = function(data) {{
            console.log('✅ Unhover event fired!');
            resetChoroplethHighlight();
        }};
        
        // Poll the chart's internal hover state using Plotly's internal data
        let lastHoveredCountry = null;
        let debugLogged = false;
        window.hoverPollingInterval = setInterval(function() {{
            try {{
                // Check if there's hover data in the plot
                if (chartDiv._hoverdata && chartDiv._hoverdata.length > 0) {{
                    const hoverPoint = chartDiv._hoverdata[0];
                    
                    // Log available properties once for debugging
                    if (!debugLogged) {{
                        console.log('�� Hover data detected. Available properties:', Object.keys(hoverPoint));
                        console.log('📍 Full hover point:', hoverPoint);
                        debugLogged = true;
                    }}
                    
                    // Try to get country from customdata
                    let country = null;
                    
                    // Method 1: Direct customdata
                    if (hoverPoint.customdata) {{
                        country = hoverPoint.customdata;
                        if (Array.isArray(country)) {{
                            country = country[0];
                        }}
                        console.log('✅ Country from customdata:', country);
                    }}
                    
                    // Method 2: If customdata not available, try to get from fullData
                    if (!country && hoverPoint.fullData && hoverPoint.fullData.customdata) {{
                        const customdataArray = hoverPoint.fullData.customdata;
                        const pointIndex = hoverPoint.pointIndex;
                        if (pointIndex !== undefined && customdataArray[pointIndex]) {{
                            country = customdataArray[pointIndex];
                            console.log('✅ Country from fullData.customdata[' + pointIndex + ']:', country);
                        }}
                    }}
                    
                    // Method 3: If still no country, try to get from fullData.name
                    if (!country && hoverPoint.fullData && hoverPoint.fullData.name) {{
                        country = hoverPoint.fullData.name;
                        console.log('✅ Country from fullData.name:', country);
                    }}
                    
                    if (country && country !== lastHoveredCountry) {{
                        console.log('✅ Country changed from', lastHoveredCountry, 'to', country);
                        if (lastHoveredCountry !== null) {{
                            resetChoroplethHighlight();
                        }}
                        lastHoveredCountry = country;
                        highlightCountryInChoropleth(country);
                    }}
                }} else if (lastHoveredCountry !== null) {{
                    console.log('✅ Hover ended, resetting all countries');
                    lastHoveredCountry = null;
                    resetChoroplethHighlight();
                    debugLogged = false;
                }}
            }} catch (e) {{
                console.log('❌ Error in polling:', e.message);
            }}
        }}, 50);
        console.log('✅ Hover polling started (using Plotly internal state with fallbacks)');
    }}
    
    function updateChart() {{
        const filters = {{}};
        const filterSelects = document.querySelectorAll('.filter-select');
        filterSelects.forEach(select => {{
            const key = select.id.replace('{chart_id}_', '');
            // Skip the test_country filter - it's only for manual highlighting
            if (key !== 'test_country') {{
                filters[key] = select.value;
            }}
        }});
        
        // Build the key from filter values
        const key = Object.values(filters).join('_').toLowerCase();
        console.log('📊 updateChart called with key:', key);
        console.log('📊 Available variations:', Object.keys(window.chartVariations));
        
        if (window.chartVariations[key]) {{
            const chartData = window.chartVariations[key];
            console.log('📊 Chart data found, rendering...');
            Plotly.react('{chart_id}-chart', chartData.data, chartData.layout, {{responsive: true}});
            
            // Add hover event listeners after chart is rendered
            setTimeout(function() {{
                attachChartHoverListeners();
            }}, 100);
        }} else {{
            console.log('❌ Chart variation not found for key:', key);
        }}
    }}
    window.testHighlightCountry = function() {{
        const testSelect = document.getElementById('{chart_id}_test_country');
        const country = testSelect.value;
        console.log('🧪 Test highlight triggered for country:', country);
        console.log('🧪 testSelect element:', testSelect);
        console.log('🧪 highlightCountryInChoropleth function exists:', typeof highlightCountryInChoropleth);
        
        if (country) {{
            console.log('🧪 Calling highlightCountryInChoropleth with:', country);
            highlightCountryInChoropleth(country);
        }} else {{
            console.log('🧪 Resetting choropleth colors');
            resetChoroplethHighlight();
        }}
    }};

    window.highlightCountryInChoropleth = function(country) {{
        const countryCode = getCountryCode(country);
        console.log('🎯 Hover detected - Country:', country, 'Code:', countryCode);
        
        if (countryCode) {{
            // Get the original z values for main countries
            const originalZ = window.choroplethOriginalZ || [100000000, 100000000, 100000000, 100000000, 100000000];
            const codes = ['KAZ', 'UZB', 'TKM', 'AZE', 'GEO'];
            
            // Create new z values - brighten hovered country, keep others at baseline
            const newZ = originalZ.map((val, idx) => {{
                if (codes[idx] === countryCode) {{
                    return 150000000;  // Bright blue for hovered country
                }} else {{
                    return 100000000;  // Light blue for other main countries
                }}
            }});
            
            console.log('🎯 Updating Z values for trace 0 (main countries):', newZ);
            
            // Update z values for trace 0 (main countries) to change colors
            Plotly.restyle('choropleth-overlay', {{
                'z': [newZ]
            }}, 0);
            
            console.log('✅ Plotly.restyle called successfully');
        }} else {{
            console.log('❌ Country code not found for:', country);
        }}
    }};
    
    window.resetChoroplethHighlight = function() {{
        console.log('Resetting choropleth colors');
        // Reset to original z values
        const originalZ = window.choroplethOriginalZ || [100000000, 100000000, 100000000, 100000000, 100000000];
        Plotly.restyle('choropleth-overlay', {{
            'z': [originalZ]
        }}, 0);
    }}
    
    window.getCountryCode = function(country) {{
        const codes = {{'Kazakhstan': 'KAZ', 'Uzbekistan': 'UZB', 'Turkmenistan': 'TKM', 'Azerbaijan': 'AZE', 'Georgia': 'GEO'}};
        return codes[country];
    }};
    
    // Initialize with first variation
    window.addEventListener('load', function() {{
        const firstKey = Object.keys(window.chartVariations)[0];
        if (firstKey) {{
            const chartData = window.chartVariations[firstKey];
            Plotly.newPlot('{chart_id}-chart', chartData.data, chartData.layout, {{responsive: true}});
            
            // Add hover event listeners after chart is rendered
            setTimeout(function() {{
                attachChartHoverListeners();
            }}, 100);
        }}
    }});
    </script>
    '''
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{chart_title} - TEST ENVIRONMENT</title>
        <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0d1b2a 0%, #1a2f4a 100%);
                color: #e0e0e0;
                min-height: 100vh;
            }}
            
            .navbar {{
                background: #0d1b2a;
                padding: 15px 20px;
                border-bottom: 2px solid #1e90ff;
                position: sticky;
                top: 0;
                z-index: 100;
                box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            }}
            
            .navbar-brand {{
                font-size: 24px;
                font-weight: bold;
                color: #1e90ff;
                margin-right: 30px;
            }}
            
            .nav-tabs {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }}
            
            .nav-tab {{
                padding: 8px 15px;
                background: #1a2f4a;
                border: 1px solid #1e90ff;
                color: #e0e0e0;
                cursor: pointer;
                border-radius: 4px;
                transition: all 0.3s ease;
                text-decoration: none;
            }}
            
            .nav-tab:hover {{
                background: #1e90ff;
                color: white;
            }}
            
            .test-badge {{
                display: inline-block;
                background: #ff6b6b;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                margin-left: 10px;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            .page-title {{
                font-size: 28px;
                font-weight: bold;
                margin: 20px 0 10px 0;
                color: #1e90ff;
            }}
            
            .page-subtitle {{
                font-size: 14px;
                color: #a0a0a0;
                margin-bottom: 20px;
            }}
            
            .chart-wrapper {{
                display: grid;
                grid-template-columns: 300px 1fr;
                gap: 20px;
                margin-bottom: 20px;
            }}
            
            .choropleth-container {{
                background: #1a2f4a;
                border: 1px solid #1e90ff;
                border-radius: 8px;
                padding: 10px;
                height: fit-content;
            }}
            
            .choropleth-title {{
                font-size: 12px;
                font-weight: bold;
                color: #1e90ff;
                margin-bottom: 10px;
                text-align: center;
            }}
            
            .main-chart {{
                background: #1a2f4a;
                border: 1px solid #1e90ff;
                border-radius: 8px;
                padding: 15px;
            }}
            
            .filters {{
                background: #1a2f4a;
                border: 1px solid #1e90ff;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 20px;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
            }}
            
            .filter-group {{
                display: flex;
                flex-direction: column;
            }}
            
            .filter-group label {{
                font-weight: bold;
                color: #1e90ff;
                margin-bottom: 5px;
                font-size: 14px;
            }}
            
            .filter-select {{
                padding: 8px;
                background: #0d1b2a;
                color: #e0e0e0;
                border: 1px solid #1e90ff;
                border-radius: 4px;
                font-size: 14px;
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            
            .filter-select:hover {{
                border-color: #4da6ff;
                background: #1a2f4a;
            }}
            
            .filter-select:focus {{
                outline: none;
                border-color: #4da6ff;
                box-shadow: 0 0 5px rgba(30, 144, 255, 0.5);
            }}
            
            .footer {{
                text-align: center;
                padding: 20px;
                color: #666;
                font-size: 12px;
                border-top: 1px solid #1e90ff;
                margin-top: 40px;
            }}
            
            @media (max-width: 768px) {{
                .chart-wrapper {{
                    grid-template-columns: 1fr;
                }}
                
                .choropleth-container {{
                    height: 300px;
                }}
                
                .filters {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="navbar">
            <span class="navbar-brand">🌍 Geopolitical Dashboard <span class="test-badge">TEST ENVIRONMENT</span></span>
            <div class="nav-tabs">
                <a href="index.html" class="nav-tab">Home</a>
                <a href="chart4-multi-country-radar.html" class="nav-tab">Multi-Country Radar</a>
                <a href="chart3-defense-systems.html" class="nav-tab">Defense Systems</a>
                <a href="chart5-priorities-heatmap.html" class="nav-tab">Priorities Heatmap</a>
            </div>
        </div>
        
        <div class="container">
            <h1 class="page-title">{chart_title}</h1>
            <p class="page-subtitle">TEST ENVIRONMENT - Functional filters + Choropleth hover sync</p>
            
            {filters_html}
            
            <div class="chart-wrapper">
                <div class="choropleth-container">
                    <div class="choropleth-title">Country Highlight (Hover over chart)</div>
                    {choropleth_html}
                    <script>
                        // Initialize choropleth data after a short delay to ensure Plotly has rendered
                        setTimeout(function() {{
                            try {{
                                const choroplethDiv = document.getElementById('choropleth-overlay');
                                if (choroplethDiv && choroplethDiv.data && choroplethDiv.data.length > 0) {{
                                    // Get the z values from the first trace (main countries)
                                    const mainCountriesTrace = choroplethDiv.data[0];
                                    if (mainCountriesTrace && mainCountriesTrace.z) {{
                                        window.choroplethOriginalZ = mainCountriesTrace.z;
                                        console.log('✅ Choropleth Z values captured from Plotly:', window.choroplethOriginalZ);
                                    }} else {{
                                        // Fallback to hardcoded values
                                        window.choroplethOriginalZ = [100000000, 100000000, 100000000, 100000000, 100000000];
                                        console.log('⚠️ Using fallback Z values:', window.choroplethOriginalZ);
                                    }}
                                }} else {{
                                    console.log('❌ Choropleth div not found or not rendered yet');
                                    window.choroplethOriginalZ = [100000000, 100000000, 100000000, 100000000, 100000000];
                                }}
                            }} catch (e) {{
                                console.log('❌ Error initializing choropleth:', e.message);
                                window.choroplethOriginalZ = [100000000, 100000000, 100000000, 100000000, 100000000];
                            }}
                        }}, 500);
                    </script>
                </div>
                <div class="main-chart">
                    <div id="{chart_id}-chart" style="width:100%;height:700px;"></div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2025 Geopolitical Analysis Dashboard - TEST ENVIRONMENT</p>
            <p>Main dashboard: https://akfave99.github.io/Data_Dashboards/</p>
        </div>
        
        {filter_js}
    </body>
    </html>
    """
    
    return html_template

def main():
    """Generate all charts with functional filters."""
    print("=" * 70)
    print("🧪 GENERATING CHARTS WITH FUNCTIONAL FILTERS & HOVER SYNC")
    print("=" * 70)
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), "docs")
    os.makedirs(output_dir, exist_ok=True)
    
    # Chart 4 - Multi-Country Radar
    print("\n📊 Generating Chart 4 - Multi-Country Radar...")
    radar_variations = create_radar_variations()
    radar_html = create_page_with_functional_filters(
        "Multi-Country Influence Radar",
        "chart4",
        radar_variations,
        {
            "Metric Type": ["influence", "matrix"],
            "Countries": ["3countries", "5countries"]
        }
    )
    with open(os.path.join(output_dir, "chart4-multi-country-radar.html"), "w") as f:
        f.write(radar_html)
    print("✅ Chart 4 created with functional filters")
    
    # Chart 3 - Defense Systems
    print("📊 Generating Chart 3 - Defense Systems...")
    defense_variations = create_defense_systems_variations()
    defense_html = create_page_with_functional_filters(
        "Defense Systems 3D Analysis",
        "chart3",
        defense_variations,
        {
            "Supplier Filter": list(defense_variations.keys())
        }
    )
    with open(os.path.join(output_dir, "chart3-defense-systems.html"), "w") as f:
        f.write(defense_html)
    print("✅ Chart 3 created with functional filters")
    
    # Chart 5 - Heatmap
    print("📊 Generating Chart 5 - Priorities Heatmap...")
    heatmap_variations = create_heatmap_variations()
    heatmap_html = create_page_with_functional_filters(
        "Defense Priorities Correlation Heatmap",
        "chart5",
        heatmap_variations,
        {
            "Grouping": ["country", "supplier"],
            "Intensity Metric": ["influence", "matrix"]
        }
    )
    with open(os.path.join(output_dir, "chart5-priorities-heatmap.html"), "w") as f:
        f.write(heatmap_html)
    print("✅ Chart 5 created with functional filters")
    
    print("\n" + "=" * 70)
    print("✅ ALL CHARTS GENERATED WITH FUNCTIONAL FILTERS")
    print("=" * 70)
    print(f"\n📁 Output directory: {os.path.abspath(output_dir)}")
    print("\n🎉 Features implemented:")
    print("   ✅ Functional interactive filters")
    print("   ✅ Choropleth hover synchronization")
    print("   ✅ Descriptive hover text")
    print("   ✅ Responsive design")
    print("   ✅ Professional dark theme")

if __name__ == '__main__':
    main()
