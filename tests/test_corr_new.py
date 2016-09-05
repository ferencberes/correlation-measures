import sys, os, math
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

sys.path.insert(1, os.path.join(sys.path[0], '../python'))

import correlation_new.correlation_computer as cc 
import correlation_new.correlation_computer_numpy as cc_np 

top_list_prev = pd.DataFrame({'scores':[8,6,6,5,3,2,1]}, index=['a','b','c','d','e','f','g'])
top_list = pd.DataFrame({'scores':[9,7,5,5,4,2,1]}, index=['h','k','a','l','c','d','b'])
vector1 = [9,9,1,9,2.5,4,2.5,5,6,7]
vector2 = [1,2,3.5,3.5,5,6,7,9,9,9]
vector_short = [1,2,3]
vector_short2 = [4,5,6]
weight = [0.1, 0.05, 2]
first_test, second_test = cc.get_first_second_vector(vector_short)
epsilon=0.00001

### Testing preprocessor functions ###

def test_proc_corr():
	list_a = [0,0,8,0,6,5,6,3,2,1]
	list_b = [9,7,5,5,4,2,1,0,0,0]
	assert list_a, list_b == cc.proc_corr(top_list_prev, top_list)

def test_proc_corr_ranks():
	list_a = [9,9,1,9,2.5,4,2.5,5,6,7]
	list_b = [1,2,3.5,3.5,6,7,8,10,10,10]
	assert list_a, list_b == cc.proc_corr_ranks(top_list_prev, top_list)


### Testing Weighted Kendall's Tau custom implementation ###

def test_first_second_vector():
	first = [1,1,1,2,2,2,3,3,3]
	second = [1,2,3,1,2,3,1,2,3]
	assert first == list(first_test)
	assert second == list(second_test)

def test_signum_vector():
	signum = [0, -1, -1, 1, 0, -1, 1, 1, 0]
	assert signum == list(cc.get_signum_vector(first_test, second_test))

def test_weight_vector():
	weight=[2, 1.5, float(4)/3, 1.5, 1, float(5)/6, float(4)/3, float(5)/6, float(2)/3]
	test_weight=cc.get_weight_vector(first_test,second_test)
	same=True
	for i in range(len(weight)):
		if abs(weight[i]-test_weight[i])>epsilon:
			same=False
			print weight, test_weight
	assert same

def test_weighted_product():
	product = 36.9
	assert abs(product - cc.get_weighted_product(np.array(vector_short), np.array(vector_short2), np.array(weight))) < epsilon

def test_compute_correl():
	correl1=32/math.sqrt(77*14)
	correl2=36.9/math.sqrt(18.3*74.85)
	assert abs(correl1 - cc.compute_correl(np.array(vector_short), np.array(vector_short2))[0])< epsilon
	assert abs(correl2 - cc.compute_correl(np.array(vector_short), np.array(vector_short2), np.array(weight))[0]) < epsilon


### Testing custom Numpy based correlation implementations ###

def test_scipy_numpy():
	assert abs(cc.corr_pearson(top_list_prev, top_list)[0]-cc_np.corr_pearson_np(top_list_prev, top_list)[0]) < epsilon
	assert abs(cc.corr_spearman(top_list_prev, top_list)[0]-cc_np.corr_spearman_np(top_list_prev, top_list)[0]) < epsilon
	assert abs(cc.corr_kendalltau(top_list_prev, top_list)[0]-cc_np.corr_kendalltau_np(top_list_prev, top_list)[0]) < epsilon
	vector_prev, vector=cc.proc_corr_ranks(top_list_prev, top_list)
	assert abs(pearsonr(vector_prev, vector)[0] - cc.corr_spearman(top_list_prev, top_list)[0]) < epsilon
