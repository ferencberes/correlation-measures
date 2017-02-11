import correlation_computer as cc
import numpy as np
import math
import numexpr as ne
from scipy.stats import rankdata

def corr_kendalltau_np(top_list_prev, top_list):
    vector_prev, vector=cc.proc_corr_ranks(top_list_prev, top_list)
    first_prev, second_prev = cc.get_first_second_vector(vector_prev)
    first, second = cc.get_first_second_vector(vector)
    sign_prev = cc.get_signum_vector(first_prev, second_prev)
    sign = cc.get_signum_vector(first, second)
    return cc.compute_correl(sign_prev,sign)

def corr_spearman_np(top_list_prev, top_list):
    vector_prev, vector=cc.proc_corr_ranks(top_list_prev, top_list)
    diff = get_avg_diff(vector)
    diff_prev = get_avg_diff(vector_prev)
    return cc.compute_correl(diff_prev,diff)

def corr_pearson_np(top_list_prev, top_list):
	list_a,list_b = cc.proc_corr(top_list_prev, top_list)
	diff_a = get_avg_diff(list_a)
	diff_b = get_avg_diff(list_b)
	return cc.compute_correl(diff_a, diff_b)

def get_avg_diff(vector):
    avg_vector = np.full(len(vector), np.average(vector))
    return ne.evaluate('vector-avg_vector')