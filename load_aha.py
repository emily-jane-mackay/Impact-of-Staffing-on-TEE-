# %%
import pathlib
import pandas as pd
import numpy as np
dirname = pathlib.Path(__file__).resolve().parent

# %%
# load data file (with headers)
# & save as dataframe (label convention "df_")
in_file = dirname / f'../data/AHA_2009_2017_a.csv'
df_aha = pd.read_csv(
  in_file,
  dtype=str,
  index_col=False
)
column_names_aha = df_aha.columns.values

# %%
# row count
len(df_aha.index)
# column count 
len(df_aha.columns.values)
# show columns
print(df_aha.columns)

# %%
# set option to display all columns
pd.set_option("display.max_columns", None)
# set option to display rows (set to 100)
# note: must set minimum and maximum
pd.set_option("display.min_rows", 100)
pd.set_option("display.max_rows", 100)

# %%
# look at first five rows
df_aha.head()
# look at last five rows
df_aha.tail()

# %%
# display all columns 
print(df_aha.columns.tolist())

# %%
df_aha['mcrnum'].value_counts()

# %%
# Boolean logic to filter rows without a 6-digit mcrnums 
# Boolean logic to filter out NaN requires a function: ~pd.isna
df_aha_filtered = df_aha[~pd.isna(df_aha['mcrnum'])]
df_aha_filtered.head(100)

# %% 
# display all columns containing " " 
df_aha_filtered.filter(regex=("mcrnum")).columns


# %% 
# visualize dataframe with selected columns
df_aha_filtered[[
  'ID', 'STCD', 'YEAR', 
  'mcrnum', 'mname', 'CNTYNAME', 
  'MADMIN', 'MLOCADDR', 'MLOCCITY', 
  'MTYPE', 'HOSPBD', 'MLOCZIP',
  'BDTOT', 'ADMTOT', 'IPDTOT', 
  'MCRDC', 'MCRIPD', 'MCDDC', 
  'MCDIPD', 'SUROPIP', 
  'SUROPOP', 'SUROPTOT', 
  'VEM', 'PAYTOT', 'NPAYBEN', 
  'EXPTOT', 'FTMDTF', 'FTRES', 
  'FTTRAN84', 'FTRNTF', 'FTLPNTF', 
  'FTAST', 'FTOTHTF', 'FTTOT', 
  'MLOCSTCD', 'AREA', 
  'BSC', 'LOS', 'ADC', 
  'ADJADM', 'ADJPD', 'ADJADC', 
  'FTEMD', 'FTERN', 'FTELPN', 
  'FTERES', 'FTETRAN', 'FTETTRN', 
  'FTEOTH94', 'FTEH', 'FTENH', 
  'FTE', 'MCNTYCD', 'FCOUNTY', 
  'FSTCD', 'FCNTYCD', 'MAPP1', 
  'MAPP2', 'MAPP3', 'MAPP5', 
  'MAPP6', 'MAPP7', 'MAPP8', 
  'MAPP9', 'MAPP10', 'MAPP11', 
  'MAPP12', 'MAPP13', 'MAPP16', 
  'MAPP17', 'EADMTOT', 'EIPDTOT', 
  'EADMH', 'EIPDH', 'MSTATE', 
  'SYSLNAME', 'COMMTY', 'HCFAID', 
  'LAT', 'LONG', 'CLUSTER', 
  'NETPHONE', 'TELNO', 
  'NPINUM', 'MAPP18', 
  'MAPP19', 'MAPP20', 'MAPP21', 
  'RURLVEN', 'CSANAME', 'CSACODE', 
  'MAPP22', 
]].copy()
  

