# %%
import pathlib
import pandas as pd
dirname = pathlib.Path(__file__).resolve().parent

pd.set_option("display.max_columns", None)
pd.set_option("display.min_rows", 100)
pd.set_option("display.max_rows", 100)

# load data
#%%
aha_df = pd.read_parquet(dirname / f'../data/aha_processed_data.parquet')
#%%
ahrf_df = pd.read_parquet(dirname / f'../data/ahrf_processed_data.parquet')
#%%
geo_df = pd.read_parquet(dirname / f'../data/geo_processed_data.parquet')
#%%
cms_df = pd.read_parquet(dirname / f'../data/cms_processed_data.parquet')
#%%
# ssa_fips_df = pd.read_parquet(dirname / f'../data/ssa_fips_processed_data.parquet')

#%%
# check to confirm right_on merge column(s) unique
aha_df.value_counts(subset=['aha_mcrnum', 'aha_year'])
# both cms_yr and aha_year must be numeric 
aha_df['aha_year'] = pd.to_numeric(aha_df['aha_year'])

# merge aha onto cms
merge_1 = cms_df.merge(
  aha_df,
  how='left',
  left_on=['cms_prvdr_num', 'cms_yr'],
  right_on=['aha_mcrnum', 'aha_year'],
  indicator='_merge_aha',
  validate='many_to_one'
)

merge_1.head()
merge_1['_merge_aha'].value_counts()

# %%
# check to confirm right_on merge column(s) unique
ahrf_df['ahrf_AHRF_state_county_5_digit'].value_counts()

merge_2 = merge_1.merge(
  ahrf_df, 
  how='left', 
  left_on=['aha_fcounty'],
  right_on=['ahrf_AHRF_state_county_5_digit'],
  indicator='_merge_ahrf',
  validate='many_to_one'
)

merge_2.head()
merge_2['_merge_ahrf'].value_counts()

# %%
# check to confirm right_on merge column unique
geo_df.head()
geo_df['geo_zip'].value_counts().head()

# look for all columns with zip in merge_3
merge_2.filter(regex=("zip")).columns

merge_3 = merge_2.merge(
  geo_df, 
  how='left', 
  left_on=['cms_bene_zip'],
  right_on=['geo_zip'],
  indicator='_merge_geo_bene', 
  validate='many_to_one', 
)


# rename geo columns for clarity 
merge_3.rename(columns={
  'geo_zip': 'geo_zip_bene',
  'geo_latitude': 'geo_latitude_bene',
  'geo_longitude': 'geo_longitude_bene',
}, inplace=True)

merge_3.head()
merge_3['_merge_geo_bene'].value_counts()
merge_3[pd.isna(merge_3['geo_latitude_bene'])].shape

#%%
merge_4 = merge_3.merge(
  geo_df, 
  how='left', 
  left_on=['aha_mloczip_5'],
  right_on=['geo_zip'],
  indicator='_merge_geo_aha',
  validate='many_to_one',
)

# rename geo columns for clarity 
merge_4.rename(columns={
  'geo_zip': 'geo_zip_aha',
  'geo_latitude': 'geo_latitude_aha',
  'geo_longitude': 'geo_longitude_aha'
}, inplace=True)

merge_4.head()
merge_4['_merge_geo_aha'].value_counts()

# %%
temp = merge_4[[
  'cms_bene_id', 
  'cms_bene_zip', 
  'aha_mloczip_5', 
  'geo_zip_bene', 
  'geo_latitude_bene', 
  'geo_longitude_bene', 
  'geo_zip_aha', 
  'geo_latitude_aha', 
  'geo_longitude_aha', 
  '_merge_geo_bene', 
  '_merge_geo_aha', 
]]

merge_4['_merge_geo_bene'].value_counts()
merge_4['_merge_geo_aha'].value_counts()

#%%
# double check for duplicates
dupes_2 = merge_4[merge_4.duplicated(subset=['cms_bene_id'])]
dupes_2['cms_bene_id'].unique().tolist()

# %%
# save to parquet file
merge_4.to_parquet(dirname / f'../data/merged_data.parquet', engine='pyarrow')

# %%

# %%
# code blocks if merging ahrf data onto beneficiary fips codes 
# requires SSA (CMS-specific 5-digit #) to FIPS (unique FIPS codes) crosswalk file 
# code: 
# ssa_fips_df['ssa_fips_SSA State county code'].value_counts().head()

# merge_number = merge_number.merge(
#   ssa_fips_df, 
#   how='left', 
#   left_on=['cms_SSA_5_digit'],
#   right_on=['ssa_fips_SSA State county code'], 
#   indicator='_merge_ssa',
#   validate='many_to_one'
# )

# merge_number.head()
# merge_number['_merge_ssa'].value_counts()

# %%
# merge FIPs in CMS data to FIPs in ahrf data 
# code
# check to confirm right_on merge column unique
# ahrf_df['ahrf_AHRF_state_county_5_digit'].value_counts().head()

# merge_number = merge_number.merge(
#   ahrf_df, 
#   how='left',
#   left_on=['ssa_fips_FIPS State county code'],
#   right_on=['ahrf_AHRF_state_county_5_digit'], 
#   indicator='_merge_ahrf', 
#   validate='many_to_one'
# )

# merge_number.head()
# merge_number['_merge_ahrf'].value_counts()

