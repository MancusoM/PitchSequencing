import requests
import streamlit as st

st.cache_data()


def return_profile_pics(mlbId: int) -> bytes | None:
    """
    Calls MLB's API to return the player's profile picture.

    :param mlbId: MLBAM ID
    :return: data containing the bytes of
    """
    url = f"https://img.mlbstatic.com/mlb-photos/image/upload/w_130,d_people:generic:headshot:silo:current.png,q_auto:best,f_auto/v1/people/{mlbId}/headshot/67/current"
    # url = f"https://securea.mlb.com/mlb/images/players/head_shot/{mlbId}.jpg"
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        return response.content
    else:
        return None
