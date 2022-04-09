# %%
import pathlib
from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy import distance
dirname = pathlib.Path(__file__).resolve().parent

pd.set_option("display.max_columns", None)
pd.set_option("display.min_rows", 100)
pd.set_option("display.max_rows", 100)

# load data
#%%
merged_df = pd.read_parquet(dirname / f'../data/merged_data.parquet')

# %%
# regex search 
merged_df.filter(regex=("cms_t")).columns

# %%
# generate random row sample df
r = merged_df
r.sample(n = 3)

# %%
# sequential filtering for exclusion count(s) 
t = merged_df['cms_t']
# starting count for manuscript 
t.value_counts()

temp = merged_df[[
  'cms_bene_id', 
  'cms_MC', 
  'cms_cpt_tee', 
  'aha_id', 
  'cms_hcpcs_cd_tee', 
  'cms_prvdr_zip_srg', 
  'cms_prvdr_zip_srg',
  'cms_yr'
]]
temp

# %% 
# look at column cms_yr 
# [exclude condition: cms_yr == 2009-2012]
# [include condition: cms_yr == 2013-2015]
t = merged_df['cms_yr']
t.value_counts()
# create dataframe with include condition
df_c_0 = merged_df[(merged_df['cms_yr'] >= 2013)]
# sanity check 
t = df_c_0['cms_yr']
t.value_counts()
# count for manuscript 
len(merged_df)
# starting inclusion count
175557 + 168527 + 140195
len(df_c_0)

# %% 
# look at column cms_MC 
# [exclude condition: MC == 1]
# [include condition: MC == 0]
t = df_c_0['cms_MC']
t.value_counts()
# create dataframe with include condition
df_c_1 = df_c_0[(df_c_0['cms_MC'] == '0')]
# sanity check 
t = df_c_1['cms_MC']
t.value_counts()
# count for manuscript 
len(df_c_0)
484279 - 109139
len(df_c_1)

# %%
# look at column cms_cov_at_least_6_mo 
# [exclude condition: cms_cov_at_least_6_mo == 0] 
# [include condition: cms_cov_at_least_6_mo == 1]
t = df_c_1['cms_cov_at_least_6_mo']
t.value_counts()
# create dataframe with include condition 
df_c_2 = df_c_1[(df_c_1['cms_cov_at_least_6_mo'] == '1')]
# sanity check 
t = df_c_2['cms_MC']
t.value_counts()
# count for manuscript 
len(df_c_1)
375140 - 10665
len(df_c_2)

# %%
# look at column cms_drg_ct
# [exclude condition: cms_drg_ct == 0]
# [include condition: cms_drg_ct == 1]
t = df_c_2['cms_drg_ct']
t.value_counts()
# create dataframe with include condition 
df_c_3 = df_c_2[(df_c_2['cms_drg_ct'] == '1')]
# sanity check 
t = df_c_3['cms_drg_ct']
t.value_counts()
# count for manuscript 
len(df_c_2)
364475 - 3451
len(df_c_3)

# %%
# look at column cms_age_cnt
# [exclude condition: cms_age_cnt < 65]
# [include condition: cms_age_cnt >= 65]
(df_c_3['cms_age_cnt'] >= 65).sum()
(df_c_3['cms_age_cnt'] < 65).sum()
# create dataframe with include condition 
df_c_4 = df_c_3[(df_c_3['cms_age_cnt'] >= 65)]
# sanity check 
(df_c_4['cms_age_cnt'] >= 65).sum()
(df_c_4['cms_age_cnt'] < 65).sum()
# count for manuscript 
len(df_c_3)
361024 - 34096
len(df_c_4)

# %%
# [exclude condition: cms_yr <= 2008]
# [include condition: cms_yr > 2008]
(df_c_4['cms_yr'] > 2008).sum()
(df_c_4['cms_yr'] <= 2008).sum()
# create dataframe with include condition 
df_c_5 = df_c_4[(df_c_4['cms_yr'] > 2008)]
# sanity check 
(df_c_5['cms_yr'] > 2008).sum()
(df_c_5['cms_yr'] <= 2008).sum()
# count for manuscript
# note: should be zero based on the above exclusion criteria 2009 - 2012
len(df_c_4)
326928 - 0 
len(df_c_5)

