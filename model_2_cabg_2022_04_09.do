// setup  
set more off
set linesize 255
// markdoc

// set markdoc to OFF
//OFF
cd "/path/"

// log file setup 
local file_name = "model_2_log"
local path = "/path/" 

//
log using "`path'`file_name'.txt", replace text name("model_2_log")

// 
import delimited "/path/data.csv", clear

// note: tee_rate variables (organization and surgeon-level) not included

// generate additional exclude condition
generate exclude = 1 if cms_prf_physn_npi_srg == .

// scale 
generate anesthesiologist_tee_ratio_sc = anesthesiologist_tee_ratio*100
generate cms_prf_physn_npi_srg_tee_rate_s = cms_prf_physn_npi_srg_tee_rate*100
generate cms_org_npi_tee_rate_sc = cms_org_npi_tee_rate*100

// look at surgical volume
summarize cms_org_npi_count, detail
summarize cms_prf_physn_npi_srg_count, detail 
// dichotomize organization volume
generate cms_org_npi_count_high = cond(cms_org_npi_count > 169, 1, 0)
generate cms_org_npi_count_low = cond(cms_org_npi_count <= 169, 1, 0)

// dichotimize surgeon tee rate variable 
summarize cms_prf_physn_npi_srg_tee_rate if exclude != 1, detail
histogram cms_prf_physn_npi_srg_tee_rate if exclude != 1
generate surgeon_tee_ratio_high = cond(cms_prf_physn_npi_srg_tee_rate >= .6969697, 1, 0)
generate surgeon_tee_ratio_low = cond(cms_prf_physn_npi_srg_tee_rate < .6969697, 1, 0)
tabulate surgeon_tee_ratio_high if exclude != 1

// dichotimize hospital tee rate variable 
summarize cms_org_npi_tee_rate if exclude != 1, detail
histogram cms_org_npi_tee_rate if exclude != 1
generate org_tee_ratio_high = cond(cms_org_npi_tee_rate >= .5541402 , 1, 0)
generate org_tee_ratio_low = cond(cms_org_npi_tee_rate < .5541402 , 1, 0)
tabulate org_tee_ratio_high if exclude != 1

// dichotomize anesthesiologist_tee_ratio variable for CABG 
summarize anesthesiologist_tee_ratio if exclude != 1, detail
generate anesthesiologist_tee_ratio_high = cond(anesthesiologist_tee_ratio >= .7134238, 1, 0)
generate anesthesiologist_tee_ratio_low = cond(anesthesiologist_tee_ratio < .7134238, 1, 0)
// dichotomize anesthesiologist_tee_ratio variable for CABG [75th percentile]
summarize anesthesiologist_tee_ratio if exclude != 1, detail
generate anesthesiologist_tee_ratio_75_h = cond(anesthesiologist_tee_ratio >= .8407871, 1, 0)
generate anesthesiologist_tee_ratio_75_l = cond(anesthesiologist_tee_ratio < .8407871, 1, 0)

// dichotomize cardiologist_tee_ratio variable for CABG 
summarize cardiologist_tee_ratio if exclude != 1, detail
generate cardiologist_tee_ratio_high = cond(cardiologist_tee_ratio >= .2006803, 1, 0)
generate cardiologist_tee_ratio_low = cond(cardiologist_tee_ratio < .2006803, 1, 0)
// dichotomize cardiologist_tee_ratio variable for CABG [75th percentile]
summarize cardiologist_tee_ratio if exclude != 1, detail
generate cardiologist_tee_ratio_75_h = cond(cardiologist_tee_ratio >= .4223602 , 1, 0)
generate cardiologist_tee_ratio_75_l = cond(cardiologist_tee_ratio < .4223602 , 1, 0)

// potential data visualization(s) 
twoway scatter cms_prf_physn_npi_srg_tee_rate cms_org_npi_count if exclude != 1, graphregion(color(white)) msize(vtiny) || lfit cms_prf_physn_npi_srg_tee_rate cms_org_npi_count 
twoway scatter cms_org_npi_tee_rate cms_org_npi_count if exclude != 1, graphregion(color(white)) || lfit cms_org_npi_tee_rate cms_org_npi_count 

