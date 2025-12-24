import pandas as pd
import polars as pl

from pathlib import Path

current_script_path = Path(__file__).resolve()
parent_directory = current_script_path.parent.parent

print(parent_directory)

data = pl.read_csv(parent_directory / "data/teams.csv")

print(data["Team"].n_unique())

# updated_data = data.filter(pl.col("Team") !='SD')

# updated_data.write_csv(f'{parent_directory}/data/teams.csv')

# .to_csv(f'{parent_directory}/data/teams.csv', mode ='a',index=False,header=False)