# %% 
# look at column cms_TAVR
# [exclude condition: cms_TAVR == 1]
# [include condition: cms_TAVR == 0]
t = df_c_5['cms_TAVR']
t.value_counts()
# create dataframe with include condition 
df_c_6 = df_c_5[(df_c_5['cms_TAVR'] == '0')]
# sanity check 
t = df_c_6['cms_TAVR']
t.value_counts()
# count for manuscript 
len(df_c_5)
326928 - 35726
len(df_c_6)

# %% 
# look at column cms_TMVR
# [exclude condition: cms_TMVR == 1]
# [include condition: cms_TMVR == .]
t = df_c_6['cms_TMVR']
t.value_counts()
# create dataframe with include condition 
df_c_7 = df_c_6[(df_c_6['cms_TMVR'] == '0')]
# sanity check 
t = df_c_7['cms_TMVR']
t.value_counts()
# count for manuscript 
len(df_c_6)
291202 - 195
len(df_c_7)

# %% 
# look at column _merge_aha
# [exclude condition: _merge_aha == 'left_only']
# [include condition: _merge_aha == 'both']
t = df_c_7['_merge_aha']
t.value_counts(dropna=False)
# create dataframe with include condition 
df_c_8 = df_c_7[(df_c_7['_merge_aha'] == 'both')]
# sanity check 
t = df_c_8['_merge_aha']
t.value_counts()
# count for manuscript 
len(df_c_7)
291007 - 479
len(df_c_8)

# %% 
# look at column cms_admit_type
# [exclude condition: cms_admit_type == 'Newborn']
# [include condition: cms_admit_type != 'Newborn']
t = df_c_8['cms_admit_type']
t.value_counts(dropna=False)
# create dataframe with include condition 
df_c_9 = df_c_8[(df_c_8['cms_admit_type'] != 'Newborn')]
# sanity check 
t = df_c_9['cms_admit_type']
t.value_counts()
# count for manuscript 
len(df_c_8)
290528 - 3
len(df_c_9)

# %% 
# look at column aha_mstate
# [exclude count: aha_mstate 'PR'(809) 'GU'(0), 'VI'(0), 'AK'(415), 'HI'(759)]
t = df_c_9['aha_mstate']
t.value_counts(dropna=False)
# create dataframe with include condition 
df_c_10 = df_c_9[~(df_c_9['aha_mstate'].isin(['PR', 'GU', 'VI', 'AK', 'HI']))]
# sanity check 
t = df_c_10['aha_mstate']
t.value_counts()
# count for manuscript 
len(df_c_9)
809 + 0 + 0 + 415 + 759  
209525 - 1983
# final inclusion count 
len(df_c_10)


# %% 
# define final cohort 
df_c = df_c_10.copy()

# final cohort count for manuscript 
t = df_c['cms_t']
t.value_counts()
len(df_c)

df_c['_merge_geo_bene'].value_counts()
df_c['_merge_geo_aha'].value_counts()

# ------------------ #
# create new columns
# ------------------ # 

# %%
# look at TEE provider column
df_c['cms_prvdr_spclty_tee'].value_counts(dropna=False)
df_c[df_c['cms_tee'] == '1']['cms_prvdr_spclty_tee'].value_counts()
df_c[df_c['cms_tee'] == '1']['cms_prvdr_spclty_tee'].value_counts(normalize=True, dropna=False)
# create labeled TEE provider column

#%% categorize tee provider
df_c['cms_tee_provider'] = np.select(
  condlist=[df_c['cms_prvdr_spclty_tee'] == '05', df_c['cms_prvdr_spclty_tee'] == '06', pd.isna(df_c['cms_prvdr_spclty_tee'])],
  choicelist=['anesthesiologist', 'cardiologist', 'no value'],
  default='other'
)

#%% create provider ratio variable
def calculate_provider_ratio(df):
  counts = df['cms_tee_provider'].value_counts(dropna=False)
  total_tee_count = np.maximum(counts.get('cardiologist', 0) + counts.get('anesthesiologist', 0) + counts.get('other', 0), 1)
  return pd.Series({
    'anesthesiologist_tee_ratio': counts.get('anesthesiologist', 0) / total_tee_count,
    'cardiologist_tee_ratio': counts.get('cardiologist', 0) / total_tee_count
  })
hospital_groups = df_c.groupby('cms_org_npi_num')
provider_ratios_df = hospital_groups.apply(calculate_provider_ratio).reset_index()
df_c = df_c.merge(
  provider_ratios_df,
  how='left',
  on='cms_org_npi_num',
  validate='many_to_one'
)