histogram cms_prf_physn_npi_srg_tee_rate if exclude != 1, graphregion(color(white)) color(grey) lcolor(blue) bin(100) xtitle("Probability of TEE by Surgeon") title("TEE in CABG by Surgeon", size(large)) plotregion(fcolor(white))
histogram cms_org_npi_tee_rate if exclude != 1, graphregion(color(white)) color(grayscale 1) lcolor(green) bin(100) xtitle("Probability of TEE by Organization") title("TEE in CABG by Organization", size(large))

// the data visualization: organization tee rate with anesthesiologist performs tee model vs organization tee rate without anesthesiologist tee perform model 
twoway (kdensity cms_org_npi_tee_rate if exclude != 1 & anesthesiologist_tee_ratio_high == 1, lcolor(blue)) (kdensity cms_org_npi_tee_rate if exclude != 1 & cardiologist_tee_ratio_high == 1, lcolor(orange)), legend(order(1 "Anesthesiolgist Performs TEE" 2 "Cardiologist Performs TEE")) ytitle("density") xtitle("Probability of TEE by Organization") title("TEE in CABG by Organization & Staffing Model: Anesthesiologist vs Cardiologist", size(medsmall)) graphregion(color(white))
/* 
// save as .eps & .svg 
. graph export "/Users/emily2/working/CMS_TEE_project/stata/kdensity_cabg.eps", as(eps) name("Graph") preview(off)
file /Users/emily2/working/CMS_TEE_project/stata/kdensity_cabg.eps saved as EPS format
//
. graph export "/Users/emily2/working/CMS_TEE_project/stata/kdensity_cabg.svg", as(svg) name("Graph")
file /Users/emily2/working/CMS_TEE_project/stata/kdensity_cabg.svg saved as SVG format
*/ 

// alternate option for graphing 
kdensity cms_org_npi_tee_rate if exclude != 1, nograph generate(x fx)
kdensity cms_org_npi_tee_rate if exclude != 1 & anesthesiologist_tee_ratio_high == 1, nograph generate(fx0) at (x) 
kdensity cms_org_npi_tee_rate if exclude != 1 & cardiologist_tee_ratio_high == 1, nograph generate(fx1) at (x) 
label var x "Probability of TEE by Organization"
label var fx1 "Cardiologist TEE"
label var fx0 "Anesthesiologist TEE"
line fx1 fx0 x, lcolor(orange green) ytitle(density) 

// the data visualization: surgeon tee rate with anesthesiologist performs tee model vs organization tee rate without anesthesiologist tee perform model 
twoway (kdensity cms_prf_physn_npi_srg_tee_rate if exclude != 1 & anesthesiologist_tee_ratio_high == 1, lcolor(dknavy)) (kdensity cms_prf_physn_npi_srg_tee_rate if exclude != 1 & cardiologist_tee_ratio_high == 1, lcolor(brown)), legend(order(1 "Anesthesiologist Performs TEE" 2 "Cardiologist Performs TEE")) ytitle("Density") xtitle("Probability of TEE use by Surgeon") title("TEE in CABG by Surgeon & Staffing Model: Anesthesiologist vs Cardiologist", size(medsmall)) graphregion(color(gs15)) plotregion(color(white))

// surgeon and hospital correlated? - Yes 
regress cms_prf_physn_npi_srg_tee_rate cms_org_npi_tee_rate if exclude != 1
// anesthesiologist and hospital (or surgeon TEE preference) correlated? - No 
regress anesthesiologist_tee_ratio cms_org_npi_tee_rate if exclude != 1
regress anesthesiologist_tee_ratio cms_prf_physn_npi_srg_tee_rate if exclude != 1

// quintile surgeon TEE rate 
// xtile
summarize cms_prf_physn_npi_srg_tee_rate, detail 
xtile srg_tee_rate_quartile = cms_prf_physn_npi_srg_tee_rate, nq(4) 
tabstat cms_prf_physn_npi_srg_tee_rate, stat(n mean min max sd p50) by(srg_tee_rate_quartile)

// quintile organization TEE rate 
// xtile
summarize cms_org_npi_tee_rate, detail 
xtile org_tee_rate_quartile = cms_org_npi_tee_rate, nq(4) 
tabstat cms_org_npi_tee_rate, stat(n mean min max sd p50) by(org_tee_rate_quartile)