# %%
# note: must be a copy if data manipulation is planned
z = df_aha_filtered[[
  'ID', 'STCD', 'YEAR', 
  'mcrnum', 'mname', 'CNTYNAME', 
  'MADMIN', 'MLOCADDR', 'MLOCCITY', 
  'MTYPE', 'HOSPBD', 'MLOCZIP',
  'BDTOT', 'ADMTOT', 'IPDTOT', 
  'MCRDC', 'MCRIPD', 'MCDDC', 
  'MCDIPD', 'SUROPIP', 
  'SUROPOP', 'SUROPTOT', 
  'VEM', 'PAYTOT', 'NPAYBEN', 
  'EXPTOT', 'FTMDTF', 'FTRES', 
  'FTTRAN84', 'FTRNTF', 'FTLPNTF', 
  'FTAST', 'FTOTHTF', 'FTTOT', 
  'MLOCSTCD', 'AREA', 
  'BSC', 'LOS', 'ADC', 
  'ADJADM', 'ADJPD', 'ADJADC', 
  'FTEMD', 'FTERN', 'FTELPN', 
  'FTERES', 'FTETRAN', 'FTETTRN', 
  'FTEOTH94', 'FTEH', 'FTENH', 
  'FTE', 'MCNTYCD', 'FCOUNTY', 
  'FSTCD', 'FCNTYCD', 'MAPP1', 
  'MAPP2', 'MAPP3', 'MAPP5', 
  'MAPP6', 'MAPP7', 'MAPP8', 
  'MAPP9', 'MAPP10', 'MAPP11', 
  'MAPP12', 'MAPP13', 'MAPP16', 
  'MAPP17', 'EADMTOT', 'EIPDTOT', 
  'EADMH', 'EIPDH', 'MSTATE', 
  'SYSLNAME', 'COMMTY', 'HCFAID', 
  'LAT', 'LONG', 'CLUSTER', 
  'NETPHONE', 'TELNO', 
  'NPINUM', 'MAPP18', 
  'MAPP19', 'MAPP20', 'MAPP21', 
  'RURLVEN', 'CSANAME', 'CSACODE', 
  'MAPP22', 
]].copy()

# %%
# add column name prefix
z = z.add_prefix('aha_')

# convert column labels to lower-case 
z.rename(columns=lambda x: x.lower(), inplace=True)

# %%
# check for duplicated columns (sanity check) 
z.columns.value_counts()


# %%
# random sample 
r = z 
z.sample(n=50)

# %%
# add leading zeros  
# check
z['aha_mcrnum'].value_counts()

# %% 
# add leading zeros
z['aha_mcrnum'] = z['aha_mcrnum'].apply(lambda x: '{0:0>6}'.format(x)) 
z['aha_fcounty'] = z['aha_fcounty'].apply(lambda x: '{0:0>5}'.format(x)) 
z['aha_fstcd'] = z['aha_fstcd'].apply(lambda x: '{0:0>2}'.format(x)) 
z['aha_fcntycd'] = z['aha_fcntycd'].apply(lambda x: '{0:0>3}'.format(x)) 

# check
r = z 
z.sample(n=10)

# %%
# convert to strings to numbers prior to sort
z['aha_admtot'] = pd.to_numeric(z['aha_admtot'])
z['aha_bdtot'] = pd.to_numeric(z['aha_bdtot'])
z['aha_suropop'] = pd.to_numeric(z['aha_suropop'])
z['aha_suropip'] = pd.to_numeric(z['aha_suropip'])
z['aha_suroptot'] = pd.to_numeric(z['aha_suroptot'])
z['aha_ftrntf'] = pd.to_numeric(z['aha_ftrntf'])
z['aha_vem'] = pd.to_numeric(z['aha_vem'])
z['aha_adc'] = pd.to_numeric(z['aha_adc'])
z['aha_fteh'] = pd.to_numeric(z['aha_fteh'])
z['aha_fte'] = pd.to_numeric(z['aha_fte'])
z['aha_ftemd'] = pd.to_numeric(z['aha_ftemd'])
z['aha_ftemd'] = pd.to_numeric(z['aha_ftemd'])
z['aha_fteres'] = pd.to_numeric(z['aha_fteres'])
z['aha_ftettrn'] = pd.to_numeric(z['aha_ftettrn'])
z['aha_suroptot'] = pd.to_numeric(z['aha_suroptot'])
z['aha_hospbd'] = pd.to_numeric(z['aha_hospbd'])
z['aha_exptot'] = pd.to_numeric(z['aha_exptot'])
z['aha_suropip'] = pd.to_numeric(z['aha_suropip'])
z['aha_vem'] = pd.to_numeric(z['aha_vem'])
z['aha_ftmdtf'] = pd.to_numeric(z['aha_ftmdtf'])
z['aha_ftres'] = pd.to_numeric(z['aha_ftres'])
z['aha_ftrntf'] = pd.to_numeric(z['aha_ftrntf'])
z['aha_adc'] = pd.to_numeric(z['aha_adc'])
z['aha_fttran84'] = pd.to_numeric(z['aha_fttran84'])
z['aha_ftlpntf'] = pd.to_numeric(z['aha_ftlpntf'])
z['aha_ftast'] = pd.to_numeric(z['aha_ftast'])
z['aha_ftothtf'] = pd.to_numeric(z['aha_ftothtf'])
z['aha_fttot'] = pd.to_numeric(z['aha_fttot'])
z['aha_los'] = pd.to_numeric(z['aha_los'])
z['aha_adjadm'] = pd.to_numeric(z['aha_adjadm'])
z['aha_adjpd'] = pd.to_numeric(z['aha_adjpd'])
z['aha_adjadc'] = pd.to_numeric(z['aha_adjadc'])
z['aha_ftern'] = pd.to_numeric(z['aha_ftern'])
z['aha_ftelpn'] = pd.to_numeric(z['aha_ftelpn'])
z['aha_ftetran'] = pd.to_numeric(z['aha_ftetran'])

