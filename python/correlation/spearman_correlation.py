#!/usr/bin/python

import math
import pearson_correlation as pearson

############################## Spearman correlation calculators ##############################
def correl_var(n, s):
    """Variance calculator for Spearman with. No ties enabled!"""
    avg = float(n+1) / 2    
    avg_weighted = pearson.avg_w(range(1,n+1))/s
    ret_val = 0.0
    ret_val_w = 0.0
    for i in range(n):
        w = 1.0/(i+1)
        ret_val += math.pow(i+1 - avg,2)
        ret_val_w += (math.pow(i+1 - avg_weighted,2) * w)
    return ret_val, ret_val_w

def compute_corr(list_a, list_b):
    """Correlation calculator for Spearman with. No ties enabled!"""
    n = len(list_a)
    h_n = pearson.szum(n)
    val, w_val = pearson.correl(list_a, list_b, h_n)
    var, w_var = correl_var(n, h_n)
    return [val / var, w_val / w_var]

def corr_no_ties(top_list_prev, top_list, sorted_id):
    """Calculate (weighted) Spearman correlation for dictioneries. No ties enabled! """
    list_a, list_b = proc_corr(top_list_prev, top_list, sorted_id)
    #print list_a
    #print list_b
    return compute_corr(list_a, list_b)

def corr(top_list_prev, top_list, sorted_id):
    """Calculate (weighted) correlation for dictioneries that hold the active elements from each day"""
    list_a, list_b = proc_corr(top_list_prev, top_list, sorted_id)
    #print list_a
    #print list_b
    return pearson.compute_corr(list_a, list_b)

################################ Processors ############################
def proc_corr(l1, l2, sort_id):
    """Create list with the same elements from active elements from two dictionaries"""
    list_a = []
    list_b = []
    n1 = len(l1) + 1.0 # number of vertices in last interval + 1
    n2 = len(l2) + 1.0 # number of vertices in current interval + 1
    sum_a = 0.0
    sum_b = 0.0
    counter_a = 0
    counter_b = 0
    for i in sort_id:
        if not i in l1:
            counter_a += 1
            sum_a += n1
            n1 += 1
    for i in l1:
        if i not in l2:
            counter_b += 1
            sum_b += n2
            n2 += 1

    if counter_a > 0:
        avg_a = sum_a / counter_a
    else:
        avg_a = 0.0

    if counter_b > 0:
        avg_b = sum_b / counter_b
    else: 
        avg_b = 0.0

    for i in sort_id:
        list_b.append(l2[i])
        if i in l1:
            list_a.append(l1[i])
        else:
            list_a.append(avg_a) # tie on last position
    for i in l1:
        if i not in l2:
            list_b.append(avg_b) # tie on last position
            list_a.append(l1[i])
    return list_a, list_b

def pre_proc(centrality_map):
    """Return the position map and an ordered index list"""
    print "spearman pre_proc"
    ret_val, ret_sort = pearson.pre_proc(centrality_map)
    return  centrality_to_position(ret_val, ret_sort)

def centrality_to_position(ret_val, ret_sort):
    """Convert centrality based dictionary to position based dictionary"""
    ret_pos_val = {}
    summed_rank = 0.0
    i = 0
    j = 1
    N = len(ret_sort)
    for j in range(1,N+1):
        summed_rank += j
        if j == N or ret_val[ret_sort[j-1]] > ret_val[ret_sort[j]]:
            for k in range(i,j):
                ret_pos_val[ret_sort[k]] = summed_rank / (j-i)
            i = j
            summed_rank = 0.0
    return ret_pos_val, ret_sort
    