// mutually exclusive staffing variable [cutpoint - median]
generate anes_vs_cards = "" 
replace anes_vs_cards = "anesthesiologist_model" if anesthesiologist_tee_ratio_high == 1 & cardiologist_tee_ratio_low == 1
replace anes_vs_cards = "cardiologist_model" if cardiologist_tee_ratio_high == 1 & anesthesiologist_tee_ratio_low == 1 
replace anes_vs_cards = "mixed_staffing_model" if anes_vs_cards == "" 
tabulate anes_vs_cards, miss
encode anes_vs_cards, generate(anes_vs_cards_e) 

// mutually exclusive staffing variable [cutpoint - 75th percentile ]
generate anes_vs_cards_extreme = "" 
replace anes_vs_cards_extreme = "anesthesiologist_model" if anesthesiologist_tee_ratio_75_h == 1 & cardiologist_tee_ratio_75_l == 1
replace anes_vs_cards_extreme = "cardiologist_model" if cardiologist_tee_ratio_75_h == 1 & anesthesiologist_tee_ratio_75_l == 1 
replace anes_vs_cards_extreme = "mixed_staffing_model" if anes_vs_cards_extreme == "" 
tabulate anes_vs_cards_extreme, miss
encode anes_vs_cards_extreme, generate(anes_vs_cards_extreme_e)

// look at TEE distribution across staffing models 
tabulate anes_vs_cards cms_cpt_tee if exclude != 1, chi2 
tabulate anes_vs_cards_extreme cms_cpt_tee if exclude != 1, chi2 

// the data visualization: surgeon tee rate with anesthesiologist performs tee model vs organization tee rate without anesthesiologist tee perform model 
twoway (kdensity cms_org_npi_tee_rate if exclude != 1 & anes_vs_cards == "anesthesiologist_model", lcolor(blue)) (kdensity cms_org_npi_tee_rate if exclude != 1 & anes_vs_cards == "cardiologist_model", lcolor(orange)), legend(order(1 "Anesthesiolgist Performs TEE" 2 "Cardiologist Performs TEE")) ytitle("density") xtitle("Probability of TEE by Organization") title("TEE in CABG by Organization & Staffing Model: Anesthesiologist vs Cardiologist", size(medsmall)) graphregion(color(white))

// deal with states
gen census_northeast = cond((state_ct == 1 | state_me == 1 | state_ma == 1 | state_nh == 1 | state_ri == 1 | state_vt == 1 | state_nj == 1 | state_ny == 1 | state_pa == 1), 1, 0)
gen census_midwest = cond((state_il  == 1 | state_in == 1 | state_mi == 1 | state_oh == 1 | state_wi == 1 | state_ia == 1 | state_ks == 1 | state_mn == 1 | state_mo == 1 | state_ne == 1 | state_nd == 1 | state_sd == 1), 1, 0) 
gen census_south = cond((state_de == 1 | state_fl == 1 | state_ga == 1 | state_md == 1 | state_nc == 1 | state_sc == 1 | state_va == 1 | state_dc == 1 | state_wv == 1 | state_al == 1 | state_ky == 1 | state_ms == 1 | state_tn == 1 | state_ar == 1 | state_la == 1 | state_ok == 1 | state_tx == 1), 1, 0) 
gen census_west = cond((state_az == 1 | state_co == 1 | state_id == 1 | state_mt == 1 | state_nv == 1 | state_nm == 1 | state_ut == 1 | state_wy == 1 | state_ca == 1 | state_or == 1 | state_wa == 1), 1, 0)

gen census_region = " " 
replace census_region = "northeast" if census_northeast == 1
replace census_region = "midwest" if census_midwest == 1
replace census_region = "south" if census_south == 1
replace census_region = "west" if census_west == 1
// sanity check 
tabulate census_region, miss 

// sex variable 
generate male = cond((cms_sex_medpar ==0 ), 1, 0) 
generate female = cond((cms_sex_medpar == 1), 1, 0)  
// label 
generate sex = "" 
replace sex = "male" if male == 1
replace sex = "female" if female == 1 
encode sex, generate(sex_e) 

///////////////////////////////////////////////////////////////////////////////

