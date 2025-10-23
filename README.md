# TEST ENVIRONMENT - Geopolitical Dashboard

This is a test environment for developing and testing new features for the Geopolitical Analysis Dashboard.

## Features Being Tested

### 1. Overview Choropleth Map Overlay
- Interactive choropleth map in the top-left corner of charts
- Highlights the country being hovered over in the main chart
- Shows country name and current metric value
- Updates dynamically as you hover over different data points

### 2. Functional Interactive Filters
- Dropdown filters that actually update the chart visualization
- Multiple chart variations embedded in HTML
- JavaScript-based filter switching
- No server required - works with static HTML files

## Current Status

🟡 **IN DEVELOPMENT**

- [x] Project structure created
- [ ] Choropleth map overlay implemented
- [ ] Functional filters implemented
- [ ] Charts deployed to GitHub Pages

## How to Use

1. Navigate to the deployed dashboard at: https://akfave99.github.io/Data_Dashboards_TEST_ENVIRONMENT/
2. Hover over data points to see the choropleth map highlight the country
3. Use filters to update the chart visualization
4. Compare with the main dashboard to verify new features work correctly

## File Structure

```
Data_Dashboards_TEST_ENVIRONMENT/
├── README.md                    # This file
├── docs/                        # GitHub Pages deployment folder
│   ├── index.html              # Home page
│   ├── chart*.html             # Individual chart pages
│   └── .nojekyll               # Disable Jekyll processing
├── geopolitical-dashboard/     # Source files
│   ├── chart_data.py           # Data module
│   ├── pages/                  # Chart creation functions
│   └── generate_charts.py      # Chart generation script
└── .github/
    └── workflows/
        └── deploy.yml          # GitHub Actions deployment
```

## Testing Checklist

- [ ] Choropleth map appears in top-left corner
- [ ] Choropleth highlights correct country on hover
- [ ] Filters update chart when changed
- [ ] All 6 charts load correctly
- [ ] Hover text shows descriptive labels
- [ ] Responsive design works on mobile/tablet
- [ ] Charts load from GitHub Pages (HTTP 200)

## Notes

This is a test environment separate from the main deployed dashboard. Changes here do not affect the production dashboard at https://akfave99.github.io/Data_Dashboards/
