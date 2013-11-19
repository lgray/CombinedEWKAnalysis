#!/bin/bash

limType=$1

python split_atgc_coefs.py ../data/WV_semileptonic/ATGC_shape_coefficients.root
cp ww_ATGC_shape_coefficients.root ../data/WV_semileptonic/
cp wz_ATGC_shape_coefficients.root ../data/WV_semileptonic/

python buildWVworkspace.py muon ${limType}
python buildWVworkspace.py electron ${limType}

combineCards.py *boosted_${limType}.txt > wv_semil_combined_${limType}.txt
text2workspace.py -m 126 wv_semil_combined_${limType}.txt -o ATGC_WV_elmu_workspace_${limType}.root -P CombinedEWKAnalysis.CommonTools.HagiwaraAndZeppenfeldTwoDimensionalModel:${limType}Model