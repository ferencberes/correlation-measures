import numpy as np
import math

### util functions ###

def reverse_sort(a):
    a.sort(axis=0)
    return a[::-1]

def list_subset(l,idx,exclusive=False):
    l_idx = [l[i] for i in idx] 
    if exclusive:
        return list(set(l)-set(l_idx))
    else:
        return l_idx

# TODO: MATLAB random binomial function was different???
def binornd(n,p):
    probs = np.zeros(n)
    #indeces = np.random.binomial(n,p,size=n)
    #for i in indeces:
    for i in range(n):
        if np.random.rand(1) < p:
            probs[i] = 1.0
    return probs

### model ###

class PopularityModel:

    def __init__(self, number_of_users, number_of_days, exponent=1.2, round_scores=True):
        """Initialize popularity model with the given power law exponent."""
        self.num_of_users = number_of_users
        self.num_of_days = number_of_days
        self.exponent = exponent
        # rounding scores can simulate ties
        self.round_scores = round_scores
        self.init_model()


    def init_model(self):
        # unknown popularity
        U = np.random.pareto(self.exponent, size=self.num_of_users)
        self.U = reverse_sort(U)
        # daily variations
        self.alpha = np.random.exponential(scale=1.0, size=(self.num_of_days, self.num_of_users))
        # daily centrality scores
        self.X = self.alpha * self.U


    def get_centrality_with_markov(self, p, p_overlap, lambda_=0.0):
        """Generate daily centrality score based on user activation probabilities. Define non-zero 'lambda_' for introducing leaders into the model!"""
        leader_index = lambda_
        m = self.num_of_days
        n = self.num_of_users
        intersection = p_overlap

        prob_set = np.zeros((m,n))
        Jaccard = np.zeros((m-1,1));
        q=np.zeros((m-1,1));
        u_index = range(n)
        intersection1 = np.zeros((m-1,1));

        for i in xrange(0,m-1):      
            Jaccard[i] = intersection[i] / (p[i]+p[i+1]-intersection[i])

            leader_fraction = intersection[i] * leader_index
            intersection1[i] = intersection[i] - leader_fraction
            q[i] = p[i] - leader_fraction
            
            leader_set = u_index[:int(math.ceil(n*leader_fraction))]
            user_set = list_subset(u_index,leader_set,exclusive=True)
            n1=len(user_set)
    
            # active users day 1
            if i==0:
                prob_set[i,leader_set] = np.ones(len(leader_set)) 
                prob_set[i,user_set] = binornd(n1,q[i]) # in Nelly code it was p(i) -> q[i] is the correct value!!!
    
            # active users day i+1
            p_mix1 = intersection1[i] / q[i]
            p_mix0 = (p[i+1]-intersection[i]) / (1-q[i])
            prob_set[i+1,leader_set] = np.ones(len(leader_set))
            prob_set[i+1,user_set] = prob_set[i,user_set] * binornd(n1,p_mix1) + (1-prob_set[i,user_set]) * binornd(n1,p_mix0);
        if self.round_scores:
            return np.ceil(self.X * prob_set)
        else:
            return self.X * prob_set