// Descriptive Statistics: CABG

///////////////////////////////////////////////////////////////////////////////

// mtable set command
mtable set cabg_characteristics

// 
tabulate anes_vs_cards_e cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" anes_vs_cards_e "staffing"

ttest cms_age_cnt, by(cms_cpt_tee) 
mtable "ttest" cms_age_cnt "age"

tabulate male cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" male "male"

tabulate female cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" female "female"

tabulate cms_race_str_white cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_race_str_white "white"

tabulate cms_race_str_black cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_race_str_black "black"

tabulate cms_race_str_asian cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_race_str_asian "asian"

tabulate cms_race_str_northamericannative cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_race_str_northamericannative "north_american_native"

tabulate cms_race_str_other cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_race_str_other "race_other"

tabulate cms_race_str_unknown cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_race_str_unknown "race_unknown"

tabulate cms_race_str_hispanic cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_race_str_hispanic "hispanic_ethnicity"

tabulate cms_admsnday_1 cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_admsnday_1 "sunday"

tabulate cms_admsnday_2 cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_admsnday_2 "monday"

tabulate cms_admsnday_3 cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_admsnday_3 "tuesday"

tabulate cms_admsnday_4 cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_admsnday_4 "wednesday"

tabulate cms_admsnday_5 cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_admsnday_5 "thursday"

tabulate cms_admsnday_6 cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_admsnday_6 "friday"

tabulate cms_admsnday_7 cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_admsnday_7 "saturday"

tabulate cms_admit_type_elective cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_admit_type_elective "elective_admit"

tabulate cms_admit_type_emergency cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_admit_type_emergency "emergency_admit"

tabulate cms_admit_type_urgent cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_admit_type_urgent "urgent_admit"

tabulate cms_arrhythmia_6_preexist cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_arrhythmia_6_preexist "arrhythmia"

tabulate cms_chf_6_preexist cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_chf_6_preexist "chf"

tabulate cms_cpd_6_preexist cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_chf_6_preexist "cpd"

tabulate cms_diabetes_all_6_preexist cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_diabetes_all_6_preexist "diabetes"

tabulate cms_htn_all_6_preexist cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_htn_all_6_preexist "hypertension"

tabulate cms_liver_6_preexist cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_liver_6_preexist "liver"

tabulate cms_neuro_6_preexist cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_neuro_6_preexist "neuro"

tabulate cms_obesity_6_preexist cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_obesity_6_preexist "obesity"

tabulate cms_pulm_circ_6_preexist cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_pulm_circ_6_preexist "pulmonary_circ"

tabulate cms_pvd_6_preexist cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_pvd_6_preexist "pvd"

tabulate cms_renal_6_preexist cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_renal_6_preexist "renal"

ttest cms_org_npi_tee_rate, by(cms_cpt_tee) 
mtable "ttest" cms_org_npi_tee_rate "TEE_ratio_organization"

ttest cms_prf_physn_npi_srg_tee_rate, by(cms_cpt_tee) 
mtable "ttest" cms_prf_physn_npi_srg_tee_rate "TEE_ratio_surgeon"

ttest anesthesiologist_tee_ratio, by(cms_cpt_tee) 
mtable "ttest" anesthesiologist_tee_ratio "Anesthesiologist_tee_ratio"

ttest cardiologist_tee_ratio, by(cms_cpt_tee) 
mtable "ttest" cardiologist_tee_ratio "Cardiologist_tee_ratio"

ttest cms_org_npi_count, by(cms_cpt_tee) 
mtable "ttest" cms_org_npi_count "surgical_volume_hospital"

ttest cms_org_npi_annual_count, by(cms_cpt_tee) 
mtable "ttest" cms_org_npi_annual_count "surgical_volume_hospital_yr"

tabulate cms_org_npi_count_high cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_org_npi_count_high "high_surgical_volume_hospital"

ttest cms_prf_physn_npi_srg_count, by(cms_cpt_tee) 
mtable "ttest" cms_prf_physn_npi_srg_count "surgical_volume_surgeon"

ttest cms_prf_physn_npi_srg_annual_cou, by(cms_cpt_tee) 
mtable "ttest" cms_prf_physn_npi_srg_annual_cou "surgical_volume_surgeon_yr"

