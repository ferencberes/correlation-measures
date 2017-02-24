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

def corr_weighted_kendalltau(top_list_prev, top_list, use_fast=True):
    """Compute weighted Kendall's Tau correlation (based on custom implementation!).
    NOTE: Lists are DataFrame columns AND they must be sorted according to their value!!!"""
    # it is irrelevant whether we compute kendall for ranks or scores.
    list_a, list_b = proc_corr(top_list_prev, top_list)
    if len(list_a) != len(list_b):
        raise RuntimeError("The length of 'list_a' and 'list_b' must be the same!")
    if use_fast:
        return [fast_weighted_kendall(list_a, list_b)[1]]
    else:
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


### FastWKEndall ###

def merge_list(left,right, index_left, index_right, node_data,other_list):
    merged_list = []
    merged_index = []
    left_move = 0
    while ((len(left)>0) & (len(right)>0)):
        if left[0]>=right[0]:
            merged_list.append(left[0])
            merged_index.append(index_left[0])
            if (left[0] != right[0]) & (other_list[index_left[0]]!=other_list[index_right[0]]):
                node_data['con'][index_left[0]] += len(right)
                node_data['dis'][index_left[0]] += left_move
                node_data['con'][index_right[0]] += 1
            del left[0], index_left[0]
        else:
            left_move+=1
            merged_list.append(right[0])
            merged_index.append(index_right[0])
            node_data['dis'][index_right[0]]+=len(left)
            del right[0], index_right[0]
    
    if len(left)!=0:
        merged_list.extend(left)
        merged_index.extend(index_left)
        for i in index_left:
            node_data['dis'][i] += left_move
        
    elif len(right)!=0:
        merged_list.extend(right)
        merged_index.extend(index_right)
    
    return merged_list, merged_index


def count_ties(list_with_ties):
    same_as_next = [list_with_ties[i]==list_with_ties[i+1] for i in range(len(list_with_ties)-1)]+[False]
    count = 1
    tie_counts = []
    for i in range(len(list_with_ties)):
        if same_as_next[i] == True:
            count+=1
        else:
            tie_counts.extend([count for i in range(count)])
            count =1
    return tie_counts


def compute_avg_ranks(tie_counts):
    ranks=[]
    i=0
    while len(ranks)<len(tie_counts):
        rank = [(2*i+tie_counts[i]+1)/2 for j in range(tie_counts[i])]
        i+=tie_counts[i]
        ranks.extend(rank)
    return ranks


def count_con_dis_diff(list_to_sort,other_list):
    list_indices = range(len(list_to_sort))
    node_data = {'con':[0 for i in list_indices], 'dis':[0 for i in list_indices]}
    lists_to_merge = [[value] for value in list_to_sort]
    index_lists = [[i] for i in list_indices]

    while len(lists_to_merge)>1:
        merged_lists = []
        merged_indicies = []
        for i in range(int(len(lists_to_merge)/2)):
            merged, indices = merge_list(lists_to_merge[2*i],lists_to_merge[2*i+1],
                                         index_lists[2*i],index_lists[2*i+1], node_data, other_list)
            merged_lists.append(merged)
            merged_indicies.append(indices)
        if len(lists_to_merge) % 2 != 0:
            merged_lists.append(lists_to_merge[-1])
            merged_indicies.append(index_lists[-1])
        lists_to_merge = merged_lists
        index_lists = merged_indicies
    tie_counts = count_ties(lists_to_merge[0])
    rank_B = compute_avg_ranks(tie_counts)
    return_data = pd.DataFrame({'index':index_lists[0], 'rank_B':rank_B})
    return_data.sort_values('index', inplace=True)
    return_data.set_index('index', inplace=True)
    return_data['concordant']=node_data["con"]
    return_data['discordant']=node_data["dis"]
    return return_data


def fast_weighted_kendall(list_a, list_b):
    """Weighted Kendall's Tau O(n*logn) implementation. The input lists should contain all nodes."""
    data_table = pd.DataFrame({'A':list_a, 'B':list_b})
    data_table['rank_A'] = tiedrank(list_a)
    data_table = data_table.sort_values(['A', 'B'], ascending=False)
    data_table.reset_index(inplace=True,drop=True)
    list_to_sort=list(data_table['B'])
    other_list = list(data_table['A'])
    con_dis_data = count_con_dis_diff(list_to_sort,other_list)
    data_table = pd.concat([data_table,con_dis_data], axis=1)
    numW = sum(data_table.apply(lambda x: 1/x['rank_A']*(x['concordant']-x['discordant']), axis=1))
    denomX = sum(data_table.apply(lambda x: 1/x['rank_A']*(x['concordant']+x['discordant']), axis=1))
    denomY = sum(data_table.apply(lambda x: 1/x['rank_B']*(x['concordant']+x['discordant']), axis=1))
    return data_table, numW/math.sqrt(denomX*denomY)
