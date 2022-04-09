# %%
import pathlib
import numpy as np
import pandas as pd
dirname = pathlib.Path(__file__).resolve().parent

# %%
# load concatenated data file (with headers)
# & save as dataframe (label convention "df_")
in_file = dirname / f'../data/out.csv'
df_cms = pd.read_csv(
  in_file,
  dtype=str,
  index_col=False
)
column_names_cms = df_cms.columns.values

# %%
# row count
len(df_cms.index)
# column count 
len(df_cms.columns.values)
# show column labels
print(df_cms.columns)

# %%
# set option to display all columns & rows
pd.set_option("display.max_columns", None)
pd.set_option("display.min_rows", 100)
pd.set_option("display.max_rows", 100)
# %%
print(df_cms.columns.tolist())

# %%
# row and column count
df_cms.shape 

# %%
# view first five rows
df_cms.head()
# view first 20 rows
df_cms.head(20)

# %%
# view last five rows
df_cms.tail()
# view last 20 rows
df_cms.tail(20)

# %%
# view selected rows
df_cms[10000:10100]

# %%
# display all columns and data types 
df_cms.info()

# %%
# describe the data 
df_cms.describe()

# %%
# look at a single column
df_cms['prvdr_num']
df_cms['prvdr_num'].values
df_cms['prvdr_num'].value_counts()

# %%
df_cms.filter(regex=("dgns")).columns

# %% 
# define a new dataframe for visualizing with filtered columns required for merging 
# note: must be a copy of the original if data manipulation is planned 
df_cms_filtered = df_cms.copy()

# %%
# display all columns 
df_cms_filtered.columns.values

# %%
# regex index link: https://regex101.com 
# display all columns containing "yr"
df_cms_filtered.filter(regex=("yr")).columns
# display all columns begining with "yr"
df_cms_filtered.filter(regex=("^yr")).columns
# display all columns ending with "yr" 
df_cms_filtered.filter(regex=("yr$")).columns