ttest aha_hospbd, by(cms_cpt_tee) 
mtable "ttest" aha_hospbd "hospital_beds"

ttest aha_adc, by(cms_cpt_tee) 
mtable "ttest" aha_adc "daily_census"

ttest aha_ftmdtf, by(cms_cpt_tee) 
mtable "ttest" aha_ftmdtf "full_time_physicians"

ttest aha_ftres, by(cms_cpt_tee) 
mtable "ttest" aha_ftres "full_time_residents"

ttest aha_fttran84, by(cms_cpt_tee) 
mtable "ttest" aha_fttran84 "full_time_trainees"

ttest aha_ftlpntf, by(cms_cpt_tee) 
mtable "ttest" aha_ftlpntf "full_time_nurses"

ttest aha_ftast, by(cms_cpt_tee) 
mtable "ttest" aha_ftast "full_time_nursing_asst"

ttest aha_suropip, by(cms_cpt_tee) 
mtable "ttest" aha_suropip "hospital_ip_surgeries"

tabulate aha_mapp1_jc_accred cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" aha_mapp1_jc_accred "jc_accred"

tabulate aha_mapp3_acgme cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" aha_mapp3_acgme "acgme_certified"

tabulate aha_mapp5_med_sch cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" aha_mapp5_med_sch "med_school_affil"

tabulate cms_yr_2013 cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_yr_2013 "2013"

tabulate cms_yr_2014 cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_yr_2014 "2014"

tabulate cms_yr_2015 cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" cms_yr_2015 "2015"

tabulate census_northeast cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" census_northeast "northeast"

tabulate census_midwest cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" census_midwest "midwest"

tabulate census_south cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" census_south "south"

tabulate census_west cms_cpt_tee, chi2 expected miss column matcell(values) matrow(names)
mtable "tabulate" census_west "west"

ttest ahrf_anes_attd_total_2015, by(cms_cpt_tee) 
mtable "ttest" ahrf_anes_attd_total_2015 "anesthesiologists_county"

ttest ahrf_surg_total_2015, by(cms_cpt_tee) 
mtable "ttest" ahrf_surg_total_2015 "surgeons_county"

ttest ahrf_thoracic_surgery_2015, by(cms_cpt_tee) 
mtable "ttest" ahrf_thoracic_surgery_2015 "thoracic_surgeons_county"

ttest ahrf_anes_crna_npi_2015, by(cms_cpt_tee) 
mtable "ttest" ahrf_anes_crna_npi_2015 "crnas_county"

ttest linear_distance_miles, by(cms_cpt_tee) 
mtable "ttest" linear_distance_miles "linear_miles"

// statistics for histograms 
ttest cms_org_npi_tee_rate, by(cms_cpt_tee) 
ttest anesthesiologist_tee_ratio, by(cms_cpt_tee) 
ttest cardiologist_tee_ratio, by(cms_cpt_tee) 

summarize anesthesiologist_tee_ratio, detail
summarize cardiologist_tee_ratio, detail 


///////////////////////////////////////////////////////////////////////////////

// Manuscript CABG: Multilevel Mixed Effects 

///////////////////////////////////////////////////////////////////////////////

// model 0: intercept only to confirm multi-level model needed due to clustering (vs multivariable logitstic model)
melogit cms_cpt_tee || cms_org_npi_num_medpar:, or 
estat icc 
// calculate MOR 
di exp(0.95*sqrt( 2.421066)) /* = 4.3849518 */ 
// calculate MOR 95% CI: 
di exp(0.95*sqrt( 2.211324)) /* = 4.1070274 */ 
di exp(0.95*sqrt( 2.650702)) /* = 4.6959141 */ 

// model 0: 
// multilevel mixed effects 
melogit cms_cpt_tee ib(3).anes_vs_cards_e if exclude != 1, || cms_org_npi_num_medpar:, or
estat icc 
// calculate MOR 
di exp(0.95*sqrt(3.492687)) /* = 5.902816 */ 
// Bo's R code for MOR calculation: exp(qnorm(0.75)*sqrt(2)*sqrt(3.49)) = 5.94
// calculate MOR 95% CI: 
di exp(0.95*sqrt(3.177076)) /* = 5.4374687 */ 
di exp(0.95*sqrt(3.839652)) /* = 6.4335588 */ 

