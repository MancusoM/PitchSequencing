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
        st.dataframe(table[["Pitch 1", "Pitch 2", "Amount", "%"]], hide_index=True)

    except Exception:  # type:ignore
        return st.error("An Error Has Occurred. \nPlease Refresh The Page", icon="🚨")

    head_col1, head_col2, head_col3 = st.columns(3)
    with head_col1:
        create_csv_button(sequence, "Raw Sequencing")
    with head_col2:
        create_csv_button(table, "Frequency")
    with head_col3:
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


def calculate_team_sequencing(
    df: pl.DataFrame, team: str, api_call: str
) -> pl.DataFrame:
    """

    Extracts top 100 results from teams.csv filtered by user selections

    :param df: Data from teams.csv dataframe
    :param team: team filter. Default is all. Examples: NYM, NYY, etc.
    :param api_call: type of sequencing filter. Example: pitch_type, pitch_type_with_location, pitch_group
    :return: table from streamlit

    """

    if team == "All":
        filter = pl.col("Call") == api_call  # type:ignore
    else:
        filter = (pl.col("Team") == team) & (pl.col("Call") == api_call)  # type:ignore

    table = df.lazy().filter(filter).unique().sort("Amount", descending=True).head(200).collect()

    if api_call == 'pitch_type':
        st.dataframe(table[["Name", "Pitch 1", 'Pitch 1 Whiff %',"Pitch 2",'Pitch 2 Whiff %', "Amount", "Usage %"]])

    if api_call == 'pitch_zone_combo':
        st.dataframe(table[["Name", "Pitch 1", 'Pitch 1 Whiff %',"Pitch 2",'Pitch 2 Whiff %', "Amount", "Usage %"]])


    else:
        st.dataframe(table[["Name", "Pitch 1", "Pitch 2", "Amount", "Usage %"]])

    create_csv_button(table, "Team Sequencing")
    return table


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
