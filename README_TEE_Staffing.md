# README

#----------------------------------------------------------------#
# Code Files
#----------------------------------------------------------------#

## Code Files - Python 

|file name|data loaded|description|output|
|--|--|--|--|
|load_data.py|out.csv|loads appended CMS data, cleans, processes, filters, and outputs .parquet file|cms_processed_data.parquet|

|load_aha.py|AHA_2009_2017_a.csv|loads AHA data, cleans, processes, filters, and outputs .parquet file|aha_processed_data.parquet|

|load_ahrf.py|ahrf_edit.csv|loads ahrf data, cleans, processes, filters, and outputs .parquet file|ahrf_processeed_data.parquet|

|load_geo.py|zip_code_database.csv|loads geocoding data, cleans, processes, filters, outputs .parquet file| geo_processed_data.parquet|

|merge_data.py|aha_processed_data.parquet; ahrf_processed_data.parquet; geo_processed_data.parquet; cms_processed_data.parquet; (ssa_fips_processed_data.parquet)|loads multiple data files, merges datasets, and outputs parquet file| merged_data.parquet

|working.py|merged_data.parquet.csv|loads & processes merged_data.parquet file| (1) data_visualization.csv; (2) data_clean.csv; (3) data_raw_valve.parquet; (4) data_raw_valve.csv; (5) data_raw_cabg.parquet; (6) data_raw_cabg.csv|

|prepare_data.py|data_raw_valve/cabg.parquet|loads valve, +/- CABG, 2009-2015; OR [toggles between] isolated CABG 2013 - 2015; processes data for model training -- both models |(1) numerical_data_valve.csv; (2) numerical_data_cabg.csv|

## Code Files - STATA

|file name|data loaded|description|output|
|--|--|--|--|
|model_1_valve_date.do|numerical_data_valve.csv|data preparation; baseline characteristics; GLMM analyses|n/a|

|model_2_cabg_date.do|numerical_data_cabg.csv|data preparation; baseline characteristics; GLMM analyses|n/a|