melogit cms_cpt_tee ib(3).anes_vs_cards_e if exclude != 1, || cms_org_npi_num_medpar:
// calculate IOR 
// calculate interval odds ratio (IOR) lower [OR coefficients] [note: need Beta coefficients to calculate the IOR]
// note: to convert back to odds ratio - exponentiate
di exp(.6547791) /* = 1.92 */ 
/* IOR lower anesthesiologist staffing vs mixed */ di exp((.6547791) + (sqrt(2*3.492687)) * (-1.2816)) /* = .0650583 */ 
/* IOR upper anesthesiologist staffing vs mixed */ di exp((.6547791) + (sqrt(2*3.492687)) * (1.2816)) /* = 56.941801 */
/* IOR lower cardiologist staffing vs mixed */ di exp((-1.814811) + (sqrt(2*3.492687)) * (-1.2816)) /* = .0055052 */
/* IOR upper cardiologist staffing vs mixed */ di exp((-1.814811) + (sqrt(2*3.492687)) * (1.2816)) /* = 4.8183889 */ 

///////////////////////////////////////////////////////////////////////////////

// without exclude condition 

///////////////////////////////////////////////////////////////////////////////

// model a: 
// multilevel mixed effects without staffing model 
melogit cms_cpt_tee cms_age_cnt female cms_race_str_white cms_race_str_black cms_race_str_asian cms_race_str_northamericannative cms_race_str_other cms_race_str_hispanic cms_admsnday_1 cms_admsnday_3 cms_admsnday_4 cms_admsnday_5 cms_admsnday_6 cms_admsnday_7 cms_admit_type_elective cms_admit_type_emergency cms_admit_type_urgent cms_arrhythmia_6_preexist cms_chf_6_preexist cms_cpd_6_preexist cms_diabetes_all_6_preexist cms_htn_all_6_preexist cms_liver_6_preexist cms_neuro_6_preexist cms_obesity_6_preexist cms_pulm_circ_6_preexist cms_pvd_6_preexist cms_renal_6_preexist cms_yr_2014 cms_yr_2015 cms_org_npi_annual_count aha_hospbd aha_mapp5_med_sch census_northeast census_south census_west linear_distance_miles, || cms_org_npi_num_medpar:, or 
// look at matrix for stored results
matrix list r(table)
ereturn list 

// calculate local variables 
local MOR_a = exp(0.95 * sqrt(r(table)["b", "/:var(_cons[cms_org_npi_num_medpar])"]))
local MOR_ll_a = exp(0.95 * sqrt(r(table)["ll", "/:var(_cons[cms_org_npi_num_medpar])"]))
local MOR_ul_a = exp(0.95 * sqrt(r(table)["ul", "/:var(_cons[cms_org_npi_num_medpar])"]))
local sigma_a = sqrt(r(table)["b", "/:var(_cons[cms_org_npi_num_medpar])"])
local sigma_ll_a = sqrt(r(table)["ll", "/:var(_cons[cms_org_npi_num_medpar])"])
local sigma_ul_a = sqrt(r(table)["ul", "/:var(_cons[cms_org_npi_num_medpar])"])

// putexcel 
putexcel set "cabg_mor_ior.xls", replace
putexcel A1 = ("variable") B1 = ("sigma") C1 = ("sigma 95% CI ll") D1 = ("sigma 95% CI: ul") E1 = ("MOR") F1 = ("MOR 95% CI: ll") G1 = ("MOR 95% CI: ul")
putexcel A2 = "cms_org_npi_num_medpar"
putexcel B2 = ("`sigma_a'")
putexcel C2 = ("`sigma_ll_a'")
putexcel D2 = ("`sigma_ul_a'")
putexcel E2 = ("`MOR_a'")
putexcel F2 = ("`MOR_ll_a'")
putexcel G2 = ("`MOR_ul_a'")

// outreg 
outreg2 using cabg_mixed_effects.xml, replace dec(2) stat(coef ci pval) eform sideway alpha(0.0001, 0.001, 0.01) noaster ctitle(model_a) 

