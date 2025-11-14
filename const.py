import polars as pl
import streamlit as st

def read_df(df):
    return pl.read_csv(df)


pitch_types = {
    "EP":"Eeuphus",
    "SI":"Sinker",
    "FC":"Cutter",
    "CU": "Curveball",
    "FF": "Fastball",
    "FT":"Two-Seam Fastball",
    "SL":"Slider",
    "CH":"Changeup",
    "FS":"Splitter",
    "FO":"Forkball",
    "ST":"Sweeper",
    "SC":"Screwball",
    "KC":"Knuckle Curve"
}

pitch_groups = {
    "Eeuphus":"Other",
    "Knuckle Curve": "Breaking",
    "Sinker":"Fastball",
    "Cutter":"Fastball",
    "Curveball": "Breaking",
    "Fastball":"Fastball",
    "Slider":"Breaking",
    "Changeup":"Offspeed",
    "Splitter":"Offspeed",
    "Forkball":"Offspeed",
    "Sweeper":"Offspeed"
}

teams_dict = {
    "Angels": "LAA",
    "Astros": "HOU",
    "Athletics": "OAK",
    "Blue Jays": "TOR",
    "Braves": "ATL",
    "Brewers": "MIL",
    "Cardinals": "STL",
    "Cubs": "CHC",
    "Rays": "TB",
    "Diamondbacks": "AZ",
    "Dodgers": "LAD",
    "Giants": "SF",
    "Guardians": "CLE",
    "Mariners": "SEA",
    "Marlins": "MIA",
    "Mets": "NYM",
    "Nationals": "WSN",
    "Orioles": "BAL",
    "Padres": "SDP",
    "Phillies": "PHI",
    "Pirates": "PIT",
    "Rangers": "TEX",
    "Red Sox": "BOS",
    "Reds": "CIN",
    "Rockies": "COL",
    "Royals": "KC",
    "Tigers": "DET",
    "Twins": "MIN",
    "White Sox": "CHW",
    "Yankees": "NYY",
}

team_list = [value for key, value in teams_dict.items()]

mlb_2025_dates = {
    "LAD": ["2025-03-18", "2025-09-28"],  # Los Angeles Dodgers (opened in Tokyo) :contentReference[oaicite:0]{index=0}
    "CHC": ["2025-03-18", "2025-09-28"],  # Chicago Cubs (opened in Tokyo) :contentReference[oaicite:1]{index=1}
    "TB": ["2025-03-28", "2025-09-28"],  # Tampa Bay Rays (delayed to March 28) :contentReference[oaicite:2]{index=2}
    "COL": ["2025-03-28", "2025-09-28"],  # Colorado Rockies (also delayed) :contentReference[oaicite:3]{index=3}
    # All other teams: opened on March 27
    "LAA": ["2025-03-27", "2025-09-28"],  # Los Angeles Angels :contentReference[oaicite:4]{index=4}
    "HOU": ["2025-03-27", "2025-09-28"],  # Houston Astros :contentReference[oaicite:5]{index=5}
    "OAK": ["2025-03-27", "2025-09-28"],  # Athletics :contentReference[oaicite:6]{index=6}
    "TOR": ["2025-03-27", "2025-09-28"],  # Toronto Blue Jays :contentReference[oaicite:7]{index=7}
    "ATL": ["2025-03-27", "2025-09-28"],  # Atlanta Braves :contentReference[oaicite:8]{index=8}
    "MIL": ["2025-03-27", "2025-09-28"],  # Milwaukee Brewers :contentReference[oaicite:9]{index=9}
    "STL": ["2025-03-27", "2025-09-28"],  # St. Louis Cardinals :contentReference[oaicite:10]{index=10}
    "AZ": ["2025-03-27", "2025-09-28"],  # Arizona Diamondbacks :contentReference[oaicite:11]{index=11}
    "SEA": ["2025-03-27", "2025-09-28"],  # Seattle Mariners :contentReference[oaicite:12]{index=12}
    "SDP": ["2025-03-27", "2025-09-28"],  # San Diego Padres :contentReference[oaicite:13]{index=13}
    "SF": ["2025-03-27", "2025-09-28"],  # San Francisco Giants :contentReference[oaicite:14]{index=14}
    "DET": ["2025-03-27", "2025-09-28"],  # Detroit Tigers :contentReference[oaicite:15]{index=15}
    "KC": ["2025-03-27", "2025-09-28"],   # Kansas City Royals :contentReference[oaicite:16]{index=16}
    "MIN": ["2025-03-27", "2025-09-28"], # Minnesota Twins :contentReference[oaicite:17]{index=17}
    "BOS": ["2025-03-27", "2025-09-28"], # Boston Red Sox :contentReference[oaicite:18]{index=18}
    "NYY": ["2025-03-27", "2025-09-28"], # New York Yankees :contentReference[oaicite:19]{index=19}
    "TEX": ["2025-03-27", "2025-09-28"], # Texas Rangers :contentReference[oaicite:20]{index=20}
    "CLE": ["2025-03-27", "2025-09-28"], # Cleveland Guardians :contentReference[oaicite:21]{index=21}
    "BAL": ["2025-03-27", "2025-09-28"], # Baltimore Orioles :contentReference[oaicite:22]{index=22}
    "PHI": ["2025-03-27", "2025-09-28"], # Philadelphia Phillies :contentReference[oaicite:23]{index=23}
    "NYM": ["2025-03-27", "2025-09-28"], # New York Mets :contentReference[oaicite:24]{index=24}
    "PIT": ["2025-03-27", "2025-09-28"], # Pittsburgh Pirates :contentReference[oaicite:25]{index=25}
    "CIN": ["2025-03-27", "2025-09-28"], # Cincinnati Reds :contentReference[oaicite:26]{index=26}
    "MIA": ["2025-03-27", "2025-09-28"], # Miami Marlins :contentReference[oaicite:27]{index=27}
    "CHW": ["2025-03-27", "2025-09-28"], # Chicago White Sox :contentReference[oaicite:28]{index=28}
}
