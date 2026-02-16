from website_operations.website_funcs import calculate_sequence
import streamlit as st
import polars as pl
from typing import Any

st.cache_data()


def run_main_functions(
    pitcher: str,
    players: pl.DataFrame,
    sequencing_choice: str,
    selected_range: Any,
    platoon: str,
) -> tuple[Any, Any, Any]:
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

    except Exception:  # type:ignore
        return st.error(
            "An Error Has Occurred. \n Please Refresh The Page. Contact the author if this persists",
            icon="🚨",
        )
    return table, sequence, mlbID


st.cache_data()


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

    return df.lazy().filter(filter).sort("Amount", descending=True).collect()