# %%
# create dataframe with columns relevant for merging, cohort development, & statistics
c = df_cms_filtered[[
  'bene_id', 'medpar_id', 'dup_n', 'seq_ct_index', 
  'bene_dob_denom_auto', 'yr', 'prvdr_num', 'prvdrsrl', 
  'admsnday', 'admsndt', 'src_adms', 'org_npi_num_medpar', 
  'prf_physn_npi_srg', 'org_npi_num_srg', 'prf_physn_npi_tee', 'org_npi_num_tee', 
  'prf_physn_npi_tte', 'org_npi_num_tte', 'org_npi_num', 'org_npi_num_str',
  'drg_cd', 'drg_ct', 'tee', 'cpt_tee', 
  'change', 'MC', 't', 'surgery_ct', 
  'c', 'surgery_c', 'v', 'surgery_v',
  'valve', 'valve_s', 'v_valve', 'valve_categorized', 
  'TAVR', 'TMVR', 'aortic_repair', 'aortic_replace', 
  'mitral_repair', 'mitral_replace', 'pulmonic_repair', 'pulmonic_replace', 
  'tricuspid_repair','tricuspid_replace', 'hv_repair_unspecified', 'hv_replace_unspecified', 
  'cabg_s', 'valve_plus_cabg', 'age_cnt', 'acmdtns', 
  'admit_date', 'admit_type', 'geographic', 'cnty_cd', 
  'state_cd_medpar', 'state_cd', 'bene_zip', 'bene_zip_denom',  
  'dschrgdt', 'disch_date', 'cov_date_2', 'covstart_denom_auto', 
  'cov_to_srg', 'cov_at_least_6_mo', 'ansthsa', 'dschrgcd', 
  'bic', 'sex_medpar', 'sex', 'race_medpar', 
  'race', 'race_str', 'clm_thru_dt_srg', 'carr_prfrng_pin_num_srg', 
  'tax_num_srg', 'prvdr_state_cd_srg', 'prvdr_zip_srg', 'prvdr_spclty_srg',
  'clm_thru_dt_tee', 'line_1st_expns_dt_tee', 'line_last_expns_dt_tee', 'clm_id_tee', 
  'carr_prfrng_pin_num_tee', 'tax_num_tee', 'prvdr_state_cd_tee', 'prvdr_zip_tee', 
  'prvdr_spclty_tee', 'betos_cd_tee', 'prvdr_perform_tee', 'line_icd_dgns_cd_tee', 
  'line_icd_dgns_vrsn_cd_tee', 'cpt_cv', 'ad_dgns',
  'dgns_cd01', 'dgns_cd02', 'dgns_cd03', 'dgns_cd04', 'dgns_cd05',
  'dgns_cd06', 'dgns_cd07', 'dgns_cd08', 'dgns_cd09', 'dgns_cd10',
  'dgns_cd11', 'dgns_cd12', 'dgns_cd13', 'dgns_cd14', 'dgns_cd15',
  'dgns_cd16', 'dgns_cd17', 'dgns_cd18', 'dgns_cd19', 'dgns_cd20',
  'dgns_cd21', 'dgns_cd22', 'dgns_cd23', 'dgns_cd24', 'dgns_cd25',
  'hcpcs_cd_srg', 'hcpcs_1st_mdfr_cd_srg', 'hcpcs_2nd_mdfr_cd_srg',
  'hcpcs_cd_tee', 'hcpcs_1st_mdfr_cd_tee', 'hcpcs_2nd_mdfr_cd_tee',
  'hcpcs_cd_tte', 'hcpcs_1st_mdfr_cd_tte', 'hcpcs_2nd_mdfr_cd_tte',
  'dgns_poa_cd', 'poa_dgns_cd_cnt', 'poa_dgns_1_ind_cd',
  'poa_dgns_2_ind_cd', 'poa_dgns_3_ind_cd', 'poa_dgns_4_ind_cd',
  'poa_dgns_5_ind_cd', 'poa_dgns_6_ind_cd', 'poa_dgns_7_ind_cd',
  'poa_dgns_8_ind_cd', 'poa_dgns_9_ind_cd', 'poa_dgns_10_ind_cd',
  'poa_dgns_11_ind_cd', 'poa_dgns_12_ind_cd', 'poa_dgns_13_ind_cd',
  'poa_dgns_14_ind_cd', 'poa_dgns_15_ind_cd', 'poa_dgns_16_ind_cd',
  'poa_dgns_17_ind_cd', 'poa_dgns_18_ind_cd', 'poa_dgns_19_ind_cd',
  'poa_dgns_20_ind_cd', 'poa_dgns_21_ind_cd', 'poa_dgns_22_ind_cd',
  'poa_dgns_23_ind_cd', 'poa_dgns_24_ind_cd', 'poa_dgns_25_ind_cd',
  'esophageal_poa', 'alcohol_poa', 'arrhythmia_poa', 'blood_loss_poa', 
  'chf_poa', 'coagulopathy_poa', 'cpd_poa', 'anemia_poa', 
  'depression_poa', 'diabetes_poa', 'diabetes_cx_poa', 'diabetes_all_poa', 
  'drugs_poa', 'electrolytes_poa', 'htn_poa', 'htn_cx_poa', 
  'htn_all_poa', 'hypothyroid_poa', 'liver_poa', 'lymphoma_poa', 
  'metastasis_poa', 'neuro_poa', 'obesity_poa', 'paralysis_poa', 
  'psychosis_poa', 'pulm_circ_poa', 'pvd_poa', 'renal_poa', 
  'rheumatoid_poa', 'valve_poa', 'weight_loss_poa', 'angina_poa', 
  'solid_tumor_poa', 'stroke_poa', 'mi_poa', 'alcohol_6_preexist', 
  'arrhythmia_6_preexist', 'blood_loss_6_preexist', 'chf_6_preexist', 
  'coagulopathy_6_preexist', 'cpd_6_preexist', 'anemia_6_preexist', 
  'depression_6_preexist', 'diabetes_6_preexist', 'diabetes_cx_6_preexist', 
  'diabetes_all_6_preexist', 'electrolytes_6_preexist', 'htn_6_preexist', 
  'htn_cx_6_preexist', 'htn_all_6_preexist', 'hypothyroid_6_preexist', 'liver_6_preexist',
  'lymphoma_6_preexist', 'metastasis_6_preexist', 'neuro_6_preexist', 'obesity_6_preexist', 
  'paralysis_6_preexist', 'psychosis_6_preexist', 'pulm_circ_6_preexist', 'pvd_6_preexist', 
  'renal_6_preexist', 'rheumatoid_6_preexist', 'ulcer_6_preexist', 'valve_6_preexist',
  'weight_loss_6_preexist', 'angina_6_preexist', 'solid_tumor_6_preexist', 'stroke_6_preexist', 
  'esophageal_6_preexist', 
  'deathdt', 'deathday', 'deathcd', 'death_dt_denom', 
  'death_dt_denom_auto', 'death_30_day', 'death_1_year', 
  'loh', 'log_loh', 'loh_1', 'log_loh_1', 
  'esophageal_perf', 'acute_stroke', 
]].copy()

