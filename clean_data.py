#%% imports
import re
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer


#%% constants
dirname = pathlib.Path(__file__).resolve().parent
pd.set_option("display.max_columns", None)
pd.set_option("display.min_rows", 100)
pd.set_option("display.max_rows", 100)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Inter'

SMALL_SIZE = 24
MEDIUM_SIZE = 30
LARGE_SIZE = 36

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=LARGE_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize

colors = {
  'light_gray': '#bcbcbc',
  'dark_gray': '#858585',
  'blue': '#2196f3',
  'red': '#e57373',
  'orange': '#f9a825',
}

# options
data_set_option = 'cabg'
# data_set_option = 'valve'
data_set_path = f'../../data/data_raw_{data_set_option}.parquet'
output_path_variables = f'../../data/variables_{data_set_option}.csv'
output_path_coeffs = f'../../data/coeffs_{data_set_option}.csv'
output_path_numerical_data = f'../../data/numerical_data_{data_set_option}.csv'
save_figures = False

#%% load data
raw_data_orig = pd.read_parquet(dirname / data_set_path)

# do not impute additional columns because it is used by later code
do_not_impute = [
  'cms_prf_physn_npi_srg_count',
  'cms_org_npi_tee_rate',
  'cms_prf_physn_npi_srg_tee_rate',
  'cms_prf_physn_npi_srg',  'cms_org_npi_num_medpar',
  'cms_prf_physn_npi_srg_annual_count',
]

# known output 
y = raw_data_orig['cms_tee'].copy().astype('int64')

# excluded columns
columns_to_exclude = [
  'aha_year', 'aha_los', 'cms_loh', 'cms_log_loh', 'cms_tee', 'cms_cpt_tee_str', 'cms_cpt_tee', 'cms_prvdr_perform_tee', 'cms_c', 'cms_valve_s', 'cms_sex', 'cms_race_medpar', 'cms_deathcd', 'cms_dschrgcd', 'cms_betos_cd_tee', 'aha_mtype',
  'aha_eadmh', 'aha_eipdh', 'aha_commty', 'cms_race', 'ahrf_AHRF_census_region_code',  'aha_bsc', 'aha_eadmtot', 'aha_eipdtot', 'aha_cluster', 'aha_rurlven', 'aha_mapp18_critical_access', 'aha_mapp22_ahrq_accred',
  'geo_latitude_bene', 'geo_longitude_bene', 'linear_distance_km', 'geo_longitude_aha', 'geo_latitude_aha', 'cms_tee_provider',
  'cms_surgery_c', 'quantile_org_tee_rate', 'quintile_org_tee_rate',
  'cms_cpt_cv', 'ahrf_AHRF_census_region_name', 'ahrf_AHRF_census_division_code',
  'cms_prf_physn_npi_srg_tee_count', 'cms_org_npi_tee_count', 'cms_cabg_only', 'aha_suropop',
  # drop because there are aggregated fields to use instead
  'ahrf_anes_MD_total_2010', 'ahrf_anes_DO_total_2010',
  'ahrf_anes_MD_total_2015', 'ahrf_anes_DO_total_2015',
   # drop because they are outcomes
  'aha_los', 'cms_loh', 'cms_log_loh', 'cms_esophageal_perf', 'cms_acute_stroke',
   # drop because it is captured by state
  'ahrf_AHRF_census_division_name',
  # drop these because, although they make the prediction much better, they aren't really useful for explaining patterns
  # 'cms_prf_physn_npi_srg_tee_rate', 'cms_org_npi_tee_rate'
]
if data_set_option == 'cabg':
  columns_to_exclude = columns_to_exclude + [
    'cms_v', 'cms_surgery_v', 'cms_valve', 'cms_v_valve', 'cms_aortic_repair',
    'cms_aortic_replace', 'cms_mitral_repair', 'cms_mitral_replace', 'cms_pulmonic_replace',
    'cms_tricuspid_repair', 'cms_tricuspid_replace', 'cms_hv_repair_unspecified', 'cms_hv_replace_unspecified',
    'cms_valve_plus_cabg', 'cms_valve_categorized'
  ]

raw_data = raw_data_orig.drop(columns_to_exclude, axis=1)

#%% create state categorical column
raw_data['state'] = raw_data['aha_mstate']

#%% filter numerical columns
all_num_columns = raw_data.select_dtypes(['number']).columns
num_columns = all_num_columns.drop(['cms_yr'])
print(f'there are {len(num_columns)} total numerical columns: \n', num_columns)

#%% filter binary columns

