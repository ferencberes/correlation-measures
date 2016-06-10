import operator
import numpy as np
import correlation.pearson_correlation_computer as pcc
import correlation.spearman_correlation_computer as scc

def compute_correlation_from_lists(list_1, list_2, corr_type='spearman', top_k=0, verbose=False):
    """"Wrapper function for sequential correlation computing. 
    'centrality_maps' contains consecutive intervals, on which the correlations are computed in a sequential manner. 
    Return [correlation_values, ordered_id_list] tuple."""
    
    (maps_for_computation, ordered_id_list) = order_by_centrality(list_1, list_2, corr_type, top_k)
    corr = 0.0
    if corr_type == 'pearson':
        corr = pcc.corr(maps_for_computation[0], maps_for_computation[1], ordered_id_list[1])
    else:
        corr = scc.corr(maps_for_computation[0], maps_for_computation[1], ordered_id_list[1])
        #corr = scc.corr_no_ties(maps_for_computation[0], maps_for_computation[1], ordered_id_list[1]) # it is for closed variance formula
    if verbose:
        print '%s computation FINISHED.' % corr_type
    return corr

def order_by_centrality(list_1, list_2, corr_type, top_k):
    """Preprocess a centrality map."""
    centrality_maps = [dict(zip(range(len(list_1)),list_1)),dict(zip(range(len(list_2)),list_2))]
    ordered_id_list = []
    maps_for_computation = []
    num_of_intervals = len(centrality_maps)
    for i in range(num_of_intervals):
        if corr_type == 'pearson':
            preprocessed = pcc.pre_proc(map_topk_filter(centrality_maps[i], top_k))
        elif corr_type == 'spearman':
            preprocessed = scc.pre_proc(map_topk_filter(centrality_maps[i], top_k))
        else:
            raise RuntimeError("'%s' option is not implemented. Choose from 'pearson' or 'spearman'" % corr_type)
        ordered_id_list.append(preprocessed[1])
        maps_for_computation.append(preprocessed[0])
    return (maps_for_computation, ordered_id_list)


def map_topk_filter(origi_map, top_k):
    """Extract the first top_k node with highest centrality values"""
    if top_k == 0 or top_k >= len(origi_map):
        return origi_map
    else:
        sorted_list = sorted(origi_map.items(), key=operator.itemgetter(1), reverse=True)
        filtered_map = {}
        for i in range(top_k):
            filtered_map[sorted_list[i][0]] = sorted_list[i][1]
        return filtered_map
        