# %%
# label variable(s)
z['aha_mtype_labeled'] = z['aha_mtype']
z['aha_mtype_labeled'] = np.select(
  condlist=[z['aha_mtype'] == 'Y', z['aha_mtype'] == 'N'],
  choicelist=['aha registered', 'not aha registered'],
  default='missing',
)

z['aha_mapp1_jc_accred'] = z['aha_mapp1']
z['aha_mapp1_jc_accred'] = np.select(
  condlist = [z['aha_mapp1_jc_accred'] == '1', z['aha_mapp1_jc_accred'] == '2'],
  choicelist = ['jc accredited', 'jc not accredited'],
  default = 'missing', 
)

z['aha_mapp2_acs_cancer'] = z['aha_mapp2']
z['aha_mapp2_acs_cancer'] = np.select(
  condlist = [z['aha_mapp2_acs_cancer'] == '1', z['aha_mapp2_acs_cancer'] == '2'],
  choicelist = ['acs certified', 'not acs certified'],
  default = 'missing', 
)

z['aha_mapp3_acgme'] = z['aha_mapp3']
z['aha_mapp3_acgme'] = np.select(
  condlist = [z['aha_mapp3_acgme'] == '1', z['aha_mapp3_acgme'] == '2'],
  choicelist = ['acgme', 'not acgme'],
  default = 'missing', 
)

z['aha_mapp5_med_sch'] = z['aha_mapp5']
z['aha_mapp5_med_sch'] = np.select(
  condlist = [z['aha_mapp5_med_sch'] == '1', z['aha_mapp5_med_sch'] == '2'],
  choicelist = ['med school affil', 'no med school affil'],
  default = 'missing', 
)

z['aha_mapp7_carf'] = z['aha_mapp7']
z['aha_mapp7_carf'] = np.select(
  condlist = [z['aha_mapp7_carf'] == '1', z['aha_mapp7_carf'] == '2'],
  choicelist = ['carf accredited', 'not carf accredited'],
  default = 'missing', 
)

z['aha_mapp8_coth'] = z['aha_mapp8']
z['aha_mapp8_coth'] = np.select(
  condlist = [z['aha_mapp8_coth'] == '1', z['aha_mapp8_coth'] == '2'],
  choicelist = ['coth member', 'not coth member'],
  default = 'missing', 
)

z['aha_mapp10_cms_cert'] = z['aha_mapp10']
z['aha_mapp10_cms_cert'] = np.select(
  condlist = [z['aha_mapp10_cms_cert'] == '1', z['aha_mapp10_cms_cert'] == '2'],
  choicelist = ['cms cert', 'no cms cert'],
  default = 'missing', 
)

z['aha_mapp11_hfap_accred'] = z['aha_mapp11']
z['aha_mapp11_hfap_accred'] = np.select(
  condlist = [z['aha_mapp11_hfap_accred'] == '1', z['aha_mapp11_hfap_accred'] == '2'],
  choicelist = ['hfap accredited', 'not hfap accredited'],
  default = 'missing', 
)

z['aha_mapp12_aoa_intern'] = z['aha_mapp12']
z['aha_mapp12_aoa_intern'] = np.select(
  condlist = [z['aha_mapp12_aoa_intern'] == '1', z['aha_mapp12_aoa_intern'] == '2'],
  choicelist = ['aoa internship', 'no aoa internship'],
  default = 'missing', 
)

z['aha_mapp13_aoa_res'] = z['aha_mapp13']
z['aha_mapp13_aoa_res'] = np.select(
  condlist = [z['aha_mapp13_aoa_res'] == '1', z['aha_mapp13_aoa_res'] == '2'],
  choicelist = ['aoa residency', 'no aoa residency'],
  default = 'missing', 
)

z['aha_mapp16_catholic_op'] = z['aha_mapp16']
z['aha_mapp16_catholic_op'] = np.select(
  condlist = [z['aha_mapp16_catholic_op'] == '1', z['aha_mapp16_catholic_op'] == '2'],
  choicelist = ['catholic op', 'not catholic op'],
  default = 'missing', 
)