# check for duplicated columns (sanity check) 
c.columns.value_counts()

# %% 
# parse dates for format 06FEB2013 
c['admsndt_date'] = pd.to_datetime(c['admsndt'], format='%d%b%Y')
c['dschrgdt_date'] = pd.to_datetime(c['dschrgdt'], format='%d%b%Y')
c['bene_dob_denom_auto_date'] = pd.to_datetime(c['bene_dob_denom_auto'], format='%d%b%Y')
c['death_dt_denom_auto_date'] = pd.to_datetime(c['death_dt_denom_auto'], format='%d%b%Y')
c['clm_thru_dt_srg_date'] = pd.to_datetime(c['clm_thru_dt_srg'], format='%d%b%Y')
c['clm_thru_dt_tee_date'] = pd.to_datetime(c['clm_thru_dt_tee'], format='%d%b%Y')

# %%
# clean bene zip
# add leading zeros to beneficiary zip
c['bene_zip'] = c['bene_zip'].apply(lambda x: '{0:0>5}'.format(x))
c['bene_zip_denom'] = c['bene_zip_denom'].apply(lambda x: '{0:0>5}'.format(x))                                         

# %%
# lists all duplicate bene_id in dataframe 
c[c.duplicated(subset=['bene_id'])]

# %%
# sort prior to drop duplicates 
# sort in place
c.sort_values(by=['bene_id', 'dup_n', 'admsndt_date'], inplace=True)

# %%
# look at duplicates
dupes = c[c.duplicated(subset=['bene_id'])]
dupes['bene_id'].unique().tolist()
# random duplicate sample
np.random.choice(dupes['bene_id'].unique(), 10)

# %% 
# data management prior to droping duplicates
# look at selected columns for a single patient
# be certain columns of interest are in the correct order prior to droppping duplicates
c[c["bene_id"] == 'lllllllQQJQJj9P']
c[c["bene_id"] == 'llllll00A009JVX']
c[c["bene_id"] == 'lllllllQJ0AJlVV']
c[c["bene_id"] == 'llllllljPXj99lA']
c[c["bene_id"] == 'llllllPQ909l99X']
c[c["bene_id"] == 'lllllll0PXl9PJX']
c[c["bene_id"] == 'lllllll0XJQP009']
c[c["bene_id"] == 'lllllllXlQ9l9A0']
c[c["bene_id"] == 'lllllllJjPAj9Xj']
c[c["bene_id"] == 'lllllll0AlAPQPl']

# look at column dup_n (condition drop on bene_id & (dup_n == 1))
c['dup_n'].value_counts()

# %% 
# drop duplicates after confirmed sorting 
c.drop_duplicates(subset=['bene_id', 'admsndt_date'], keep='first', inplace=True)

# %%
# sanity check 
# look for duplicates after duplicates drop (should be zero) 
dupes_2 = c[c.duplicated(subset=['bene_id'])]
dupes_2['bene_id'].unique().tolist()

