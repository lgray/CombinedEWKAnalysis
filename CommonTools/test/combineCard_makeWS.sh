#!/bin/bash

limType=$1
sig_syst=$2 

python split_atgc_coefs.py ../data/WV_semileptonic/ATGC_shape_coefficients.root
cp ww_ATGC_shape_coefficients.root ../data/WV_semileptonic/
cp wz_ATGC_shape_coefficients.root ../data/WV_semileptonic/

python buildWVworkspace.py muon ${limType} ${sig_syst}
python buildWVworkspace.py electron ${limType} ${sig_syst}

combineCards.py *boosted_${limType}_${sig_syst}.txt > wv_semil_combined_${limType}_${sig_syst}.txt
text2workspace.py -m 126 wv_semil_combined_${limType}_${sig_syst}.txt -o ATGC_WV_elmu_workspace_${limType}.root -P CombinedEWKAnalysis.CommonTools.HagiwaraAndZeppenfeldTwoDimensionalModel:${limType}Model