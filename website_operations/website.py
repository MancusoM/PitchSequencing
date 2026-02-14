import streamlit as st
from datetime import date

from pathlib import Path
import sys
import os
import polars as pl

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

current_script_path = Path(__file__).resolve()
parent_directory = current_script_path.parent
data_directory = current_script_path.parent.parent
from const import pitch_types_list, zones_list, pitches

from helper_functions.helpers import (
    run_main_functions,
    calculate_team_sequencing,
    return_filtered_dataframes,
    read_df,
    set_up_footer,
    set_up_list,
)

# Create Website Emoji
st.set_page_config(
    page_icon="⚾️️",
    layout="wide",
    page_title="Pitch Pairs",
    initial_sidebar_state="collapsed",
)

# Create Border and configures webpage layout
with st.container(border=True):
    # Create Headers
    st.subheader("Pitch Pairs ⚾️")
    header_col1, header_col2 = st.columns(2)
    with header_col1:
        st.write(
            "**Pitch Pairs** explores the frequencies of pitch sequences from 2025.\n\nLocation is optionally included. Location Zones are located on the left."
        )
        st.write("**Please wait up to 10 seconds for sequencing data to populate**")

    st.write("-----")

    # Adds Filters to Sidebar
    with st.sidebar:
        st.image(data_directory / "images/zones_2.png", width=250)
        # Adds Team/Player/League Filter
        Filter = st.selectbox(
            "Filters",
            ["Players", "Team", "League"],
            key="Grouping",
            help="Click to Filter Sequencing at a Player, Team, or League level",
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

    # Adds Sequencing Filter
    Return_Filters = st.selectbox(
        "Filters",
        [
            "Pitch Pairs",
            "Pitch Pairs With Location",
        ],
        key="Display Preference",
        help="Flip Through to Select Different Pitch Sequences",
        label_visibility="visible",
    )
    # Controls the Player Page
    if Filter == "Players":
        with st.sidebar:
            default_player = list(players_list).index("Freddy Peralta")
            pitcher = st.selectbox(
                "Choose pitcher",
                players_list,
                index=default_player,
                help="Select Pitcher",
                label_visibility="visible",
            )
            platoon = st.selectbox(
                "Platoon",
                ["None", "LHB", "RHB"],
                key="platoon",
                help="Click to Select Pitch Sequences thrown to a left-handed or right-handed batter [Optional]. Default: None",
                label_visibility="visible",
            )

        st.write(f"{pitcher}'s 20 Most Frequent Pitch Sequences")

        if Return_Filters == "Pitch Pairs":
            table, sequence, mlbID = run_main_functions(
                pitcher, players, "pitch_type", selected_range, platoon
            )
            with st.sidebar:
                pitch_one_list = set_up_list(table, pitches[0], pitches[0])
                pitch_two_list = set_up_list(table, pitches[1], pitches[1])

            filtered = return_filtered_dataframes(
                table, pitch_one_list, pitch_two_list, pitches[0], pitches[1]
            )
            st.dataframe(
                filtered[[pitches[0], pitches[1], "Amount", "%"]], hide_index=True
            )

            set_up_footer(table, sequence, mlbID)

        if Return_Filters == "Pitch Pairs With Location":
            table, sequence, mlbID = run_main_functions(
                pitcher, players, "pitch_zone_combo", selected_range, platoon
            )
            table = (
                table.with_columns(
                    pl.col(pitches[0])
                    .str.split_exact(by=";", n=2)
                    .alias("temp_struct"),
                )
                .unnest("temp_struct")
                .rename(
                    {"field_0": f"{pitches[0]} Pitch", "field_1": f"{pitches[0]} Zone"}
                )
                .drop("field_2")
            )
            table = (
                table.with_columns(
                    pl.col(pitches[1])
                    .str.split_exact(by=";", n=2)
                    .alias("temp_struct_1")
                )
                .unnest("temp_struct_1")
                .rename(
                    {"field_0": f"{pitches[1]} Pitch", "field_1": f"{pitches[1]} Zone"}
                )
                .drop("field_2")
            )
            with st.sidebar:
                pitch_one_list = set_up_list(table, f"{pitches[0]} Pitch", "Pitch 1")
                pitch_one_zone_list = set_up_list(
                    table, f"{pitches[0]} Zone", "Pitch 1 Zone"
                )
                pitch_two_list = set_up_list(table, f"{pitches[1]} Pitch", "Pitch 2")
                pitch_two_zone_list = set_up_list(
                    table, f"{pitches[1]} Zone", "Pitch 2 Zone"
                )

            filtered = return_filtered_dataframes(
                table,
                pitch_one_list,
                pitch_two_list,
                f"{pitches[0]} Pitch",
                f"{pitches[1]} Pitch",
            )
            filtered_zones = return_filtered_dataframes(
                filtered,
                pitch_one_zone_list,
                pitch_two_zone_list,
                f"{pitches[0]} Pitch",
                f"{pitches[1]} Pitch",
            )

            st.dataframe(
                filtered_zones[[pitches[0], pitches[1], "Amount", "%"]], hide_index=True
            )

            set_up_footer(table, sequence, mlbID)

    # Controls Team Filter Page
    if Filter == "Team":
        team_df = read_df(data_directory / "data/teams.csv")  # type:ignore
        teams = sorted(list(set(team_df["Team"])))
        teams.remove("NYM")
        teams.insert(0, "All")
        teams.insert(1, "NYM")

        # Adds Functionality to return data from teams.csv
        with st.sidebar:
            default_index = teams.index("All")
            team = st.selectbox("Choose team", teams, index=default_index)

        st.write(
            "Select a Team on the Drop-Down on the left side. Returning the top 200 sequences"
        )

        if Return_Filters == "Pitch Pairs":
            with st.sidebar:
                pitch_one_list = set_up_list(pitch_types_list, "N/A", f"{pitches[0]}")
                pitch_two_list = set_up_list(pitch_types_list, "N/A", f"{pitches[1]}")

            table = calculate_team_sequencing(team_df, team, "pitch_type")

            filtered_table = return_filtered_dataframes(
                table, pitch_one_list, pitch_two_list, f"{pitches[0]}", f"{pitches[1]}"
            )
            lazy_table = (
                filtered_table.lazy()
                .sort("Amount", descending=True)
                .head(200)
                .collect()
            )
            st.dataframe(lazy_table[["Name", pitches[0], pitches[1], "Amount", "%"]])

        if Return_Filters == "Pitch Pairs With Location":
            with st.sidebar:
                pitch_one_list = set_up_list(pitch_types_list, "", pitches[0])
                pitch_two_list = set_up_list(pitch_types_list, "", pitches[1])
                pitch_one_zone_list = set_up_list(zones_list, "", "Zone 1")
                pitch_two_zone_list = set_up_list(zones_list, "", "Zone 2")

            table = calculate_team_sequencing(team_df, team, "pitch_zone_combo")
            table = (
                table.with_columns(
                    pl.col(pitches[0])
                    .str.split_exact(by=";", n=2)
                    .alias("temp_struct"),
                )
                .unnest("temp_struct")
                .rename(
                    {"field_0": f"{pitches[0]} Pitch", "field_1": f"{pitches[0]} Zone"}
                )
                .drop("field_2")
            )
            table = (
                table.with_columns(
                    pl.col(pitches[1])
                    .str.split_exact(by=";", n=2)
                    .alias("temp_struct_1")
                )
                .unnest("temp_struct_1")
                .rename(
                    {"field_0": f"{pitches[1]} Pitch", "field_1": f"{pitches[1]} Zone"}
                )
                .drop("field_2")
            )

            filtered_table = return_filtered_dataframes(
                table,
                pitch_one_list,
                pitch_two_list,
                f"{pitches[0]} Pitch",
                f"{pitches[1]} Pitch",
            )
            filtered_zone_table = return_filtered_dataframes(
                filtered_table,
                pitch_one_zone_list,
                pitch_two_zone_list,
                f"{pitches[0]} Zone",
                f"{pitches[1]} Zone",
            )

            lazy_zones = (
                filtered_zone_table.lazy()
                .sort("Amount", descending=True)
                .head(200)
                .collect()
            )
            st.dataframe(
                lazy_zones[["Name", f"{pitches[0]}", f"{pitches[1]}", "Amount", "%"]]
            )

    # Adds Expander
    with st.expander("Click For More Information"):
        (
            st.write(
                "Location is measured using Baseball Savant's predefined Gameday Zones. \n\n Pitch Pairs are reset upon a new batter, inning, or out status \n\n Data is retrieved in real-time using the Baseball Savant functionality in PyBaseball \n\n With questions,concerns, or comments, please contact Matt Mancuso at mancusom33@gmail.com"
            )
        )