binary_columns = []
for column in raw_data.columns:
  value_counts = len(raw_data[column].value_counts(dropna=False))
  dtype = raw_data[column].dtype
  if re.match('.*_dgns_.*|.*_hcpcs_.*|.*geo.*|.*death.*|^aha_mapp\d+$', column): continue
  if column in columns_to_exclude: continue
  if value_counts == 2 and dtype in ['object', pd.CategoricalDtype, 'bool']:
    binary_columns.append(column)

print(f'there are {len(binary_columns)} total binary columns: \n', binary_columns)

#%% filter categorical columns

categorical_columns = []
for column in raw_data.columns:
  value_counts = len(raw_data[column].value_counts(dropna=False))
  dtype = raw_data[column].dtype
  if re.match('.*_dgns_.*|.*_hcpcs_.*|.*geo.*|.*death.*|^aha_mapp\d+$', column): continue
  if column in columns_to_exclude: continue
  if value_counts > 2 and (value_counts < 10 or column == 'state') and dtype in ['object', pd.CategoricalDtype, 'bool', 'int64']:
    categorical_columns.append(column)

print(f'there are {len(categorical_columns)} total categorical columns: \n', categorical_columns)

#%% table of "final" variables
variables = pd.DataFrame(data={
  'column': num_columns.to_list() + binary_columns + categorical_columns
})
variables[['column']].to_csv(dirname / output_path_variables, index=False, header=False)

#%% set up data processing pipeline

num_pipeline = Pipeline([
  ('median_imputer', SimpleImputer(strategy='median')),
])

binary_pipeline = Pipeline([
  ('categorize', OneHotEncoder(drop='first', sparse=False))
])

categorical_pipeline = Pipeline([
  ('categorize', OneHotEncoder(drop=None, sparse=False)),
  ('select_k_best', SelectKBest(chi2, k='all'))
])

passthrough_pipeline = Pipeline([
  ('passthrough', FunctionTransformer(lambda x: x))
])

column_transformer = ColumnTransformer([
  ('number', num_pipeline, np.setdiff1d(num_columns, do_not_impute)),
  ('passthrough', passthrough_pipeline, do_not_impute),
  ('binary', binary_pipeline, binary_columns),
  ('categorical', categorical_pipeline, categorical_columns)
], sparse_threshold=0, remainder='drop')

column_transformer.fit(raw_data, y)

#%% describe the selected category columns
selected_category_indices = column_transformer.named_transformers_['categorical'].named_steps['select_k_best'].get_support()
categories = column_transformer.named_transformers_['categorical'].named_steps['categorize'].get_feature_names(categorical_columns)
selected_categories = categories[selected_category_indices]
print(f'selected {len(selected_categories)} out of {len(categories)} categories are: \n {selected_categories}')

#%% export the transformed data
columns = np.append(
  np.append(
    np.append(
      np.array(np.setdiff1d(num_columns, do_not_impute)),
      do_not_impute
    ),
    binary_columns
  ),
  selected_categories
)
transformed_data = pd.DataFrame(column_transformer.transform(raw_data), columns=columns)
transformed_data['cms_cpt_tee'] = y.values
transformed_data.to_csv(dirname / output_path_numerical_data, index=False)

#%% filter out observations
data = raw_data[~pd.isna(raw_data['cms_prf_physn_npi_srg'])].copy()

n_bins = 50

#%% plot 2d histogram
fig = plt.figure(figsize=(19, 15))
ax = fig.add_subplot(1, 1, 1)
sns.histplot(
  data=data,
  x='cms_org_npi_tee_rate',
  y='cms_prf_physn_npi_srg_tee_rate',
  cbar=True,
  stat='percent',
  bins=n_bins,
  cbar_kws={ 'label': 'Percent of total' }
)

plt.xticks([0, 0.25, 0.5, 0.75, 1.0])
plt.xlim([0, 1])
plt.xlabel('Probability of TEE by Hospital')

plt.xticks([0, 0.25, 0.5, 0.75, 1.0])
plt.ylim([0, 1])
plt.xlabel('Probability of TEE by Physician')

if save_figures:
  plt.savefig(dirname / f'../../figures/org_and_phys_tee_rate_{data_set_option}.png', bbox_inches='tight', dpi=300, format='png')
plt.show()

#%% overall histogram
fig = plt.figure(figsize=(19, 15))
ax = fig.add_subplot(1, 1, 1)
values, _bins, _patches = plt.hist(
  data['cms_org_npi_tee_rate'],
  bins=n_bins,
  color=colors['dark_gray'],
  rwidth=0.9,
)

ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))
plt.xlim(-.01, 1.01)
plt.xlabel('Probability of TEE by Hospital')

