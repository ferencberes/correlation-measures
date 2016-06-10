import math
import operator

############### functions ####################################
def avg(l):
    sum = 0.0
    for i in l:
        sum+= i
    return sum/len(l)

def avg_w(l):
    sum = 0.0
    N = len(l)
    for i in range(N):
        sum +=  (l[i]/(1.0+i))
    return sum

def szum(n):
    ret_val = 0.0
    for i in range(n):
        ret_val += 1.0/(i + 1)
    return ret_val

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

############################## Pearson correlation calculators ##############################
def correl(list_a, list_b, s):
    """Compute the numerator of the correlation formula"""
    n = len(list_a)
    avg_normal = float(n+1) / 2
    avg_weighted_a = avg_w(list_a)/s
    avg_weighted_b = avg_w(list_b)/s
    ret_val = 0.0
    ret_val_w = 0.0
    for i in range(n):
        w = 1.0/(i+1)
        #print list_a[i], list_b[i], avg_normal
        ret_val += (list_a[i] - avg_normal)*(list_b[i] - avg_normal)
        ret_val_w += ((list_a[i]- avg_weighted_a) * (list_b[i]-avg_weighted_b) * w)
    return ret_val, ret_val_w

def compute_corr(list_a, list_b):
    """Calculate (weighted) correlation for lists that hold the same elements"""
    n = len(list_a)
    h_n = szum(n)
    val, w_val = correl(list_a, list_b, h_n)
    val_a, w_val_a = correl(list_a, list_a, h_n)
    val_b, w_val_b = correl(list_b, list_b, h_n)
    return [val / math.sqrt(val_a * val_b),  w_val / math.sqrt(w_val_a * w_val_b)]

def corr(top_list_prev, top_list, sorted_id):
    list_a, list_b = proc_corr(top_list_prev, top_list, sorted_id)
    #print list_a
    #print list_b
    return compute_corr(list_a, list_b)

################################ Processors ############################
def proc_corr(l1, l2, sort_id):
    """Fill lists with scores ordered by the ranks in the second list"""
    list_a = []
    list_b = []
    for i in sort_id:
        list_b.append(l2[i])
        if i in l1:
            list_a.append(l1[i])
        else:
            list_a.append(0.0)
    for i in l1:
        if i not in l2:
            list_b.append(0.0)
            list_a.append(l1[i])
    return list_a, list_b

def pre_proc(centrality_map):
    """Return the original centrality map and an ordered index list"""
    sorted_map = sorted(centrality_map.items(), key=operator.itemgetter(1), reverse=True)
    ret_sort = []
    for item in sorted_map:
        ret_sort.append(item[0])
    return centrality_map, ret_sort
