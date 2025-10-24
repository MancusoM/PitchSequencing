from datetime import datetime

from sequence import call_statcast_pitcher
import streamlit as st
from datetime import date

selected_range = st.date_input(
    "Select a date range",
    value=(date(2025, 1, 1), date(2025, 12, 31)),  # Default range
    min_value=date(2022, 1, 1),
    max_value=date(2025, 12, 31)
)


call_statcast_pitcher(str(selected_range[0]),'2025-12-31',621242)