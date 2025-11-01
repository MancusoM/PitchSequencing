
pitch_types = {
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
    "SC":"Screwball"
}

pitch_groups = {
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
    "Rays": "TBR",
    "Diamondbacks": "ARI",
    "Dodgers": "LAD",
    "Giants": "SFG",
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
    "Royals": "KCR",
    "Tigers": "DET",
    "Twins": "MIN",
    "White Sox": "CHW",
    "Yankees": "NYY",
}

team_list = [value for key, value in teams_dict.items()]
