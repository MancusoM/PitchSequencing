# Pitch Sequencing 

This Python script powers the backend of a Streamlit "Pitch Sequencing" Dashboard that interacts with pybaseball to display real-time pitch sequencing data. This data is processed and returned as Polars DataFrames for easy manipulation and analysis.

## (Need to Add) Requirements
- Python 3.x
- `regex` library
- `requests` library
- `polars` library
- `numpy` library
- `tqdm` library
- `pytz` library


## Folders 
#### `Calculations`

##### calculate_sequencing.py
Stores functions that ingest, massage, format, and normalize PyBaseball data to pitch sequences


#### 'Data'
- Player data from Fangraphs. used to merge data from PyBaseball using the 'MLBAMID'

#### 'helper_functions'
- runs main functions, creates csv export functionality, returns streamlit table to website, calculates team and league percentages

#### 'website'
- set streamlit functionality

- check calculate_sequence is duplicate

Checks if the provided sport ID exists in the list of sports retrieved from the MLB API.
