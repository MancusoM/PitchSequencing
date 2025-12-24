import streamlit as st
from datetime import date

from pathlib import Path
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

current_script_path = Path(__file__).resolve()
parent_directory = current_script_path.parent
data_directory = current_script_path.parent.parent

from helper_functions.helpers import (
    run_main_functions,
    calculate_team_sequencing,
    calculate_league_sequencing,
    read_df,
)

# Create Website Emoji
st.set_page_config(page_icon="⚾️️", layout="wide", page_title="Pitch Pairs")

# Create Border and configures webpage layout
with st.container(border=True):
    head_col1, head_col2 = st.columns(2)
    # Create Headers
    with head_col1:
        st.subheader("Pitch Pairs")
        st.write(
            "**Paired Pitches** provides an insight into a pitcher's arsenal by exploring the frequencies of sequences & by providing a window into their intent to tunnel pitches. "
        )
        st.text("")
        st.write(
            "This website visualizes the most frequent **Paired Pitches** from the 2025 MLB Season. \n Location is optionally included in the return to serve as an insight into pitch tunnelling. Location Zones are located on the right"
        )
    with head_col2:
        st.image(parent_directory / "zones.png", width=220)

    st.write("-----")

    # Adds Filters to Sidebar
    with st.sidebar:
        st.sidebar.header("Filters")

        # Adds Team/Player/League Filter
        Filter = st.selectbox(
            "Filters",
            ["Players", "Team", "League"],
            key="Grouping",
            help="Click to Filter Sequencing on at a Player,Team, or League level",
            label_visibility="visible",
        )

        # Creates Unique Players list
        players = read_df(data_directory / "data/players.csv")  # type:ignore
        players_list = set(players["Name"].to_list())

        # Sets Data Range
        selected_range = st.date_input(
            "Select a date range",
            value=(date(2025, 3, 27), date(2025, 10, 2)),  # Default range
            min_value=date(2025, 3, 26),
            max_value=date(2025, 10, 3),
            key="date",
        )

        # Adds Platoon Filter
        platoon = st.selectbox(
            "Platoon",
            ["None", "LHB", "RHB"],
            key="platoon",
            help="Click to Select Pitch Sequences thrown to a LHB or RHB [Optional]",
            label_visibility="visible",
        )

    # Adds Sequencing Filter
    Return_Filters = st.selectbox(
        "Filters",
        [
            "Pitch Pairs",
            "Pitch Pairs With Location",
            "Pitch Grouping Pairs",
            "Pitch Grouping Pairs With Location",
        ],
        key="Display Preference",
        help="Flip Through to Select Different Pitch Sequences",
        label_visibility="visible",
    )

    # Controls the Player Page
    if Filter == "Players":
        with st.sidebar:
            default_player = list(players_list).index("Clay Holmes")
            pitcher = st.selectbox(
                "Choose pitcher",
                players_list,
                index=default_player,
                help="Select Pitcher",
                label_visibility="visible",
            )

        st.write(f"{pitcher}'s 20 Most Frequent Pitch Sequences")

        if Return_Filters == "Pitch Pairs":
            table, sequence = run_main_functions(
                pitcher, players, "pitch_type", selected_range, platoon
            )

        if Return_Filters == "Pitch Pairs With Location":
            table, sequence = run_main_functions(
                pitcher, players, "pitch_zone_combo", selected_range, platoon
            )
        if Return_Filters == "Pitch Grouping Pairs":
            table, sequence = run_main_functions(
                pitcher, players, "pitch_group", selected_range, platoon
            )

        if Return_Filters == "Pitch Grouping Pairs With Location":
            table, sequence = run_main_functions(
                pitcher, players, "pitch_group_combo", selected_range, platoon
            )

    # Controls Team Filter Page
    if Filter == "Team":
        team_df = read_df(data_directory / "data/teams.csv")  # type:ignore
        teams = list(set(team_df["Team"]))
        teams.append("All")

        # Adds Functionality to Return all Teams Data
        with st.sidebar:
            default_index = teams.index("All")
            team = st.selectbox("Choose team", teams, index=default_index)
        st.write(
            "Select a Team on the Drop-Down on the left side. Returning the top 150 sequences"
        )

        if Return_Filters == "Pitch Pairs":
            table = calculate_team_sequencing(team_df, team, "pitch_type")

        if Return_Filters == "Pitch Pairs With Location":
            table = calculate_team_sequencing(team_df, team, "pitch_zone_combo")

        if Return_Filters == "Pitch Grouping Pairs":
            table = calculate_team_sequencing(team_df, team, "pitch_group")

        if Return_Filters == "Pitch Grouping Pairs With Location":
            table = calculate_team_sequencing(team_df, team, "pitch_group_combo")

    # Controls League Filter
    if Filter == "League":
        team_df = read_df(data_directory / "data/teams.csv")  # type:ignore

        if Return_Filters == "Pitch Pairs":
            calculate_league_sequencing(team_df, "pitch_type")

        if Return_Filters == "Pitch Pairs With Location":
            calculate_league_sequencing(team_df, "pitch_zone_combo")

        if Return_Filters == "Pitch Grouping Pairs":
            calculate_league_sequencing(team_df, "pitch_group")

        if Return_Filters == "Pitch Grouping Pairs With Location":
            calculate_league_sequencing(team_df, "pitch_group_combo")

    # Adds Expander
    with st.expander("Click For More Information"):
        (
            st.write(
                "Location is measured using Baseball Savant's predefined Gameday Zones. \n\n Pitch Pairs are reset upon a new batter, inning, or out status \n\n Data is retrieved in real-time using the Baseball Savant functionality in PyBaseball \n\n With questions,concerns, or comments, please contact Matt Mancuso at mancusom33@gmail.com"
            )
        )