# %%
df_c[df_c['cms_tee'] == '1']['cms_tee_provider'].value_counts(normalize=True)
df_c['cms_tee_provider'].value_counts(normalize=True)


# %%
# define a function to calculate TEE rates by organization (to be called)
def calculate_rates(df):
  # check data distribution for key columns cms_  
  df['cms_org_npi_num'].describe()
  df['cms_prf_physn_npi_srg'].describe()

  #%% count org surgery volume
  org_counts = df['cms_org_npi_num'].value_counts(dropna=False)
  org_counts.describe()
  org_counts.hist(bins=100)
  df['cms_org_npi_count'] = df['cms_org_npi_num'].map(org_counts)
  df['cms_org_npi_annual_count'] = df['cms_org_npi_num'].map(org_counts) / 3.0

  #%% count physician surgery volume
  phys_counts = df['cms_prf_physn_npi_srg'].value_counts(dropna=False)
  phys_counts[np.NaN]
  phys_counts.hist(bins = 100)
  df['cms_prf_physn_npi_srg_count'] = df['cms_prf_physn_npi_srg'].map(phys_counts)
  df['cms_prf_physn_npi_srg_annual_count'] = df['cms_prf_physn_npi_srg'].map(phys_counts) / 3.0

  #%% org tee rate
  org_tee_counts = df[df['cms_cpt_tee'] == '1']['cms_org_npi_num'].value_counts(dropna=False)
  df['cms_org_npi_tee_count'] = df['cms_org_npi_num'].map(lambda x: org_tee_counts.get(x, 0))
  df['cms_org_npi_tee_rate'] = df['cms_org_npi_tee_count'] / df['cms_org_npi_count']
  df['cms_org_npi_tee_rate'].describe()
  df['cms_org_npi_tee_rate'].hist(bins = 100)

  # divide equally into 4 bins using qcut
  # store 4 bin results
  [df['quantile_org_tee_rate'], bins] = pd.qcut(df['cms_org_npi_tee_rate'], q=4, labels=['bin_1', 'bin_2', 'bin_3', 'bin_4'], retbins=True)
  print(f'org npi rate quartile bins: {bins}')

  # look at the data
  print(df['quantile_org_tee_rate'].value_counts())

  # divide equally into 5 bins using qcut
  # store 5 bin results
  [df['quintile_org_tee_rate'], bins] = pd.qcut(df['cms_org_npi_tee_rate'], q=5, labels=['bin_1', 'bin_2', 'bin_3', 'bin_4', 'bin_5'], retbins=True)
  print(f'org npi rate quintile bins: {bins}')

  # look at the data 
  print(df['quintile_org_tee_rate'].value_counts())
  df['quintile_org_tee_rate'].hist()

  #%% physician tee rate
  phys_tee_counts = df[df['cms_cpt_tee'] == '1']['cms_prf_physn_npi_srg'].value_counts(dropna=False)
  df['cms_prf_physn_npi_srg_tee_count'] = df['cms_prf_physn_npi_srg'].map(lambda x: phys_tee_counts.get(x, 0))
  df['cms_prf_physn_npi_srg_tee_rate'] = df['cms_prf_physn_npi_srg_tee_count'] / df['cms_prf_physn_npi_srg_count']
  df['cms_prf_physn_npi_srg_tee_rate'].describe()
  df['cms_prf_physn_npi_srg_tee_rate'].hist(bins = 100)


# %%
df_c.head(5)
# generate random row sample df
r = df_c
r.sample(n = 10)

# %%
# check data distribution for key columns cms_  
df_c['_merge_aha'].value_counts()
df_c['aha_id'].value_counts() 
df_c['aha_id'].describe()
df_c['aha_admtot'].describe()
df_c['aha_admtot'].hist(bins = 100)
df_c['aha_bdtot'].describe()
df_c['aha_bdtot'].hist(bins = 100)
df_c['aha_fteh'].describe()
df_c['aha_fteh'].hist(bins = 100)
df_c['aha_fte'].describe()
df_c['aha_fte'].hist(bins = 100)
df_c['aha_ftemd'].describe()
df_c['aha_ftemd'].hist(bins = 100)
df_c['aha_suroptot'].describe()
df_c['aha_suroptot'].hist(bins = 100)