# %% 
# look at distribution of 05 - Anesthesiology & 06 - Cardiology 
# only consider rows where tee == '1'
c.filter(regex=("tee")).columns
c[c['tee'] == '1']['prvdr_spclty_tee'].value_counts(dropna=False)
c[c['tee'] == '1']['prvdr_spclty_tee'].value_counts(normalize=True, dropna=False)

# %%
# view first five rows
c.head()
# view first 20 rows
c.head(20)

# %%
# view last five rows
c.tail()
# view last 20 rows
c.tail(20)

# %% 
# generate random row sample df
r = c 
r.sample(n=50)
r

# %% 
# add column name prefix
c = c.add_prefix('cms_')

# %% 
# look @ random sample 
r = c.sample(n=50)
r

# %%
# identify colums (note: beneficiary counties)
c.filter(regex=("cnty")).columns
c.filter(regex=("state")).columns
# add leading zeros to key columns 
c['cms_cnty_cd'] = c['cms_cnty_cd'].apply(lambda x: '{0:0>3}'.format(x)) 
c['cms_state_cd'] = c['cms_state_cd'].apply(lambda x: '{0:0>2}'.format(x)) 
c['cms_prvdr_zip_srg'] = c['cms_prvdr_zip_srg'].apply(lambda x: '{0:0>9}'.format(x))
c['cms_prvdr_zip_tee'] = c['cms_prvdr_zip_tee'].apply(lambda x: '{0:0>9}'.format(x))
c['cms_drg_cd'] = c['cms_drg_cd'].apply(lambda x: '{0:0>3}'.format(x)) 


# create SSA 5-digit column
c["cms_SSA_5_digit"] = c.cms_state_cd.str.cat(others=[c.cms_cnty_cd])

# convert object to integer (numeric) 
c['cms_age_cnt'] = pd.to_numeric(c['cms_age_cnt'])
c['cms_yr'] = pd.to_numeric(c['cms_yr'])
c['cms_loh'] = pd.to_numeric(c['cms_loh'])
c['cms_log_loh'] = pd.to_numeric(c['cms_log_loh'])

# %%
# srg zip 
c['cms_prvdr_zip_srg'].value_counts()
c['cms_prvdr_zip_tee'].value_counts()

# map binary categorical to 1 vs 0
c['cms_c'].value_counts(dropna=False)
c['cms_c'].replace({ np.nan: '0' }, inplace = True)
c['cms_c'].value_counts(dropna=False)
# 
c['cms_v'].value_counts(dropna=False)
c['cms_v'].replace({ np.nan: '0' }, inplace = True)
c['cms_v'].value_counts(dropna=False)
# 
c['cms_tee'].value_counts(dropna=False)
c['cms_tee'].replace({ np.nan: '0' }, inplace = True)
c['cms_tee'].value_counts(dropna=False)

# sex
c['cms_sex'].describe()
c['cms_sex'].value_counts(normalize=True)
c['cms_sex_str'] = np.select(
  condlist=[c['cms_sex'] == '1', c['cms_sex'] == '2'],
  choicelist=['male', 'female'],
  default='unknown'
)
c['cms_sex_str'].value_counts(normalize=True)

# tee
c['cms_tee'].describe()
c['cms_tee'].value_counts(normalize=True, dropna=False)
c['cms_cpt_tee'].value_counts(normalize=True, dropna=False)
c['cms_cpt_tee_str'] = np.select(
  condlist=[c['cms_cpt_tee'] == '1', c['cms_cpt_tee'] == '0'],
  choicelist=['tee', 'no tee'],
  default='unknown'
)
c['cms_cpt_tee_str'].value_counts(normalize=True)

# %%
temp = c[[
  'cms_bene_id', 'cms_medpar_id', 
  'cms_SSA_5_digit',
  'cms_state_cd_medpar', 'cms_cnty_cd', 
  'cms_state_cd', 'cms_geographic', 
  'cms_bene_zip', 'cms_bene_zip_denom', 
  'cms_prvdr_zip_srg', 'cms_prvdr_zip_tee'
]].copy()
temp


# %%
# save to parquet file
c.to_parquet(dirname / f'../data/cms_processed_data.parquet', engine='pyarrow')



# %%
