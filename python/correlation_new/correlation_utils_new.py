import pandas as pd
import numpy as np
import correlation_computer as cc

def load_score_map(input_prefix ,day, measure):
    """The centrality maps were pre-sorted in decreasing order!!!"""
    scores = pd.read_csv(input_prefix + '/%s_scores_%i.txt_s' % (measure,day), sep=" ", names=["id","score"])
    scores = scores.set_index("id")
    return scores


def result2file(result_list,file_name):
    """Write correlation values to file for each snapshot."""
    with open(file_name, 'w') as f:
        #f.write('index value\n')
        for i in xrange(len(result_list)):
            f.write('%i %f\n' % (i, result_list[i]))
    print 'Done'


def calculate_corr_for_a_day(input_prefix, day, corr_type, measure):
    """Calculate the selected correlation measure for the given snapshot."""
    prev_day = load_score_map(input_prefix, day-1, measure)
    current_day = load_score_map(input_prefix, day, measure)
    corr = None
    if corr_type=="pearson":
        corr = cc.corr_pearson(prev_day,current_day)[0]
    elif corr_type=="spearman":
        corr = cc.corr_spearman(prev_day,current_day)[0]
    elif corr_type=="kendall":
        corr = cc.corr_kendalltau(prev_day,current_day)[0]
    elif corr_type=="w_kendall":
        corr = cc.corr_weighted_kendalltau(prev_day,current_day)[0]
    else:
        raise RuntimeError("Invalid correlation type: %s!" % corr_type)
    return corr
        

def calculate_corr_for_days(input_prefix, days, corr_type, measure_type):
    """Calculate the selected correlation measure for multiple snapshots."""
    return map(lambda x: calculate_corr_for_a_day(input_prefix, x, corr_type=corr_type, measure=measure_type), days)

