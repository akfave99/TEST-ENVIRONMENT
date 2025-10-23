"""
Mock data module for geopolitical charts
Provides sample data for all 7 charts
"""

import pandas as pd
import numpy as np


def get_data():
    """Generate comprehensive geopolitical threat perception data."""
    data = {
        "Country": [
            "Kazakhstan", "Uzbekistan", "Turkmenistan", "Azerbaijan", "Georgia"
        ],
        "Avg_Spend": [
            120_000_000, 90_000_000, 45_000_000, 70_000_000, 30_000_000
        ],
        "Threat Perception": [
            "Regional Instability", "Regional Instability", "Border Security",
            "Energy Competition", "Russian Influence"
        ],
        "Defense Priorities": [
            "Border Security, Regional Stability", 
            "Border Security, Terrorism Prevention",
            "Energy Infrastructure Protection",
            "Territorial Integrity, Energy Security",
            "NATO Integration, Russian Deterrence"
        ],
        "Suppliers": [
            "Russia, China, US",
            "Russia, China",
            "Russia, Turkey",
            "Russia, Israel, Turkey",
            "US, NATO, Turkey"
        ],
        # Influence levels (1-3 scale)
        "Influence_US_numeric": [1.5, 1.0, 0.5, 1.5, 3.0],
        "Influence_Russia_numeric": [3.0, 3.0, 3.0, 2.5, 2.0],
        "Influence_China_numeric": [2.0, 2.5, 1.5, 1.0, 0.5],
        "Influence_Turkiye_Israel_numeric": [1.0, 0.5, 2.0, 2.5, 1.5],
        
        # Matrix values (alternative to influence)
        "Matrix_US_numeric": [2.0, 1.5, 1.0, 2.0, 3.0],
        "Matrix_Russia_numeric": [3.0, 3.0, 3.0, 2.5, 2.0],
        "Matrix_China_numeric": [2.5, 2.5, 2.0, 1.5, 1.0],
        "Matrix_Turkiye_Israel_numeric": [1.5, 1.0, 2.5, 2.5, 2.0],
        
        # Defense systems by supplier
        "Systems_US": [
            "Patriot Air Defense; F-16 Fighter Jets",
            "Patriot Air Defense",
            "None",
            "Patriot Air Defense; Stinger MANPADS",
            "F-16 Fighter Jets; Patriot Air Defense; HIMARS"
        ],
        "Systems_Russia": [
            "S-300 Air Defense; Mi-24 Helicopters; T-90 Tanks",
            "S-300 Air Defense; Mi-24 Helicopters",
            "S-300 Air Defense; Mi-24 Helicopters; T-72 Tanks",
            "S-300 Air Defense; Mi-24 Helicopters",
            "S-300 Air Defense; Mi-24 Helicopters"
        ],
        "Systems_China": [
            "FD-2000 Air Defense; CH-4 UAVs",
            "FD-2000 Air Defense; CH-4 UAVs",
            "CH-4 UAVs",
            "None",
            "None"
        ],
        "Systems_Turkiye_Israel": [
            "None",
            "None",
            "Bayraktar TB2 UAVs; Akinci UAVs",
            "Bayraktar TB2 UAVs; Harop Loitering Munitions; David's Sling",
            "Bayraktar TB2 UAVs; Spike Missiles"
        ],
        
        # Distance metrics (in degrees from regional center)
        "Distance_Europe": [3500, 3200, 3800, 2800, 2200],
        "Distance_China": [2000, 1800, 1500, 2200, 2500],
        "Distance_Russia": [1200, 1500, 1800, 1000, 800],
        "Distance_Near": [1500, 1200, 1000, 800, 600],
    }
    
    return pd.DataFrame(data)


def filter_data(df, **kwargs):
    """Filter data based on provided kwargs."""
    # This is a placeholder - in a real app, this would filter based on various criteria
    return df


# Mock FILTER_CALLBACK_INPUTS for compatibility
FILTER_CALLBACK_INPUTS = {}


# Mock logger for compatibility
class MockLogger:
    def debug(self, msg, *args):
        if args:
            print(f"[DEBUG] {msg % args}")
        else:
            print(f"[DEBUG] {msg}")
    
    def info(self, msg, *args):
        if args:
            print(f"[INFO] {msg % args}")
        else:
            print(f"[INFO] {msg}")
    
    def warning(self, msg, *args):
        if args:
            print(f"[WARN] {msg % args}")
        else:
            print(f"[WARN] {msg}")
    
    def error(self, msg, *args):
        if args:
            print(f"[ERROR] {msg % args}")
        else:
            print(f"[ERROR] {msg}")


logger = MockLogger()

