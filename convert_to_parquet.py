##########################################
# Lab # 5 # Dataset Conversion           #
# Kenda S Breish # HSC4933.005 9/29/2026 #

import pandas as pd

df = pd.read_csv("Maternal Health Risk Data Set.csv")

df = df.loc[:, ~df.columns.duplicated()]

parquet_file = ("Maternal Health Risk Data Set.parquet")

df.to_parquet(parquet_file, engine="pyarrow", index=False)

print(f"Wrote {len(df)} rows to {parquet_file}")