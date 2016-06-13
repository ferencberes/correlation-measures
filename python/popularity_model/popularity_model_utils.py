import sys, math
from sklearn.metrics import mean_squared_error

sys.path.insert(0,'../correlation')
import correlation.correlation_utils as cu


def filter_active_users(A, num_of_days):
    num_users = A.shape[1]
    centrality_maps = []
    for i in range(num_of_days):
        centrality_maps.append({})
        for j in range(num_users):
            val = A[i,j]
            if val > 0.0:
                centrality_maps[i][j] = val
    return centrality_maps


def get_custom_correlations(A, num_of_days, corr_type='spearman'):
    """Return unweighted and weighted correlations"""
    return cu.compute_correlation_sequential(filter_active_users(A,num_of_days),corr_type=corr_type)


def rmse(original_values, model_values):
    return math.sqrt(mean_squared_error(original_values, model_values))


def get_result_for_lambda(proposed_lambda, pop_model, prob, prob_overlap, number_of_days, for_weighted):
    scores_with_leaders = pop_model.get_centrality_with_markov(prob, prob_overlap, lambda_=proposed_lambda)
    results = get_custom_correlations(scores_with_leaders, number_of_days)
    if for_weighted:
        model_spearman = list(results[:,1])
    else:
        model_spearman = list(results[:,0])
    return model_spearman, scores_with_leaders


def get_opt_lambda_for_model(proposed_lambdas, pop_model, prob, prob_overlap, number_of_days, original_corr_values, for_weighted=False):
    opt_lambda = proposed_lambdas[0]
    (opt_spearman, opt_scores) = get_result_for_lambda(opt_lambda, pop_model, prob, prob_overlap, number_of_days, for_weighted)
    opt_diff = rmse(original_corr_values, opt_spearman)
    #print opt_diff
    for i in range(1, len(proposed_lambdas)):
        current_lambda = proposed_lambdas[i]
        (current_spearman, current_scores) = get_result_for_lambda(current_lambda, pop_model, prob, prob_overlap, number_of_days, for_weighted)
        current_diff = rmse(original_corr_values, current_spearman)
        #print current_lambda, current_diff
        if current_diff < opt_diff:
            opt_lambda = current_lambda
            opt_spearman = current_spearman
            opt_scores = current_scores
            opt_diff = current_diff
    return (opt_lambda, opt_spearman, opt_diff, opt_scores)