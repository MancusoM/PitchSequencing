from website_operations.website_funcs import calculate_sequence
import streamlit as st
import polars as pl
from typing import Union, Any
# Add documentation


def run_main_functions(
    pitcher: str,
    players: pl.DataFrame,
    sequencing_choice: str,
    selected_range: Any,
    platoon: str,
) -> Union[pl.DataFrame, pl.DataFrame]:
    """


    :param pitcher:
    :param players:
    :param sequencing_choice:
    :param selected_range:
    :param platoon:
    :return:
    """
    try:
        table, sequence, mlbID = calculate_sequence(
            pitcher, players, sequencing_choice, selected_range, platoon
        )
        st.dataframe(table[["Pitch 1", "Pitch 2", "Amount", "%"]], hide_index=True)

    except:
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


def create_csv_button(df: pl.DataFrame, name: str) -> Any:
    """

    :param df:
    :param name:
    :return:
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

    :param df:
    :param team:
    :param api_call:
    :return:
    """

    if team == "All":
        filter = (pl.col("Call") == api_call)
    else:
        filter = (pl.col("Team") == team) & (pl.col("Call") == api_call)

    table = (
        df.lazy()
        .filter(filter)
        .head(100)
        .collect()
    )

    st.dataframe(table[["Name", "Pitch 1", "Pitch 2", "Amount", "%"]])
    create_csv_button(table, "Team Sequencing")
    return table


def calculate_league_sequencing(df: pl.DataFrame, api_call: str) -> Any:
    """

    :param df:
    :param api_call:
    :return:
    """
    table = df.lazy().filter(pl.col("Call") == api_call).collect()
    grouped = table.group_by("Pitch 1", "Pitch 2").agg(pl.col(["Amount"]).sum())
    return st.dataframe(grouped.sort(by="Amount", descending=True))


def calculate_percentage(data: pl.DataFrame) -> pl.DataFrame:
    """

    :param data:
    :return:
    """
    grouped = data.group_by("Pitcher").agg(pl.col("Amount").sum())
    return data.join(grouped, how="full", on="Pitcher")
