#!/bin/bash

dataset_id="$1"
measure_id="$2"
corr_type="$3"
day=$4

input_prefix="/mnt/idms/fberes/NETWORK/DATA/temporal_centralities/centrality_output_for_datasets/"$dataset_id"/centrality_scores/"
output_prefix="/mnt/idms/fberes/NETWORK/andreas_article/correlations/parts/"$dataset_id"_"$measure_id

python ../python/correlation_new/correlation_utils_new.py $input_prefix $day $corr_type $measure_id $output_prefix