# %% 
# check data distribution ahrf_
df_c['ahrf_AHRF_state_county_5_digit'].describe()
df_c['_merge_ahrf'].value_counts()
df_c['ahrf_anes_MD_total_2015'].describe()
df_c['ahrf_anes_MD_total_2015'].value_counts()
df_c['ahrf_anes_MD_total_2015'].hist(bins = 100)
len(df_c[pd.isna(df_c['ahrf_anes_MD_total_2015'])]['ahrf_anes_MD_total_2015'])

df_c['ahrf_anes_MD_total_2010'].describe()
df_c['ahrf_anes_MD_total_2010'].value_counts()
df_c['ahrf_anes_MD_total_2010'].hist(bins = 100)
len(df_c[pd.isna(df_c['ahrf_anes_MD_total_2010'])]['ahrf_anes_MD_total_2010'])

df_c['ahrf_anes_DO_total_2015'].describe()
df_c['ahrf_anes_DO_total_2010'].describe()

df_c['ahrf_anes_CRNA_npi_2015'].describe()
df_c['ahrf_anes_CRNA_npi_2010'].describe()

df_c['ahrf_surg_total_2015'].describe()
df_c['ahrf_surg_total_2015'].hist(bins = 100)

df_c['ahrf_surg_total_2010'].describe()
df_c['ahrf_surg_total_2010'].hist(bins = 100)

df_c['ahrf_thoracic_surgery_2015'].describe()
df_c['ahrf_thoracic_surgery_2015'].hist(bins = 100)

df_c['ahrf_thoracic_surgery_2010'].describe()
df_c['ahrf_thoracic_surgery_2010'].hist(bins = 100)

# %% 
# combine DO and MD anesthesiologists
df_c['ahrf_anes_attd_total_2015'] = df_c['ahrf_anes_DO_total_2015'] + df_c['ahrf_anes_MD_total_2015']
df_c['ahrf_anes_attd_total_2015'].describe()

# %%
# generate random row sample df
r = df_c
r.sample(n = 10)

# %%
df_f = r['cms_valve']
t = df_c_10['aha_mstate']


# %% 
# surgical categorizations
len(df_c)
# create cabg only column
df_c['cms_cabg_only'] = ((df_c['cms_c'] == '1') | (df_c['cms_cabg_s'] == '1')) & ((df_c['cms_v'] != '1') & (df_c['cms_v_valve'] != '1') & (df_c['cms_valve'] != '1') & (df_c['cms_valve_categorized'] == '.'))


# %%
# look at surgery distributions
df_c.filter(regex=("cms_cabg_only")).columns

# create temp dataframe to test column cleaning code
t = df_c.copy()

# look at random sample for data cleaning 
r = t
r.sample(n = 10)