/* 
outreg2 using multilevel_mixed_cabg_hos_a.xml, replace dec(3) stat(coef se ci pval) addstat(MOR_a, `MOR_a', MOR_ll_a, `MOR_ll_a', MOR_ul_a, `MOR_ul_a', sigma_a, `sigma_a', sigma_ll_a, `sigma_ll_a', sigma_ul_a, `sigma_ul_a') eform sideway alpha(0.0001, 0.001, 0.01) ctitle(model_a)
*/ 

///////////////////////////////////////////////////////////////////////////////

// model b: 
// multilevel mixed effects logistic regression with staffing model variable
melogit cms_cpt_tee ib(3).anes_vs_cards_e cms_age_cnt female cms_race_str_white cms_race_str_black cms_race_str_asian cms_race_str_northamericannative cms_race_str_other cms_race_str_hispanic cms_admsnday_1 cms_admsnday_3 cms_admsnday_4 cms_admsnday_5 cms_admsnday_6 cms_admsnday_7 cms_admit_type_elective cms_admit_type_emergency cms_admit_type_urgent cms_arrhythmia_6_preexist cms_chf_6_preexist cms_cpd_6_preexist cms_diabetes_all_6_preexist cms_htn_all_6_preexist cms_liver_6_preexist cms_neuro_6_preexist cms_obesity_6_preexist cms_pulm_circ_6_preexist cms_pvd_6_preexist cms_renal_6_preexist cms_yr_2014 cms_yr_2015 cms_org_npi_annual_count aha_hospbd aha_mapp5_med_sch census_northeast census_south census_west linear_distance_miles, || cms_org_npi_num_medpar:, or 
// look at matrix for stored results
matrix list r(table)
ereturn list

// cacluate sigma 
di sqrt(1.565774) /* 1.2513089 */ 
// calculate MOR 
di exp(0.95*sqrt( 1.565774 )) /* = 3.2829535 */ 

// calculate local variables 
local MOR_b = exp(0.95 * sqrt(r(table)["b", "/:var(_cons[cms_org_npi_num_medpar])"]))
local MOR_ll_b = exp(0.95 * sqrt(r(table)["ll", "/:var(_cons[cms_org_npi_num_medpar])"]))
local MOR_ul_b = exp(0.95 * sqrt(r(table)["ul", "/:var(_cons[cms_org_npi_num_medpar])"]))
local sigma_b = sqrt(r(table)["b", "/:var(_cons[cms_org_npi_num_medpar])"])
local sigma_ll_b = sqrt(r(table)["ll", "/:var(_cons[cms_org_npi_num_medpar])"])
local sigma_ul_b = sqrt(r(table)["ul", "/:var(_cons[cms_org_npi_num_medpar])"])

// putexcel 
putexcel set "cabg_mor_ior.xls", modify 
putexcel J1 = ("variable") K1 = ("sigma") L1 = ("sigma 95% CI ll") M1 = ("sigma 95% CI: ul") N1 = ("MOR") O1 = ("MOR 95% CI: ll") P1 = ("MOR 95% CI: ul")
putexcel J2 = "with staffing: cms_org_npi_num_medpar"
putexcel K2 = ("`sigma_b'")
putexcel L2 = ("`sigma_ll_b'")
putexcel M2 = ("`sigma_ul_b'")
putexcel N2 = ("`MOR_b'")
putexcel O2 = ("`MOR_ll_b'")
putexcel P2 = ("`MOR_ul_b'")

// 
outreg2 using cabg_mixed_effects.xml, append dec(2) stat(coef ci pval) eform sideway alpha(0.0001, 0.001, 0.01) noaster ctitle(model_b) 

/*
outreg2 using multilevel_mixed_cabg_hos_b.xml, replace dec(3) stat(coef se ci pval) addstat(MOR_b, `MOR_b', MOR_ll_b, `MOR_ll_b', MOR_ul_b, `MOR_ul_b', sigma_b, `sigma_b', sigma_ll_b, `sigma_ll_b', sigma_ul_b, `sigma_ul_b') eform sideway alpha(0.0001, 0.001, 0.01) ctitle(model_b)
*/ 

///////////////////////////////////////////////////////////////////////////////
 
