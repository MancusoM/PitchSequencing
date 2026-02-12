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
from const import pitch_types_list, pitch_types, zones_list

from helper_functions.helpers import (
    run_main_functions,
    calculate_team_sequencing,
    calculate_league_sequencing,
    read_df,
)

# Create Website Emoji
st.set_page_config(page_icon="⚾️️", layout="wide", page_title="Pitch Pairs",initial_sidebar_state ='collapsed')

# Create Border and configures webpage layout
with st.container(border=True):
    # Create Headers
    st.subheader("Pitch Pairs ⚾️")
    header_col1, header_col2 =st.columns(2)
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

        # Adds Platoon Filter
        platoon = st.selectbox(
            "Platoon",
            ["None", "LHB", "RHB"],
            key="platoon",
            help="Click to Select Pitch Sequences thrown to a left-handed or right-handed batter [Optional]. Default: None",
            label_visibility="visible",
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


    def set_up_list(table, column, pitch):
        if isinstance(table,pl.DataFrame):
            pitch_list = list(set(table[column]))
        else:
            pitch_list = table
        pitch_list.insert(0, "None")
        pitch_list = list(set(pitch_list))
        default_pitch = pitch_list.index("None")

        return st.selectbox(
            f"{pitch} Filter",
            pitch_list,
            index=default_pitch
        )

    def return_filtered_dataframes(dataframe, pitch_one_list,pitch_two_list,target_col1, target_col2):
        st.write(pitch_one_list)
        if pitch_one_list =="None":
            if pitch_two_list =="None":
                return dataframe
            else:
                return dataframe.filter(pl.col(target_col2) == pitch_two_list)
        else:
            if pitch_two_list =="None":
                return dataframe.filter(pl.col(target_col1) == pitch_one_list)
            else:
                return dataframe.filter(pl.col(target_col1) == pitch_one_list, pl.col(target_col2) == pitch_two_list)


    def return_filtered_zone_dataframes(dataframe, zone_1, zone_2,target_col_zone_1,target_col_zone_2):
        if zone_1 == "None":
            if zone_2 == "None":
                return dataframe
            else:
                return dataframe.filter(pl.col(target_col_zone_2) == zone_2, pl.col(target_col_zone_1) == zone_1)
        else:
            if zone_2 !="None":
                return dataframe.filter(pl.col(target_col_zone_2) == zone_2)
            else:
                return dataframe.filter(pl.col(target_col_zone_1) == zone_1)

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

        st.write(f"{pitcher}'s 20 Most Frequent Pitch Sequences")

        if Return_Filters == "Pitch Pairs":

            table, sequence = run_main_functions(
                pitcher, players, "pitch_type", selected_range, platoon
            )
            with st.sidebar:
                pitch_one_list = set_up_list(table, "Pitch 1", "1")
                pitch_two_list = set_up_list(table, "Pitch 2", "2")

            filtered = return_filtered_dataframes(table,pitch_one_list,pitch_two_list,"Pitch 1","Pitch 2")
            st.dataframe(filtered[["Pitch 1", "Pitch 2", "Amount", "%"]], hide_index=True)

        if Return_Filters == "Pitch Pairs With Location":
            table, sequence = run_main_functions(
                pitcher, players, "pitch_zone_combo", selected_range, platoon
            )
            table = table.with_columns(
                pl.col("Pitch 1").str.split_exact(by =";",n =2).alias("temp_struct"),
            ).unnest("temp_struct").rename({"field_0": "Pitch 1 Pitch", "field_1": "Pitch 1 Zone"}).drop("field_2")
            table = table.with_columns(
                pl.col("Pitch 2").str.split_exact(by=";", n=2).alias("temp_struct_1")
            ).unnest("temp_struct_1").rename({"field_0": "Pitch 2 Pitch", "field_1": "Pitch 2 Zone"}).drop("field_2")

            with st.sidebar:
                pitch_one_list = set_up_list(table, "Pitch 1 Pitch", "1")
                pitch_one_zone_list = set_up_list(table, "Pitch 1 Zone", "1 Zone")
                pitch_two_list = set_up_list(table, "Pitch 2 Pitch", "2")
                pitch_two_zone_list = set_up_list(table, "Pitch 2 Zone", "2 Zone")

            filtered = return_filtered_dataframes(table, pitch_one_list, pitch_two_list, "Pitch 1 Pitch","Pitch 2 Pitch")
            filtered_zones = return_filtered_zone_dataframes(filtered, pitch_one_zone_list, pitch_two_zone_list, "Pitch 1 Pitch","Pitch 2 Pitch")

            st.dataframe(filtered_zones[["Pitch 1", "Pitch 2", "Amount", "%"]], hide_index=True)

        # st.write(pitch_filter)
        #return df.lazy().filter(filter).sort("Amount", descending=True).head(200).collect()

    # Controls Team Filter Page
    if Filter == "Team":

        def return_zone_filter(zone_one_list, zone_two_list):
            if pitch_one_list == "None":
                return pl.col("Pitch Zone 2") == zone_two_list
            else:
                return pl.col("Pitch Zone 1") == zone_one_list


        def test_function(filter, zone_one_list, zone_two_list):
            if zone_one_list == "None" and zone_two_list == "None":
                st.write('here')
                return filter

            elif zone_one_list != "None" and zone_two_list != "None":
                return filter & (pl.col("Pitch 1 Zone") == zone_one_list) & (pl.col("Pitch 2 Zone") == zone_two_list)
            elif pitch_one_list or pitch_two_list != "None":
                return filter & return_zone_filter(zone_one_list, zone_two_list)

        team_df = read_df(data_directory / "data/teams.csv")  # type:ignore
        teams = list(set(team_df["Team"]))
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
                pitch_one_list = set_up_list(pitch_types_list, "N/A", "1")
                pitch_two_list =  set_up_list(pitch_types_list, "N/A", "2")

            st.write(pitch_one_list,pitch_two_list)
            table = calculate_team_sequencing(team_df, team, "pitch_type", pitch_one_list,pitch_two_list)
            st.write(table)

            filtered_table = return_filtered_dataframes(table, pitch_one_list, pitch_two_list,"Pitch 1", "Pitch 2")
            st.write(filtered_table)
            lazy_table = filtered_table.lazy().sort("Amount", descending=True).head(200).collect()
            #lazy_frame = table.lazy().sort("Amount", descending=True).head(200).collect()
            st.dataframe(lazy_table[["Name", "Pitch 1", "Pitch 2", "Amount", "%"]])

        if Return_Filters == "Pitch Pairs With Location":

            with st.sidebar:
                pitch_one_list = set_up_list(pitch_types_list, "N/A", "Pitch 1")
                pitch_two_list = set_up_list(pitch_types_list, "", "Pitch 2")
                pitch_one_zone_list = set_up_list(zones_list, "NA", "Zone 1")
                pitch_two_zone_list = set_up_list(zones_list, "NAe", "Zone 2")

            table = calculate_team_sequencing(team_df, team, "pitch_zone_combo", pitch_one_list,pitch_two_list)
            table = table.with_columns(
                pl.col("Pitch 1").str.split_exact(by=";", n=2).alias("temp_struct"),
            ).unnest("temp_struct").rename({"field_0": "Pitch 1 Pitch", "field_1": "Pitch 1 Zone"}).drop("field_2")
            table = table.with_columns(
                pl.col("Pitch 2").str.split_exact(by=";", n=2).alias("temp_struct_1")
            ).unnest("temp_struct_1").rename({"field_0": "Pitch 2 Pitch", "field_1": "Pitch 2 Zone"}).drop("field_2")
            st.dataframe(table)

            #1 refactor this to make it quicker and remove erranous code
            #2. add type hints throughout
            #3 fix the zones (there is a space in front of every one :))
            #4 can i change aggregation to pre-csv export
            filtered_table = return_filtered_dataframes(table, pitch_one_list, pitch_two_list, "Pitch 1 Pitch", "Pitch 2 Pitch")
            st.dataframe(filtered_table)
            filtered_zone_table = return_filtered_dataframes(filtered_table, pitch_one_zone_list, pitch_two_zone_list, "Pitch 1 Zone", "Pitch 2 Zone")

            lazy_zones = filtered_zone_table.lazy().sort("Amount", descending=True).head(100).collect()
            st.dataframe(lazy_zones[["Name", "Pitch 1", "Pitch 2","Amount", "%"]])

            '''

            filtered = return_filtered_dataframes(table, pitch_one_list, pitch_two_list,"Pitch 1 Pitch", "Pitch 2 Pitch")
            st.write(filtered)
            st.write(table)

            filtered_zones = return_filtered_dataframes(filtered, pitch_one_zone_list, pitch_two_zone_list,"Pitch 1 Zone", "Pitch 2 Zone")
            lazy_frame = table.lazy().filter(filtered_zones).sort("Amount", descending=True).head(200).collect()


            #st.write(f'Filtered  = {filtered_zones}')

            #lazy_frame = filtered_zones.lazy().filter(filtered_zones).sort("Amount", descending=True).head(200).collect()

            st.dataframe(lazy_frame[["Name", "Pitch 1", "Pitch 2", "Amount", "%"]])

            #st.write(pitch_one_list,pitch_two_list,pitch_one_zone_list,pitch_two_zone_list)
            #st.dataframe(filtered_zones[["Name", "Pitch 1", "Pitch 2", "Amount", "%"]])
            
            '''
    '''
    # Controls League Filter
    if Filter == "League":
        team_df = read_df(data_directory / "data/teams.csv")  # type:ignore

        if Return_Filters == "Pitch Pairs":
            calculate_league_sequencing(team_df, "pitch_type")

        if Return_Filters == "Pitch Pairs With Location":
            calculate_league_sequencing(team_df, "pitch_zone_combo")
    '''
    # Adds Expander
    with st.expander("Click For More Information"):
        (
            st.write(
                "Location is measured using Baseball Savant's predefined Gameday Zones. \n\n Pitch Pairs are reset upon a new batter, inning, or out status \n\n Data is retrieved in real-time using the Baseball Savant functionality in PyBaseball \n\n With questions,concerns, or comments, please contact Matt Mancuso at mancusom33@gmail.com"
            )
        )