# %%
df_c.filter(regex=("cms")).columns
# list of clean columns columns 
t['cms_bene_id'].value_counts(normalize=True)
t['cms_bene_id'].describe()
t['cms_medpar_id'].value_counts(normalize=True)
t['cms_prvdr_num'].value_counts(normalize=True)
t['cms_drg_cd'].value_counts(normalize=True)
t['cms_drg_ct'].value_counts(normalize=True)
t['cms_drg_ct'].value_counts(normalize=True)
t['cms_t'].value_counts(normalize=True)
t['cms_v'].value_counts(normalize=True)
t['cms_c'].value_counts(normalize=True)
t['cms_cabg_only'].value_counts(normalize=True)
t['cms_aortic_repair'].value_counts(normalize=True)
t['cms_aortic_replace'].value_counts(normalize=True)
t['cms_mitral_repair'].value_counts(normalize=True)
t['cms_mitral_replace'].value_counts(normalize=True)
t['cms_pulmonic_repair'].value_counts(normalize=True)
t['cms_pulmonic_replace'].value_counts(normalize=True)
t['cms_tricuspid_repair'].value_counts(normalize=True)
t['cms_tricuspid_replace'].value_counts(normalize=True)
t['cms_hv_repair_unspecified'].value_counts(normalize=True)
t['cms_hv_replace_unspecified'].value_counts(normalize=True)
t['cms_valve_plus_cabg'].value_counts(normalize=True)
t['cms_age_cnt'].value_counts(normalize=True)
t['cms_yr'].value_counts(normalize=True)
t['cms_admsndt_date'].describe(datetime_is_numeric=True)
t['cms_dschrgdt_date'].describe(datetime_is_numeric=True)
t['cms_bene_dob_denom_auto_date'].describe(datetime_is_numeric=True)
t['cms_clm_thru_dt_srg_date'].describe(datetime_is_numeric=True)
t['cms_clm_thru_dt_tee_date'].describe(datetime_is_numeric=True)
t['cms_admit_type'].value_counts(normalize=True)
t['cms_geographic'].value_counts(normalize=True)
t['cms_cnty_cd'].value_counts(normalize=True)
t['cms_cnty_cd'].describe()
t['cms_state_cd'].value_counts(normalize=True)
t['cms_state_cd'].describe()
t['cms_bene_zip'].value_counts(normalize=True)
t['cms_cov_to_srg'].describe()
t['cms_sex_str'].value_counts(normalize=True)
t['cms_race_str'].value_counts(normalize=True)
t['cms_prf_physn_npi_srg'].value_counts(normalize=True, dropna=False)
t['cms_prf_physn_npi_tee'].value_counts(normalize=True, dropna=False)
t['cms_org_npi_num_medpar'].value_counts(normalize=True, dropna=False)
t['cms_cpt_tee_str'].value_counts(normalize=True, dropna=False)
t['cms_cpt_tee'].value_counts(normalize=True, dropna=False)
t[t['cms_tee'] == '1']['cms_tee_provider'].value_counts(normalize=True)
t['cms_cpt_cv'].value_counts(normalize=True, dropna=False)
t['cms_alcohol_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_alcohol_poa'].value_counts(normalize=True, dropna=False)
t['cms_arrhythmia_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_arrhythmia_poa'].value_counts(normalize=True, dropna=False)
t['cms_blood_loss_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_blood_loss_poa'].value_counts(normalize=True, dropna=False)
t['cms_chf_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_chf_poa'].value_counts(normalize=True, dropna=False)
t['cms_coagulopathy_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_coagulopathy_poa'].value_counts(normalize=True, dropna=False)
t['cms_cpd_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_cpd_poa'].value_counts(normalize=True, dropna=False)
t['cms_anemia_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_anemia_poa'].value_counts(normalize=True, dropna=False)
t['cms_depression_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_depression_poa'].value_counts(normalize=True, dropna=False)
t['cms_diabetes_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_diabetes_poa'].value_counts(normalize=True, dropna=False)
t['cms_diabetes_cx_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_diabetes_cx_poa'].value_counts(normalize=True, dropna=False)
t['cms_diabetes_all_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_diabetes_all_poa'].value_counts(normalize=True, dropna=False)
t['cms_electrolytes_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_electrolytes_poa'].value_counts(normalize=True, dropna=False)
t['cms_htn_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_htn_poa'].value_counts(normalize=True, dropna=False)
t['cms_htn_cx_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_htn_cx_poa'].value_counts(normalize=True, dropna=False)
t['cms_htn_all_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_htn_all_poa'].value_counts(normalize=True, dropna=False)
t['cms_hypothyroid_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_hypothyroid_poa'].value_counts(normalize=True, dropna=False)
t['cms_liver_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_liver_poa'].value_counts(normalize=True, dropna=False)
t['cms_lymphoma_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_lymphoma_poa'].value_counts(normalize=True, dropna=False)
t['cms_metastasis_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_metastasis_poa'].value_counts(normalize=True, dropna=False)
t['cms_neuro_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_neuro_poa'].value_counts(normalize=True, dropna=False)
t['cms_obesity_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_obesity_poa'].value_counts(normalize=True, dropna=False)
t['cms_paralysis_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_paralysis_poa'].value_counts(normalize=True, dropna=False)
t['cms_psychosis_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_psychosis_poa'].value_counts(normalize=True, dropna=False)
t['cms_pulm_circ_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_pulm_circ_poa'].value_counts(normalize=True, dropna=False)
t['cms_pvd_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_pvd_poa'].value_counts(normalize=True, dropna=False)
t['cms_renal_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_renal_poa'].value_counts(normalize=True, dropna=False)
t['cms_rheumatoid_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_rheumatoid_poa'].value_counts(normalize=True, dropna=False)
t['cms_valve_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_valve_poa'].value_counts(normalize=True, dropna=False)
t['cms_weight_loss_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_weight_loss_poa'].value_counts(normalize=True, dropna=False)
t['cms_angina_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_angina_poa'].value_counts(normalize=True, dropna=False)
t['cms_solid_tumor_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_solid_tumor_poa'].value_counts(normalize=True, dropna=False)
t['cms_stroke_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_stroke_poa'].value_counts(normalize=True, dropna=False)
t['cms_esophageal_6_preexist'].value_counts(normalize=True, dropna=False)
t['cms_esophageal_poa'].value_counts(normalize=True, dropna=False)
t['cms_hcpcs_cd_srg'].value_counts(normalize=True, dropna=False)
t['cms_hcpcs_cd_srg'].value_counts(dropna=False)

