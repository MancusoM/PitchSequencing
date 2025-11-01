# ======================================================
# Import Required Libraries
# ======================================================

import streamlit as st
import pandas as pd
from website_funcs import main, create_csv_button
from datetime import date
import polars as pl

# Create Header
st.set_page_config(page_icon="⚾️️", layout="wide", page_title="Pitch Sequencing")

with st.container(border=True):
    head_col1, headcol2 = st.columns(2)
    with head_col1:
        st.title("Pitch Sequencing ")
        st.write(
            "This dashboard aggregates pitch pairs from the 2023, 2024, and 2025 MLB Seasons and returns the frequency of each pitch sequence. User can choose to display their sequencing preference to include location. \n Location is optinally included in the return to serve as an insight into pitch tunnelling."
        )
        st.text("")
        st.write(
            "Pitch pairs provides insight into a player's pitch movement and pitch tunneling. If two pitches are frequent paired together, but land in opposing zones, it could give an indication that pitches follow the same path and diverge after they reach the batter's decision point"
        )
        st.text("")
        st.write(
            "Example: In 2025, Edwin Diaz's most frequent Paired Pitches were a Slider in Zone 14 & a Slider in Zone 14. Scroll down to see more examples"
        )
    with headcol2:
        st.image("zones.png", width=325)

    @st.cache_data
    def read_df(df):
        return pl.read_csv(df)

    st.write("-----")

    with st.sidebar:
        st.sidebar.header("Filters")

        Filter = st.selectbox("Filters", ["Players", "Team", "League"], key="Grouping")

        players = read_df("players.csv")
        players_list = players["Name"].to_list()

        pitcher = st.selectbox("Choose pitcher", players_list)

        selected_range = st.date_input(
            "Select a date range",
            value=(date(2025, 4, 1), date(2025, 10, 2)),  # Default range
            min_value=date(2023, 4, 1),
            max_value=date(2025, 10, 2),
            key="date",
        )

        platoon = st.selectbox("Batter Faced", ["None", "LHB", "RHB"], key="platoon")

    if Filter == "Players":
        Return_Filters = st.selectbox(
            "Filters",
            [
                "Pitch Pairs",
                "Pitch Pairs With Location",
                "Pitch Grouping Pairs",
                "Pitch Grouping Pairs With Location",
            ],
            key="Display Preference",
        )

        st.write("Most Frequent Pitch Sequences")

        if Return_Filters == "Pitch Pairs":

            table, sequence = main(
                pitcher, players, "pitch_type", selected_range, platoon
            )
            st.table(table)
            (
                create_csv_button(sequence, "Sequence Data"),
                create_csv_button(table, "Frequency Data"),
            )

        if Return_Filters == "Pitch Pairs With Location":

            table, sequence = main(
                pitcher, players, "pitch_zone_combo", selected_range, platoon
            )
            st.table(table)
            (
                create_csv_button(sequence, "Sequence Data"),
                create_csv_button(table, "Frequency Data"),
            )
        if Return_Filters == "Pitch Grouping Pairs":
            table, sequence = main(
                pitcher, players, "pitch_group", selected_range, platoon
            )
            st.table(table)
            (
                create_csv_button(sequence, "Sequence Data"),
                create_csv_button(table, "Frequency Data"),
            )
        if Return_Filters == "Pitch Grouping Pairs With Location":
            table, sequence = main(
                pitcher, players, "pitch_group_combo", selected_range, platoon
            )
            st.table(table)
            (
                create_csv_button(sequence, "Sequence Data"),
                create_csv_button(table, "Frequency Data"),
            )

    with st.expander("Click For More Information"):
        (
            st.write(
                "Location is measured using Baseball Savant's predefined Gameday Zones. \n Pitch Pairs are reset upon a new batter, inning, or out status"
            )
        )
    '''
    """
    #Create Tabs
    Player_Sequence, Team_Sequence, League_Trends = st.tabs(
        ["Player Sequencing", "Team Sequencing", "League Trends"]
    )
    
    #Read Player CSV
    players = pd.read_csv("players.csv")
    
    # Format Player Sequence Page
    with Player_Sequence:
        players_list = players["Name"].to_list()
        pitcher = st.selectbox("Choose pitcher", players_list)
    
        selected_range = st.date_input(
            "Select a date range",
            value=(date(2025, 4, 1), date(2025, 10, 2)),  # Default range
            min_value=date(2015, 4, 1),
            max_value=date(2025, 10, 2),
            key=uuid4()
        )
    
        platoon = st.selectbox("Batter Faced", ["None","LHB","RHB"],key = uuid4())
    
        pitch, pitch_zone,pitch_group,pitch_group_zone = st.tabs(
            ["Pitches", "Pitches + Zone","Pitch Group","Pitch Group + Zone"]
        )
    
    
    
        #Turn into function
        with pitch:
            table,sequence = main(pitcher,players,"pitch_type",selected_range,platoon)
            st.table(table)
            create_csv_button(sequence,"Sequence Data"), create_csv_button(table, "Frequency Data")
        with pitch_zone:
            table,sequence = main(pitcher, players, "pitch_zone_combo",selected_range,platoon)
            st.table(table)
            create_csv_button(sequence,"Sequence Data"), create_csv_button(table, "Frequency Data")
        with pitch_group:
            table, sequence = main(pitcher, players, "pitch_group", selected_range, platoon)
            st.table(table)
            create_csv_button(sequence, "Sequence Data"), create_csv_button(table, "Frequency Data"),
            #
        with pitch_group_zone:
            table, sequence = main(pitcher, players, "pitch_group_combo", selected_range, platoon)
            st.table(table)
            create_csv_button(sequence, "Sequence Data"), create_csv_button(table, "Frequency Data")
    '''
    """
    with Team_Sequence:
    
        team_list = players["Team"].to_list()
        team = st.selectbox("Choose Team", team_list)
    
        selected_range = st.date_input(
            "Select a date range",
            value=(date(2025, 4, 1), date(2025, 10, 2)),  # Default range
            min_value=date(2015, 4, 1),
            max_value=date(2025, 10, 2),
            key = uuid4()
        )
    
        platoon = st.selectbox("Batter Faced", ["None", "LHB", "RHB"],key = uuid4())
    
        team_pitch, team_pitch_zone, team_pitch_group, team_pitch_group_zone = st.tabs(
            ["Pitches", "Pitches + Zone", "Pitch Group", "Pitch Group + Zone"]
        )
        #team_df = pd.read_csv("players.csv")['Team']
        team_results2 = players[players['Team'] == "NYM"]
    
        team_results = pd.DataFrame()
    
        with team_pitch:
    
            for pitcher in team_results2['Name']:
                table,sequence = main(pitcher,players,"pitch_type",selected_range,platoon)
                print(f'Processed {pitcher}')
                time.sleep(30)
                team_results =pd.concat([table,team_results])
                st.table(team_results)
            create_csv_button(sequence,"Sequence Data"), create_csv_button(table, "Frequency Data")
        with team_pitch_zone:
            table,sequence = main(pitcher, players, "pitch_zone_combo",selected_range,platoon)
            st.table(table)
            create_csv_button(sequence,"Sequence Data"), create_csv_button(table, "Frequency Data")
        with team_pitch_group:
            table, sequence = main(pitcher, players, "pitch_group", selected_range, platoon)
            st.table(table)
            create_csv_button(sequence, "Sequence Data"), create_csv_button(table, "Frequency Data"),
            #
        with team_pitch_group_zone:
            table, sequence = main(pitcher, players, "pitch_group_combo", selected_range, platoon)
            st.table(table)
            create_csv_button(sequence, "Sequence Data"), create_csv_button(table, "Frequency Data")
    """
