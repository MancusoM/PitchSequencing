import pandas as pd
import polars as pl

data = pl.read_csv("testing.csv")

grouped = data.group_by("Pitcher").agg(pl.col("Amount").sum())
merged = data.join(grouped, how="full", on="Pitcher")

print(merged.columns)
