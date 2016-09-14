#!/bin/bash

dataset_id="$1"
measure_id="$2"
corr_type="$3"

for i in $(seq 1 5); do
./get_corr_single_day.sh $dataset_id $measure_id $corr_type $i &
done;
wait;

for i in $(seq 6 10); do
./get_corr_single_day.sh $dataset_id $measure_id $corr_type $i &
done;
wait;

for i in $(seq 11 15); do
./get_corr_single_day.sh $dataset_id $measure_id $corr_type $i &
done;
wait;

for i in $(seq 16 21); do
get_corr_single_day.sh $dataset_id $measure_id $corr_type $i &
done;
wait;

echo "FINISHED!!!"

