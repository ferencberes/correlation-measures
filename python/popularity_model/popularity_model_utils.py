import sys, math
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

sys.path.insert(0,'../correlation_new')
import correlation_new.correlation_utils_new as cu

from popularity_model import PopularityModel

def rmse(original_values, model_values):
    return math.sqrt(mean_squared_error(original_values, model_values))

def test_stability_for_lambdas(lambdas, num_samples, corr_type, measure_id, popularity_model_parameters, origi_corrs, n_threads, output_prefix=None):
    num_of_users, num_of_days, p, p_overlap = popularity_model_parameters
    rmse_arr = []
    for selected_lambda in lambdas:
        for i in xrange(num_samples):
            sample_model = PopularityModel(num_of_users, num_of_days)
            scores_with_leaders = sample_model.get_centrality_with_markov(p, p_overlap, lambda_=selected_lambda)
            simulated_corrs = cu.get_correlations_from_matrix_for_act(scores_with_leaders, num_of_days, corr_type, n_threads=n_threads)
            rmse_arr.append([selected_lambda, corr_type, measure_id, rmse(origi_corrs, simulated_corrs)])
            print i
            if output_prefix != None:
                rmse_df = pd.DataFrame(np.array(rmse_arr), columns=["lambda","corr_type","measure_id","rmse"])
                rmse_df["rmse"] = rmse_df["rmse"].astype("float64")
                rmse_df.to_csv("%s_stability.%s" % (output_prefix,corr_type),index=False)
        print "lambda=%f finished" % selected_lambda
    rmse_df = pd.DataFrame(np.array(rmse_arr), columns=["lambda","corr_type","measure_id","rmse"])
    rmse_df["rmse"] = rmse_df["rmse"].astype("float64")
    return rmse_df

def summarize_stability_results(rmse_df, key=["lambda","corr_type","measure_id"]):
    mean_rmse = rmse_df.groupby(key).mean().reset_index()
    std_rmse = rmse_df.groupby(key).std().reset_index()
    rmse_stats = mean_rmse.merge(std_rmse,on=key,suffixes=("_mean","_std"))
    return rmse_stats
