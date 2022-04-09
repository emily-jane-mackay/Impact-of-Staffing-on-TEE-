# %%
import pathlib
import pandas as pd
dirname = pathlib.Path(__file__).resolve().parent

# %%
# load data file (with headers)
# & save as dataframe (label convention "df_")
in_file = dirname / f'../data/ahrf_edit.csv'
df_ahrf = pd.read_csv(
  in_file,
  dtype=str,
  index_col=False
)
column_names_ahrf = df_ahrf.columns.values
# %%

df_ahrf = df_ahrf.add_prefix('ahrf_')

# %% 
# convert columns with continuous data to numeric
df_ahrf['ahrf_anes_MD_total_2015'] = pd.to_numeric(df_ahrf['ahrf_anes_MD_total_2015'])
df_ahrf['ahrf_anes_MD_total_2010'] = pd.to_numeric(df_ahrf['ahrf_anes_MD_total_2010'])
df_ahrf['ahrf_anes_DO_total_2015'] = pd.to_numeric(df_ahrf['ahrf_anes_DO_total_2015'])
df_ahrf['ahrf_anes_DO_total_2010'] = pd.to_numeric(df_ahrf['ahrf_anes_DO_total_2010'])
df_ahrf['ahrf_anes_CRNA_npi_2015'] = pd.to_numeric(df_ahrf['ahrf_anes_CRNA_npi_2015'])
df_ahrf['ahrf_anes_CRNA_npi_2010'] = pd.to_numeric(df_ahrf['ahrf_anes_CRNA_npi_2010'])
df_ahrf['ahrf_surg_total_2015'] = pd.to_numeric(df_ahrf['ahrf_surg_total_2015'])
df_ahrf['ahrf_surg_total_2010'] = pd.to_numeric(df_ahrf['ahrf_surg_total_2010'])
df_ahrf['ahrf_thoracic_surgery_2015'] = pd.to_numeric(df_ahrf['ahrf_thoracic_surgery_2015'])
df_ahrf['ahrf_thoracic_surgery_2010'] = pd.to_numeric(df_ahrf['ahrf_thoracic_surgery_2010'])

# %%
# save to parquet file
df_ahrf.to_parquet(dirname / f'../data/ahrf_processed_data.parquet', engine='pyarrow')

# %% 