z['aha_mapp18_critical_access'] = z['aha_mapp18']
z['aha_mapp18_critical_access'] = np.select(
  condlist = [z['aha_mapp18_critical_access'] == '1', z['aha_mapp18_critical_access'] == '2'],
  choicelist = ['critical access', 'not critical access'],
  default = 'missing', 
)

z['aha_mapp19_rural_ref'] = z['aha_mapp19']
z['aha_mapp19_rural_ref'] = np.select(
  condlist = [z['aha_mapp19_rural_ref'] == '1', z['aha_mapp19_rural_ref'] == '2'],
  choicelist = ['rural referal center', 'not rural referal center'],
  default = 'missing', 
)

z['aha_mapp20_sole_prov'] = z['aha_mapp20']
z['aha_mapp20_sole_prov'] = np.select(
  condlist = [z['aha_mapp20_sole_prov'] == '1', z['aha_mapp20_sole_prov'] == '2'],
  choicelist = ['sole provider', 'not sole provider'],
  default = 'missing', 
)

z['aha_mapp21_dnv_accred'] = z['aha_mapp21']
z['aha_mapp21_dnv_accred'] = np.select(
  condlist = [z['aha_mapp21_dnv_accred'] == '1', z['aha_mapp21_dnv_accred'] == '2'],
  choicelist = ['dnv accredited', 'not dnv accredited'],
  default = 'missing', 
)

z['aha_mapp22_ahrq_accred'] = z['aha_mapp22']
z['aha_mapp22_ahrq_accred'] = np.select(
  condlist = [z['aha_mapp22_ahrq_accred'] == '1', z['aha_mapp22_ahrq_accred'] == '2'],
  choicelist = ['ahrq accredited', 'not ahrq accredited'],
  default = 'missing', 
)

# %%
# lists all duplicates based on columns in dataframe 
z[z.duplicated(subset=['aha_mcrnum', 'aha_year'])]

# %% 
# sort in place
z.sort_values(by=['aha_mcrnum', 'aha_year', 'aha_fte', 'aha_admtot', 'aha_bdtot',], ascending=[True, True, False, False, False], inplace=True)

# %%
# write duplicates to list
dupes = z[z.duplicated(subset=['aha_mcrnum', 'aha_year'])]
dupes['aha_mcrnum'].unique().tolist()

# %%
# print list of all columns in z
print(z.columns.tolist())

# check for duplicated columns (sanity check) 
z.columns.value_counts()

# %%
# check duplicate examples ordered reasonably
z[z["aha_mcrnum"] == '102010']
z[z["aha_mcrnum"] == '150167']
z[z["aha_mcrnum"] == '192019']
z[z["aha_mcrnum"] == '193064']
z[z["aha_mcrnum"] == '194074']
z[z["aha_mcrnum"] == '230195']
z[z["aha_mcrnum"] == '222046']
z[z["aha_mcrnum"] == '234041']
z[z["aha_mcrnum"] == '260062']
z[z["aha_mcrnum"] == '264028']
z[z["aha_mcrnum"] == '310022']
z[z["aha_mcrnum"] == '313032']
z[z["aha_mcrnum"] == '450133']
z[z["aha_mcrnum"] == '451380']
z[z["aha_mcrnum"] == '452039']

# %% 
# look at column with zip code data 
z['aha_mloczip'].value_counts()
z['aha_mloczip'].describe()

# %%
# clean aha_mloczip column - first 5-digits
# note: code built using https://regex101.com     
z['aha_mloczip'] = z['aha_mloczip'].apply(lambda x: '{0:0>5}'.format(x))                                         
z['aha_mloczip_5'] = z['aha_mloczip'].str.extract(r'^\s*(\d{4,})', expand=False).apply(lambda x: '{0:0>5}'.format(x))
# check 
z['aha_mloczip_5'].value_counts()
z['aha_mloczip_5'].describe()

# %% 
# generate random row sample df
rando = z
rando.sample(n=50)
rando 

# %%
# drop duplicates in order to uniquely merge
z.drop_duplicates(subset=['aha_mcrnum', 'aha_year'], keep='first', inplace=True)

# %%
# check for duplicates
dupes_2 = z[z.duplicated(subset=['aha_mcrnum', 'aha_year'])]
dupes_2['aha_mcrnum'].unique().tolist()

# %%
# save to parquet file
z.to_parquet(dirname / f'../data/aha_processed_data.parquet', engine='pyarrow')
