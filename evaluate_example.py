"""
Simple script for testing bare-bones evaluation functionality
Requried a config.pkl file
"""
import sys
sys.path.append('PATH_TO/python_codebase/') # folder this file is in
## Read in test input
import cPickle as pickle
ground_truth_fname = "PATH_TO/simulated_spheroid_config.pkl"
ground_truth = pickle.load(open(ground_truth_fname))

## Make some test data
#  Hand pick some molecules from simulated_spheroid_config.pkl
results_true = {
    'C18H23N9O4S3_Na':[], #no abudnance -> []
    'C35H64O6_K':[],
    'C42H80NO7P_H':[],
    'C28H50N1O17_K':[],}
# create some false molecules
results_false={
    'C28H20N1O17_K':[],
    'C28H20N1O17_Na':[],
    'C28H20N1O17_H':[],
    }
results = results_true.copy()
results.update(results_false)
# Check for presence of moleucles
from pyims_simulate_evaluate import evaluate
e = evaluate.eval(ground_truth,results)
r_check =  e.check_all_results()
# Print results
for r in r_check:
    print r,r_check[r][0],r in results_true