import operator, sys
import numpy as np
import pearson_correlation_computer as pcc
import spearman_correlation_computer as scc

def compute_correlation_sequential(centrality_maps, corr_type='spearman', top_k=0, verbose=False):
    """"Wrapper function for sequential correlation computing:
    'centrality_maps' contains consecutive intervals, on which the correlations are computed in a sequential manner. 
    Return [correlation_values, ordered_id_list] tuple."""
    
    (maps_for_computation, ordered_id_list) = order_by_centrality(centrality_maps, corr_type, top_k, verbose=verbose)
    corrs = []
    if verbose:
        print '%s computation STARTED..' % corr_type
    for i in range(1, len(centrality_maps)):
        if verbose:
            print "[Day %i]" % i
        if corr_type == 'pearson':
            corrs.append(pcc.corr(maps_for_computation[i-1], maps_for_computation[i], ordered_id_list[i]))
        else:
            corrs.append(scc.corr(maps_for_computation[i-1], maps_for_computation[i], ordered_id_list[i]))
            #corrs.append(scc.corr_no_ties(maps_for_computation[i-1], maps_for_computation[i], ordered_id_list[i])) # it is for closed variance formula
    if verbose:
        print '%s computation FINISHED.' % corr_type
    #return (np.array(corrs), ordered_id_list)
    return np.array(corrs)


def order_by_centrality(centrality_maps, corr_type, top_k, verbose=False):
    """Preprocess a centrality map."""
    ordered_id_list = []
    maps_for_computation = []
    num_of_intervals = len(centrality_maps)
    if verbose:
        print "Preprocessing intervals STARTED.." 
    for i in range(num_of_intervals):
        if verbose:
            print "[Day %i]" % i
        if corr_type == 'pearson':
            preprocessed = pcc.pre_proc(map_topk_filter(centrality_maps[i], top_k))
        elif corr_type == 'spearman':
            preprocessed = scc.pre_proc(map_topk_filter(centrality_maps[i], top_k))
        else:
            raise RuntimeError("'%s' option is not implemented. Choose from 'pearson' or 'spearman'" % corr_type)
        ordered_id_list.append(preprocessed[1])
        maps_for_computation.append(preprocessed[0])
    if verbose:
        print "Preprocessing intervals FINISHED."
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


### UTILS ###
def read_score_file(file_name):
    f = open(file_name,'r')
    score_map = {}
    for line in f:
        splitted = line.rstrip().split(" ")
        score_map[int(splitted[0])] = float(splitted[1])
    f.close()
    return score_map


def write_to_file(file_name, corr_results):
    num_of_intervals = len(corr_results)
    f = open(file_name,'w')
    for i in range(num_of_intervals):
        f.write('%i %f %f\n' % (i, corr_results[i,0], corr_results[i,1]))
    f.close()


### MAIN ###
def main():
    centrality_folder = sys.argv[1]
    input_file_prefix = sys.argv[2]
    output_file = sys.argv[3]
    corr_type = sys.argv[4]
    num_of_intervals = int(sys.argv[5])
    if not corr_type in ['pearson', 'spearman']:
        raise RuntimeError("Only 'pearson' and 'spearman' correlations are cupported!")
    out_file = open(output_file, 'w')
    top_list_prev = []
    top_list = []
    ret_sort = []
    centrality_maps = []
    for day in range(num_of_intervals):
        centrality_maps.append(read_score_file(centrality_folder+"/"+input_file_prefix+"_%i.txt_s" % day))
    print "Score files were LOADED."
    correlations = compute_correlation_sequential(centrality_maps, corr_type=corr_type, top_k=0, verbose=True)[0]
    write_to_file(output_file, correlations)

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 6:
        main()
    else:
        print 'Usage: <centrality_data_folder> <input_file_prefix> <output_file> <kendall/corr> <num_of_intervals>'