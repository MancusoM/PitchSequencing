from website_operations.website_funcs import calculate_sequence
import streamlit as st
import polars as pl
from typing import Any
import pandas as pd


def run_main_functions(
    pitcher: str,
    players: pl.DataFrame,
    sequencing_choice: str,
    selected_range: Any,
    platoon: str,
) -> tuple[Any, Any]:
    """

    Runs Main Sequencing Functions to return table to streamlit dashboard

    :param pitcher: - player Name chosen from Streamlit drop-down. Example: "Skubal, Tarik" etc.
    :param players: players.csv from Fangraphs
    :param sequencing_choice: Choice to filter the dashboard by. Example: Pitch Type, Pitch Type with Location, Pitch Group, Pitch Group with Location
    :param selected_range: Date range of query
    :param platoon: Platoon (optional). Examples: "LHB","RHB", ""

    :return: streamlit table, sequencing dataframe - to be exported as CSVs
    """

    try:
        table, sequence, mlbID = calculate_sequence(
            pitcher, players, sequencing_choice, selected_range, platoon
        )

    except Exception as e:  # type:ignore
        st.write(e)
        return st.error("An Error Has Occurred. \nPlease Refresh The Page. Contact the author if this persists", icon="🚨")

    footer_column1, footer_column2, footer_column3 = st.columns(3)
    with footer_column1:
        create_csv_button(sequence, "Raw Sequencing")
    with footer_column2:
        create_csv_button(table, "Frequency")
    with footer_column3:
        st.link_button(
            "Pitcher Plinko",
            f"https://baseballsavant.mlb.com/visuals/pitch-plinko?playerId={mlbID}",
        )
    return table, sequence


def create_csv_button(df: pl.DataFrame, name: str):
    """

    Creates CSV button for Data Export

    :param df: data to be exported
    :param name: name of dataframe
    :return: N/A
    """
    dataframe = df.to_pandas()

    st.download_button(
        label=f"Download {name} Data",
        data=dataframe.to_csv().encode("utf-8"),
        file_name=f"{name}.csv",
        mime="text/csv",
    )

def return_pitch_filter(pitch_one_list,pitch_two_list):
    st.write(pitch_one_list,pitch_two_list)
    if pitch_one_list =="None":
        return pl.col("Pitch 2") ==pitch_two_list
    else:
        return pl.col("Pitch 1") ==pitch_one_list

#def return_zone_filter(zone_one, zone_two)

def calculate_team_sequencing(
    df: pl.DataFrame, team: str, api_call: str, pitch_one_list, pitch_two_list
) -> pl.DataFrame:
    """

    Extracts top 100 results from teams.csv filtered by user selections

    :param df: Data from teams.csv dataframe
    :param team: team filter. Default is all. Examples: NYM, NYY, etc.
    :param api_call: type of sequencing filter. Example: pitch_type, pitch_type_with_location, pitch_group
    :return: table from streamlit

    """

    #Turn into function
    if team == "All":
        filter = pl.col("Call") == api_call  # type:ignore
    else:
        filter = (pl.col("Team") == team) & (pl.col("Call") == api_call)  # type:ignore
    #return filter
    '''
    if pitch_one_list != "None" and pitch_two_list !="None":
        pitch_filter = (pl.col("Pitch 1") == pitch_one_list) & (pl.col("Pitch 2") == pitch_two_list)
    elif pitch_one_list or pitch_two_list !="None":
        pitch_filter = filter & return_pitch_filter(pitch_one_list,pitch_two_list)

    if pitch_one_list == "None" and pitch_two_list =="None":
        st.write('here')
        pass
    else:
        filter  = filter & pitch_filter
    '''
    #return filter
    '''
    else:
        st.write(df)
        # Turn into function
        if team == "All":
            filter = pl.col("Call") == api_call  # type:ignore
        elif team != "All":
            filter = (pl.col("Team") == team) & (pl.col("Call") == api_call)  # type:ignore
        st.write(filter)

        if pitch_one_list != "None" and pitch_two_list != "None":
            pitch_filter = (pl.col("Pitch 1") == pitch_one_list) & (pl.col("Pitch 2") == pitch_two_list)
        elif pitch_one_list or pitch_two_list != "None":
            pitch_filter = filter & return_pitch_filter(pitch_one_list, pitch_two_list)

        if pitch_one_list == "None" and pitch_two_list == "None":
            st.write('here')
            pass
        else:
            filter = filter & pitch_filter

        if pitch_one_list != "None" and pitch_two_list != "None":
            pitch_filter = (pl.col("Pitch 1") == pitch_one_list) & (pl.col("Pitch 2") == pitch_two_list)
        elif pitch_one_list or pitch_two_list != "None":
            pitch_filter = filter & return_pitch_filter(pitch_one_list, pitch_two_list)

        if pitch_one_list == "None" and pitch_two_list == "None":
            st.write('here')
            pass
        else:
            filter = filter & pitch_filter
    '''
    #return df
    #st.write(pitch_filter)
    return df.lazy().filter(filter).sort("Amount", descending=True).head(200).collect()

    #st.dataframe(table[["Name", "Pitch 1", "Pitch 2", "Amount", "%"]])
    #create_csv_button(table, "Team Sequencing")
    #return table


def calculate_league_sequencing(df: pl.DataFrame, api_call: str) -> Any:
    """
    :param df: Data from teams.csv dataframe
    :param api_call: type of sequencing filter. Example: pitch_type, pitch_type_with_location, pitch_group
    :return:
    """
    table = df.lazy().filter(pl.col("Call") == api_call).collect()
    grouped = table.group_by("Team", "Pitch 1", "Pitch 2").agg(pl.col(["Amount"]).sum())
    return st.dataframe(grouped.sort(by="Amount", descending=True))


def calculate_percentage(data: pl.DataFrame) -> pl.DataFrame:
    """

    creates % column

    :param data: data from team csv
    :return: data with % column appended
    """
    grouped = data.group_by("Pitcher").agg(pl.col("Amount").sum())
    return data.join(grouped, how="full", on="Pitcher")


def read_df(df: pd.DataFrame) -> pl.DataFrame:
    """
    Turns pandas df into polars df

    :param df: pandas df
    :return: polars df
    """
    return pl.read_csv(df)