# %%
# generate random row sample df
r = t
r.sample(n = 10)

# %%
df_c.filter(regex=("aha")).columns
# list of clean columns columns 
t['aha_id'].value_counts(normalize=True)
t['aha_id'].describe()
t['aha_mname'].value_counts(normalize=True)
t['aha_cntyname'].value_counts(normalize=True)
t['aha_mlocaddr'].value_counts(normalize=True)
t['aha_mloccity'].value_counts(normalize=True)
t['aha_mloccity'].value_counts(normalize=True)
t['aha_mtype'].value_counts(normalize=True)
t['aha_hospbd'].describe()
t['aha_mloczip_5'].value_counts(normalize=True)
t['aha_mloczip_5'].describe()
t['aha_bdtot'].describe()
t['aha_admtot'].describe()
t['aha_ipdtot'].describe()
t['aha_mcrdc'].describe()
t['aha_mcripd'].describe()
t['aha_suropip'].describe()
t['aha_suropop'].describe()
t['aha_suroptot'].describe()
t['aha_vem'].describe()
t['aha_paytot'].describe()
t['aha_npayben'].describe()
t['aha_exptot'].describe()
t['aha_ftmdtf'].describe()
t['aha_ftres'].describe()
t['aha_fttran84'].describe()
t['aha_ftrntf'].describe()
t['aha_ftlpntf'].describe()
t['aha_ftast'].describe()
t['aha_ftothtf'].describe()
t['aha_fttot'].describe()
t['aha_mlocstcd'].value_counts(normalize=True)
t['aha_mlocstcd'].describe()
t['aha_area'].value_counts(normalize=True)
t['aha_area'].describe()
t['aha_adc'].describe()
t['aha_adjadm'].describe()
t['aha_adjpd'].describe()
t['aha_adjadc'].describe()
t['aha_ftemd'].describe()
t['aha_ftern'].describe()
t['aha_ftelpn'].describe()
t['aha_fteres'].describe()
t['aha_ftetran'].describe()
t['aha_fteh'].describe()
t['aha_fte'].describe()
t['aha_fcounty'].value_counts(normalize=True)
t['aha_fstcd'].value_counts(normalize=True)
t['aha_fcntycd'].value_counts(normalize=True)
t['aha_mapp1_jc_accred'].value_counts(normalize=True)
t['aha_mapp2_acs_cancer'].value_counts(normalize=True)
t['aha_mapp3_acgme'].value_counts(normalize=True)
t['aha_mapp5_med_sch'].value_counts(normalize=True)
t['aha_mapp7_carf'].value_counts(normalize=True)
t['aha_mapp8_coth'].value_counts(normalize=True)
t['aha_mapp10_cms_cert'].value_counts(normalize=True)
t['aha_mapp11_hfap_accred'].value_counts(normalize=True)
t['aha_mapp12_aoa_intern'].value_counts(normalize=True)
t['aha_mapp13_aoa_res'].value_counts(normalize=True)
t['aha_mapp16_catholic_op'].value_counts(normalize=True)
t['aha_mapp18_critical_access'].value_counts(normalize=True)
t['aha_mapp19_rural_ref'].value_counts(normalize=True)
t['aha_mapp20_sole_prov'].value_counts(normalize=True)
t['aha_mapp21_dnv_accred'].value_counts(normalize=True)
t['aha_mapp22_ahrq_accred'].value_counts(normalize=True)
t['aha_mstate'].value_counts(normalize=True)
t['aha_lat'].describe()
t['aha_long'].describe()
t['aha_long'].describe()

