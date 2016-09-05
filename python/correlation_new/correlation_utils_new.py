import operator
import numpy as np
import correlation_computer as cc
import pandas as pd
import numexpr as ne

def compute_correlation_sequential(centrality_df, corr_type='spearman', top_k=0, verbose=False, num_of_threads=1):
    """"Wrapper function for sequential correlation computing. 
    'centrality_maps' contains consecutive intervals, on which the correlations are computed in a sequential manner."""
    ne.set_num_threads(num_of_threads)
    dfs_for_computation = order_by_centrality(centrality_df, top_k)
    corrs = []
    for i in range(1, len(list(centrality_df))):
        if corr_type == 'pearson':
            corrs.append(cc.corr_pearson(dfs_for_computation[i-1], dfs_for_computation[i]))
        elif corr_type=='kendalltau':
            corrs.append(cc.corr_kendalltau(dfs_for_computation[i-1], dfs_for_computation[i]))
        elif corr_type=='weighted_kendalltau':
            corrs.append(cc.corr_weighted_kendalltau(dfs_for_computation[i-1], dfs_for_computation[i]))
        else:
            corrs.append(cc.corr_spearman(dfs_for_computation[i-1], dfs_for_computation[i]))
    if verbose:
        print '%s computation FINISHED.' % corr_type
    return np.array(corrs)


def compute_correlation_pairwise(centrality_df_1, centrality_df_2, corr_type='spearman', top_k=0, verbose=False, num_of_threads=1):
    """"Wrapper function for pairwise correlation computing. 
    'centrality_maps_1' and 'centrality_maps_2' contain consecutive intervals, on which the correlations are computed in a pairwise manner."""
    ne.set_num_threads(num_of_threads)
    if len(list(centrality_df_1)) != len(list(centrality_df_2)):
        raise RuntimeError('The length of the centrality maps does not match!')
    dfs_for_computation_1 = order_by_centrality(centrality_df_1, top_k)
    dfs_for_computation_2 = order_by_centrality(centrality_df_2, top_k)
    corrs = []
    for i in range(0, len(list(centrality_df_1))):
        if corr_type == 'pearson':
            corrs.append(cc.corr_pearson(dfs_for_computation_1[i], dfs_for_computation_2[i]))
        elif corr_type == 'kendalltau':
            corrs.append(cc.corr_kendalltau(dfs_for_computation_1[i], dfs_for_computation_2[i]))
        elif corr_type == 'weighted_kendalltau':
            corrs.append(cc.corr_weighted_kendalltau(dfs_for_computation_1[i], dfs_for_computation_2[i]))
        else:
            corrs.append(cc.corr_spearman(dfs_for_computation_1[i], dfs_for_computation_2[i]))
    if verbose:
        print '%s computation FINISHED.' % corr_type
    return np.array(corrs)



def order_by_centrality(centrality_df, top_k):
    """Preprocess a centrality map."""
    dfs_for_computation = []
    num_of_intervals = len(list(centrality_df))
    for i in range(num_of_intervals):
        preprocessed = topk_filter_and_order(centrality_df['rank_'+str(i)], i, top_k)
        dfs_for_computation.append(preprocessed)
    return dfs_for_computation


def topk_filter_and_order(origi_df, i, top_k):
    """Extract the first top_k node with highest centrality values"""
    sorted_df=pd.DataFrame(origi_df).sort('rank_'+str(i),ascending=False)
    if top_k == 0 or top_k >= len(origi_df):
        return sorted_df
    else:
        return sorted_df.head(n=top_k)