values_sum, values_max = values.sum(), values.max()
n_ticks = np.ceil(values_max / values_sum * 100)
y_ticks = np.linspace(0, n_ticks, np.int_(n_ticks+1)) * values_sum / 100
if y_ticks.size > 10:
  y_ticks = y_ticks[0::2]
y_max = n_ticks * values_sum / 100

ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=values_sum))
plt.yticks(y_ticks)
plt.ylim(0, y_max)
plt.ylabel('Percent of total')

if save_figures:
  plt.savefig(dirname / f'../../figures/org_npi_tee_rate_{data_set_option}.png', bbox_inches='tight', dpi=300, format='png')
plt.show()

#%% individual combined histograms
fig = plt.figure(figsize=(19, 15))
ax = fig.add_subplot(3, 1, 1)
plt.hist(
  data['cms_org_npi_tee_rate'],
  bins=n_bins,
  weights=data['anesthesiologist_tee_ratio'],
  color=colors['blue'],
  rwidth=0.9,
)

ax.xaxis.set_visible(False)
plt.xlim(-.01, 1.01)

ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=values_sum))
plt.yticks(y_ticks)
plt.ylim(0, y_max)
plt.ylabel('Cardiologist freq.', size=SMALL_SIZE)

ax = fig.add_subplot(3, 1, 2)
plt.hist(
  data['cms_org_npi_tee_rate'],
  bins=n_bins,
  weights=data['cardiologist_tee_ratio'],
  color=colors['orange'],
  rwidth=0.9,
)

ax.xaxis.set_visible(False)
plt.xlim(-.01, 1.01)

ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=values_sum))
plt.yticks(y_ticks)
plt.ylim(0, y_max)
plt.ylabel('Anesthesiologist freq.', size=SMALL_SIZE)

ax = fig.add_subplot(3, 1, 3)
plt.hist(
  data['cms_org_npi_tee_rate'],
  bins=n_bins,
  weights=1 - (data['cardiologist_tee_ratio'] + data['anesthesiologist_tee_ratio']),
  color=colors['light_gray'],
  rwidth=0.9,
)

plt.xticks([0, 0.25, 0.5, 0.75, 1.0])
plt.xlim(-.01, 1.01)
plt.xlabel('Probability of TEE by Hospital')

ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=values_sum))
plt.yticks(y_ticks)
plt.ylim(0, y_max)
plt.ylabel('Mixed freq.', size=SMALL_SIZE)

if save_figures:
  plt.savefig(dirname / f'../../figures/org_npi_tee_rate_2_{data_set_option}.png', bbox_inches='tight', dpi=300, format='png')
  plt.savefig(dirname / f'../../figures/org_npi_tee_rate_2_{data_set_option}.svg', bbox_inches='tight', dpi=300, format='svg')

plt.show()

#%% stacked histogram
fig = plt.figure(figsize=(19, 15))
ax = fig.add_subplot(1, 1, 1)
plt.hist(
  [
    data['cms_org_npi_tee_rate'],
    data['cms_org_npi_tee_rate'],
    data['cms_org_npi_tee_rate'],
  ],
  bins=n_bins,
  weights=[
    1 - (data['cardiologist_tee_ratio'] + data['anesthesiologist_tee_ratio']),
    data['cardiologist_tee_ratio'],
    data['anesthesiologist_tee_ratio'],
  ],
  histtype='barstacked',
  label=['Other provider', 'Cardiologist', 'Anesthesiologist'],
  color=[
    colors['light_gray'],
    colors['orange'],
    colors['blue'],
  ],
  rwidth=0.9,
)

plt.xticks([0, 0.25, 0.5, 0.75, 1.0])
plt.xlim(-.01, 1.01)
plt.xlabel('Probability of TEE by Hospital')

ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=values_sum))
plt.yticks(y_ticks)
plt.ylim(0, y_max)
plt.ylabel('Percent of total')

# reorder legend
handles, labels = plt.gca().get_legend_handles_labels()
order = [2, 1, 0]
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order])

if save_figures:
  plt.savefig(dirname / f'../../figures/org_npi_tee_rate_3_{data_set_option}.png', bbox_inches='tight', dpi=300, format='png')
  plt.savefig(dirname / f'../../figures/org_npi_tee_rate_3_{data_set_option}.svg', bbox_inches='tight', dpi=300, format='svg')
plt.show()
