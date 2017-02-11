#!/bin/bash
data_set="$1"
corr_type="$2"
measure_type="$3"
day_idx="$4"

python correlation_utils_new.py /mnt/idms/fberes/network/DATA/temporal_centralities/centrality_output_for_datasets/"$data_set"/centrality_scores/ /mnt/idms/fberes/network/correlation_2016_12/correlations_tmp/"$data_set" "$corr_type" "$measure_type" "$day_idx"
