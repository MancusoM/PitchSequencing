import streamlit as st
import polars as pl
from typing import Any, Union
import pandas as pd

st.cache_data()


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


st.cache_data()


def return_filtered_dataframes(
    dataframe: pl.DataFrame,
    filter_1: Union[str],
    filter_2: Union[str],
    target_col1: str,
    target_col2: str,
) -> pl.DataFrame:
    """
    function that is responsible for multiple acts of filtering via polars

    :param dataframe: pre-filtered dataframe
    :param filter_1: value 1 to be filtered
    :param filter_2: value 2 to be filtered
    :param target_col1: column that is filtered by value 1
    :param target_col2: column that is filtered by value 2
    :return:filtered dataframe
    """
    if filter_1 == "None" or filter_1 == None:
        if filter_2 == "None" or filter_2 == None:
            return dataframe
        else:
            return dataframe.lazy().filter(pl.col(target_col2) == filter_2).collect()
    else:
        if filter_2 == "None" or filter_2 == None:
            return dataframe.lazy().filter(pl.col(target_col1) == filter_1).collect()
        else:
            return (
                dataframe.lazy()
                .filter(
                    pl.col(target_col1) == filter_1,
                    pl.col(target_col2) == filter_2,
                )
                .collect()
            )


st.cache_data()


def calculate_percentage(data: pl.DataFrame) -> pl.DataFrame:
    """

    creates % column

    :param data: data from team csv
    :return: data with % column appended
    """
    grouped = data.group_by("Pitcher").agg(pl.col("Amount").sum())
    return data.join(grouped, how="full", on="Pitcher")


st.cache_data()


def read_df(df: pd.DataFrame) -> pl.DataFrame:
    """
    Turns pandas df into polars df

    :param df: pandas df
    :return: polars df
    """
    return pl.read_csv(df)


st.cache_data()


def set_up_footer(table: pl.DataFrame, sequence: pl.DataFrame, mlbID: str) -> None:
    """
    Sets up footer with option to export data

    :param table: table with aggregated filtering data
    :param sequence: sequencing data from API Call
    :param mlbID: MLBAM ID
    :return:

    """
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


st.cache_data()


def set_up_list(table: Union[str] | pl.DataFrame, column: str, option: str) -> Any:
    """
    Creates Filters Located on the sidebar

    First 3 lines are necessary since input may be a dataframe or a list
    Sets up the Pitch Type List located on the sidebar

    :param table: dataframe/list containing list information
    :param column: if input is a dataframe, column will contain the information to be placed into the sidebar list
    :param option: Name of Filter
    :return:
    """
    if isinstance(table, pl.DataFrame):
        pitch_list = table[column]
    else:
        pitch_list = sorted(table)
    pitch_list = sorted(list(set(pitch_list)))
    pitch_list.insert(0, "None")
    default_pitch = pitch_list.index("None")

    return st.selectbox(f"{option} Filter", pitch_list, index=default_pitch)
