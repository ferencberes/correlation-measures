import math
import operator
import pandas as pd
from scipy.stats import pearsonr,spearmanr,kendalltau,rankdata
import itertools
import numpy as np
import numexpr as ne


### Basic correlation measures ###

def corr_pearson(top_list_prev, top_list):
    """Compute Pearson correlation (based on Scipy)
    NOTE: Lists are DataFrame columns AND they must be sorted according to their value!!!"""
    list_a, list_b = proc_corr(top_list_prev, top_list)
    return [pearsonr(list_a, list_b)[0]]

def corr_spearman(top_list_prev, top_list):
    """Compute Spearman's Rho correlation (based on Scipy)
    NOTE: Lists are DataFrame columns AND they must be sorted according to their value!!!"""
    list_a, list_b = proc_corr(top_list_prev, top_list)
    return [spearmanr(list_a, list_b)[0]]

def corr_kendalltau(top_list_prev, top_list):
    """Compute Kendall's Tau correlation (based on Scipy).
    NOTE: Lists are DataFrame columns AND they must be sorted according to their value!!!"""
    # it is irrelevant whether we compute kendall for ranks or scores.
    list_a, list_b = proc_corr(top_list_prev, top_list)
    return [kendalltau(list_a, list_b)[0]]

def corr_weighted_kendalltau(top_list_prev, top_list):
    """Compute weighted Kendall's Tau correlation (based on custom implementation!).
    NOTE: Lists are DataFrame columns AND they must be sorted according to their value!!!"""
    # it is irrelevant whether we compute kendall for ranks or scores.
    list_a, list_b = proc_corr(top_list_prev, top_list)
    if len(list_a) != len(list_b):
        raise RuntimeError("The length of 'list_a' and 'list_b' must be the same!")
    rank_list_a = tiedrank(list_a)
    rank_list_b = tiedrank(list_b)
    return [computeWKendall(rank_list_a,rank_list_b,ranked_input=True)[1]]

### Score list preproceor functions ###

def proc_corr(l_1, l_2):
    """Fill lists with scores ordered by the ranks in the second list. 
    NOTE: Lists are DataFrame columns AND they must be sorted according to their value!!!"""
    l1=l_1.copy()
    l2=l_2.copy()
    l1.columns=['l1_col']
    l2.columns=['l2_col']
    df=pd.concat([l2, l1], axis=1).fillna(0)
    index_diff=list(set(list(l1.index))-set(list(l2.index)))
    index_diff.sort()
    sorted_id=list(l2.index)+index_diff # NOTE: input lists must be sorted! For custom weighted correlations?
    df=df.reindex(sorted_id)
    return np.array(df['l1_col']), np.array(df['l2_col'])


def tiedrank(vector):
    """Return rank with average tie resolution. Rank is based on decreasing score order"""
    return (len(vector) + 1) * np.ones(len(vector)) - rankdata(vector, method='average')


def get_union_of_active_nodes(day_1, day_2):
    """Find common subvectors of non-zero elements. (we only consider positive scores to be active nodes)"""
    ind_one=np.nonzero(day_1)[0];
    ind_two=np.nonzero(day_2)[0];
    ind=np.union1d(ind_one,ind_two)
    ranks_day_one=tiedrank(day_1[ind])
    ranks_day_two=tiedrank(day_2[ind])
    return ranks_day_one, ranks_day_two


def computeWKendall(day_1,day_2,ranked_input=False):
    """Compute Kendall and WKendall only for active (nonzero) positions."""
    if ranked_input:
        rankX, rankY = day_1, day_2
    else:
        rankX, rankY = get_union_of_active_nodes(day_1, day_2)
    n = len(rankX)
    denomX, denomY = 0, 0
    denomXW, denomYW = 0, 0
    num, numW = 0, 0 

    for i in range(n):
        for j in range(i+1,n):
            weightXY= 1.0/rankY[i]+1.0/rankY[j]
            weightX=1.0/rankX[i]+1.0/rankX[j];
            weightY=1.0/rankY[i]+1.0/rankY[j];
            termX=np.sign(rankX[i]-rankX[j]);
            termY=np.sign(rankY[i]-rankY[j]);
            denomX=denomX+(termX)**2;
            denomY=denomY+(termY)**2;
            denomXW=denomXW+(termX)**2*weightX;
            denomYW=denomYW+(termY)**2*weightY;
            num=num+termX*termY;
            numW=numW+termX*termY*weightXY;

    Kendall=num/math.sqrt(denomX*denomY);
    WKendall=numW/math.sqrt(denomXW*denomYW);
    return [Kendall, WKendall]