// model c: beta coefficients instead of odds ratio 
melogit cms_cpt_tee ib(3).anes_vs_cards_e cms_age_cnt female cms_race_str_white cms_race_str_black cms_race_str_asian cms_race_str_northamericannative cms_race_str_other cms_race_str_hispanic cms_admsnday_1 cms_admsnday_3 cms_admsnday_4 cms_admsnday_5 cms_admsnday_6 cms_admsnday_7 cms_admit_type_elective cms_admit_type_emergency cms_admit_type_urgent cms_arrhythmia_6_preexist cms_chf_6_preexist cms_cpd_6_preexist cms_diabetes_all_6_preexist cms_htn_all_6_preexist cms_liver_6_preexist cms_neuro_6_preexist cms_obesity_6_preexist cms_pulm_circ_6_preexist cms_pvd_6_preexist cms_renal_6_preexist cms_yr_2014 cms_yr_2015 cms_org_npi_annual_count aha_hospbd aha_mapp5_med_sch census_northeast census_south census_west linear_distance_miles, || cms_org_npi_num_medpar:
// look at matrix for stored results
matrix list r(table)
ereturn list 

// calculate IOR 
// calculate interval odds ratio (IOR) lower [OR coefficients] [note: need Beta coefficients to calculate the IOR]
// note: to convert back to odds ratio - exponentiate
di exp(.6106107) /* = 1.8415557 */ 
/* IOR lower anesthesiologist staffing vs mixed */ di exp(( .6106107 ) + (sqrt(2*1.565774 )) * (-1.2816)) /* = .19776233 */ 
/* IOR upper anesthesiologist staffing vs mixed */ di exp(( .6106107 ) + (sqrt(2*1.565774 )) * (1.2816)) /* = 17.869667 */
/* IOR lower cardiologist staffing vs mixed */ di exp((-1.159077 ) + (sqrt(2*1.565774 )) * (-1.2816)) /* = .03333295 */
/* IOR upper cardiologist staffing vs mixed */ di exp((-1.159077 ) + (sqrt(2*1.565774 )) * (1.2816)) /* = 3.0119419 */ 

local IOR_anes_l_c = exp((r(table)["b", "cms_cpt_tee:1.anes_vs_cards_e"]) + (sqrt(2 * r(table)["b", "/:var(_cons[cms_org_npi_num_medpar])"]) * (-1.2816)))
local IOR_anes_u_c = exp((r(table)["b", "cms_cpt_tee:1.anes_vs_cards_e"]) + (sqrt(2 * r(table)["b", "/:var(_cons[cms_org_npi_num_medpar])"]) * (1.2816)))
local IOR_cards_l_c = exp((r(table)["b", "cms_cpt_tee:2.anes_vs_cards_e"]) + (sqrt(2 * r(table)["b", "/:var(_cons[cms_org_npi_num_medpar])"]) * (-1.2816)))
local IOR_cards_u_c = exp((r(table)["b", "cms_cpt_tee:2.anes_vs_cards_e"]) + (sqrt(2 * r(table)["b", "/:var(_cons[cms_org_npi_num_medpar])"]) * (1.2816)))

// putexcel 
putexcel set "cabg_mor_ior.xls", modify 
putexcel S1 = ("variable") T1 = ("IOR: ll") U1 = ("IOR: ul") 
putexcel S4 = "anes: TEE" 
putexcel S5 = "cards: TEE"
putexcel T4 = ("`IOR_anes_l_c'")
putexcel U4 = ("`IOR_anes_u_c'")
putexcel T5 = ("`IOR_cards_l_c'")
putexcel U5 = ("`IOR_cards_u_c'")

// outreg 
outreg2 using cabg_mixed_effects.xml, append dec(2) stat(coef ci pval) sideway alpha(0.0001, 0.001, 0.01) noaster ctitle(model_c) 

/* 
outreg2 using multilevel_mixed_cabg_hos_c_ior.xml, replace dec(3) stat(coef se ci pval) addstat(IOR_anes_l_c, `IOR_anes_l_c', IOR_anes_u_c, `IOR_anes_u_c', IOR_cards_l_c, `IOR_cards_l_c', IOR_cards_u_c, `IOR_cards_u_c') sideway alpha(0.0001, 0.001, 0.01) ctitle(model_c)
*/ 

///////////////////////////////////////////////////////////////////////////////


log close _all 