# %%
# list of clean columns columns 
t['ahrf_AHRF_county_3_digit'].value_counts()
t['ahrf_AHRF_state_2_digit'].value_counts()
t['ahrf_AHRF_county_name'].value_counts()
t['ahrf_AHRF_state_county_5_digit'].value_counts()
t['ahrf_AHRF_state'].value_counts()
t['ahrf_AHRF_state_abbrev'].value_counts()
t['ahrf_AHRF_census_region_code'].value_counts()
t['ahrf_AHRF_census_region_name'].value_counts()
t['ahrf_AHRF_census_division_code'].value_counts()
t['ahrf_AHRF_census_division_name'].value_counts()
t['ahrf_anes_MD_total_2015'].describe()
t['ahrf_anes_MD_total_2010'].describe()
t['ahrf_anes_DO_total_2015'].describe()
t['ahrf_anes_DO_total_2010'].describe()
t['ahrf_anes_CRNA_npi_2015'].describe()
t['ahrf_anes_CRNA_npi_2010'].describe()
t['ahrf_surg_total_2015'].describe()
t['ahrf_surg_total_2010'].describe()
t['ahrf_thoracic_surgery_2015'].describe()
t['ahrf_thoracic_surgery_2010'].describe()
t['ahrf_anes_attd_total_2015'].describe()

# %%
# list of clean columns columns 
t['geo_zip_bene'].describe()
t['cms_bene_zip'].describe()
t['geo_latitude_bene'].describe()
t['geo_longitude_bene'].describe()

t['geo_zip_aha'].describe()
t['aha_mloczip_5'].describe()
t['geo_latitude_aha'].describe()
t['geo_longitude_aha'].describe()

t[pd.isna(t['geo_latitude_bene'])].shape
t[pd.isna(t['geo_longitude_bene'])].shape

t[pd.isna(t['geo_latitude_aha'])].shape
t[pd.isna(t['geo_longitude_aha'])].shape

#%%
def calculate_km (row):
  try:
    if pd.isna(row['geo_latitude_bene']) | pd.isna(row['geo_latitude_aha']):
      return float('nan')
    
    return distance.distance(
      [row['geo_latitude_bene'], row['geo_longitude_bene']],
      [row['geo_latitude_aha'], row['geo_longitude_aha']]
    ).km

  except:
    print('Error for row:', row['geo_latitude_bene'], row['geo_longitude_bene'], row['geo_latitude_aha'], row['geo_longitude_aha'])
    raise

#%%
t['linear_distance_km'] = t.apply(lambda row: calculate_km(row) , axis=1)

# %%
# conversion factor km to miles 0.621371
t['linear_distance_miles'] = 0.621371 * t['linear_distance_km']

# %%
# check 
t[pd.isna(t['linear_distance_km'])].shape
# extreme example
t[(t['linear_distance_km'] > 16649.916000) & (t['linear_distance_km'] < 16649.918000)]

# %%
t.head()

t['cms_cabg_only'].value_counts(normalize = True)


#%% define indicator variable
t['model_indicator'] = np.select(
  condlist=[(t['cms_v'] == '1') & (t['cms_cabg_only'] == False), (t['cms_t'] == '1') & (t['cms_cabg_only'] == True)],
  choicelist=['model_valve', 'model_cab'],
  default='model_neither'
)
t['model_indicator'].value_counts(normalize=True, dropna=False)

# %% 
# a) df for model 1: valves | valve + CABG (2009 - 2015)
df_v = t[t['model_indicator'] == 'model_valve'].copy()
calculate_rates(df_v)
# look at key column(s)
df_v['cms_cpt_tee'].value_counts(normalize = True)

# %% 
# b) df for model 2: CABG only (2013 - 2015) 
df_cab = t[t['model_indicator'] == 'model_cab'].copy()
calculate_rates(df_cab)
# look at key column(s)
df_cab[df_cab['cms_cpt_cv'] == '1']['cms_cpt_tee'].value_counts(normalize = True)

# %% 
# save to parquet file
df_v.to_parquet(dirname / f'../data/data_raw_valve.parquet', engine='pyarrow')

# save to csv file
df_v.to_csv(
  dirname / f'../data/data_raw_valve.csv', 
  index=False
)

# %% 
df_cab.to_parquet(dirname / f'../data/data_raw_cabg.parquet', engine='pyarrow')

# %%
df_cab.to_csv(
  dirname / f'../data/data_raw_cabg.csv', 
  index=False
)

# %%
calculate_rates(t)
t.to_csv(
  dirname / f'../data/data_visualization.csv',
  index=False
)

# %%
t.to_csv(
  dirname / f'../data/data_clean.csv',
  index=False
)



# %%
