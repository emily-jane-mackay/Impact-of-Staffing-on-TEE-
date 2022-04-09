# %%
import pathlib
import pandas as pd
import numpy as np
dirname = pathlib.Path(__file__).resolve().parent
# %%
# %%
# load data file (with headers)
# & save as dataframe (label convention "df_")
in_file = dirname / f'../data/zip_code_database.csv'
df_geo = pd.read_csv(
  in_file,
  dtype=str,
  index_col=False
)
column_names_geo = df_geo.columns.values

# %%
df_geo.head()

# %%
df_geo = df_geo.add_prefix('geo_')

# %%
df_geo.head()

# drop columns 
df_geo.drop([
  'geo_decommissioned', 
  'geo_acceptable_cities', 
  'geo_unacceptable_cities', 
  'geo_world_region', 
  'geo_irs_estimated_population_2015', 
], 
axis=1).copy()

# check
df_geo.head()

# check zip
df_geo['geo_zip'].value_counts(normalize=True, dropna=False)
df_geo['geo_latitude'].value_counts(normalize=True, dropna=False)
df_geo['geo_longitude'].value_counts(normalize=True, dropna=False)

# convert latitude & longitude to integer
df_geo['geo_latitude'] = pd.to_numeric(df_geo['geo_latitude'])
df_geo['geo_longitude'] = pd.to_numeric(df_geo['geo_longitude'])

# %%
# save to parquet file
df_geo.to_parquet(dirname / f'../data/geo_processed_data.parquet', engine='pyarrow')
