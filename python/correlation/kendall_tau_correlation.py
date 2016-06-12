#!/usr/bin/python

import math
import pearson_correlation as pearson

def sign(x,y):
    if x > y:
        return 1
    elif x < y:
        return -1
    else:
		return 0


def min_val(l):
    ret_val = 0;
    first = True
    for i in l:
        num = l[i]
        if first:
            ret_val = num
            first = False
        if ret_val > num:
            ret_val = num
	return ret_val


def kendall_tau_parts(list_a, list_b, list_a_sorted): 
    ret_val = 0
    ret_val_w = 0
    ret_val_a = 0
    ret_val_a_w = 0
    ret_val_b = 0
    ret_val_b_w = 0
    N = len(list_a)
    for i in range(N):
        for j in range(N)[i+1:]:
            #print i,j
            w = ((1.0/(i+1))+(1.0/(j+1)))
            sign_a = sign(list_a[i],list_a[j])
            sign_a_sorted = sign(list_a_sorted[i],list_a_sorted[j])
            sign_b = sign(list_b[i],list_b[j])
            ret_val += sign_a*sign_b # normal
            ret_val_w += sign_a*sign_b*w # weighted
            ret_val_a += sign_a_sorted*sign_a_sorted # normal for list_a_sorted
            ret_val_a_w += sign_a_sorted*sign_a_sorted*w # weighted for list_a_sorted
            ret_val_b += sign_b*sign_b # normal for list_b
            ret_val_b_w += sign_b*sign_b*w # weighted for list_b
    return ret_val, ret_val_w, ret_val_a, ret_val_a_w, ret_val_b, ret_val_b_w


def kendall_tau_all(list_a, list_b): # both lists are preprocessed by kendal_multi_preproc.py
    sorted_a = sorted(list_a, reverse=True)
    val, w_val, val_a, w_val_a, val_b, w_val_b = kendall_tau_parts(list_a, list_b, sorted_a)
    return [val/math.sqrt(val_a*val_b), w_val/ math.sqrt(w_val_a*w_val_b)]


def kendall_tau(top_list_prev, top_list, sorted_id):
    list_a, list_b = proc_kendall(top_list_prev, top_list, sorted_id)
    return kendall_tau_all(list_a, list_b)


def proc_kendall(l1, l2, sort_id):
    list_a = []
    list_b = []
    n1 = min_val(l1) - 1
    n2 = min_val(l2) - 1
    for i in sort_id:
        # current toplist contains nodes in descending order based on centrality scores
        list_b.append(l2[i])
        if i in l1:
            list_a.append(l1[i])
        else:
            list_a.append(n1)
    for i in l1:
        if i not in l2:
            list_b.append(n2)
            list_a.append(l1[i])
            # previous toplist is not sorted. Later we must sort it for the variance (e.g.: kendall_tau_all()).
	return list_a, list_b


def pre_proc(centrality_map):
    """Return the original centrality map and an ordered index list."""
    return  pearson.pre_proc(centrality_map)
