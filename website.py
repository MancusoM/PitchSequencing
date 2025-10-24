import streamlit as st

import pandas as pd
from sequence import (
    retrieve_mlb_id,
    call_statcast_pitcher,
    define_additional_cols,
    create_pitch_sequencing,
    get_combinations,
    count_combinations,
)
from datetime import date

st.set_page_config(page_icon="⚾️️", layout="centered", page_title="Pitch Sequencing")

container = st.container()
container.write("test")
with st.sidebar:
    st.image("zones.png",width = 'stretch',caption ='Zones')

Player_Sequence, Team_Sequence, League_Trends = st.tabs(
    ["Player Sequencing", "Team Sequencing", "League Trends"]
)

with Player_Sequence:
    players = pd.read_csv("players.csv")
    players_list = players["Name"].to_list()
    option = st.selectbox("Choose pitcher", players_list)

    def format_name(option):
        return option.split(" ")[::-1]

    # For a date range
    selected_range = st.date_input(
        "Select a date range",
        value=(date(2025, 1, 1), date(2025, 12, 31)),  # Default range
        min_value=date(2022, 1, 1),
        max_value=date(2025, 12, 31),
    )


    mlbID,team = retrieve_mlb_id(option, players)
    player_pitch_data = call_statcast_pitcher(
        selected_range[0], selected_range[1], mlbID
    )
    df = define_additional_cols(player_pitch_data)
    pitch_sequence = create_pitch_sequencing(df)
    st.table(count_combinations(pitch_sequence).head(10))
