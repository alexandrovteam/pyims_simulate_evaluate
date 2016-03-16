__author__ = 'palmer'
import numpy as np

def get_true_sumformula_adduct_list(ground_truth):
    """
    Gets a global list of sumformula_adduct from layers
    :return:
        a list
    """
    layer_names = ground_truth['layers_list'].keys()
    sf_a_list = []
    layer_names = ground_truth['layers_list'].keys()
    for layer_name in layer_names:
        for sf_a in ground_truth['layers_list'][layer_name]['sf_list']:
            sf_a_list.append(sf_a['sf_a'])
    sf_a_list = list(set(sf_a_list))
    return sf_a_list

def get_sumformula_adduct_abudnace(ground_truth,sf_a):
    """
    get abundance for a sumformula_adduct
    :param ground_truth:
        true spatial abundances
    :param sf_a:
        sf_a to search for
    :return:
        a 2D array of abundances
    """
    layer_names = ground_truth['layers_list'].keys()
    n_y,n_x = np.shape(ground_truth['layers_list'][layer_names[0]]['image'])
    mol_im = np.zeros(n_y,n_x)
    for layer_name in layer_names:
        if sf_a in ground_truth['layers_list'][layer_name]['sf_list']:
            im = ground_truth['layers_list'][layer_name]['image']
            im *= ground_truth['layers_list'][layer_name]['sf_list']["mult"][0]
            mol_im += im
    return mol_im

def score_spatial(template_im,test_im):
    """
    Calculate some metrics of spatial matching
    :param template_im:
        ground truth image
    :param test_im:
        test image
    :return:
        tuple of scores
    """
    print "Spatial scoring not implemented"
    scores = (0,0)
    return scores


class Evaluate():
    """
    Class for comparing spatial metaboloics annotations against a ground truth.
    Designed for data built with the simulator from pyims_simulate_evaluate
    Reads a ground truth and a set of results and produces various reports
    """
    def __init__(self,ground_truth,results):
        """
        Opens a ground truth layers and a results dict
        :param layers:
            see pyims_simulate_evaluate.simulate for description of layers
        :param results:
            Results should contain a dictionary of metabolite_adduct name detected each with a spatial distribution.
            If no abundance was calculated then an empty array should be passed
        """
        # Ground truth
        self.ground_truth=ground_truth
        layer_names = ground_truth['layers_list'].keys()
        self.n_y,self.n_x = np.shape(ground_truth['layers_list'][layer_names[0]]['image'])
        self.true_sf_a = get_true_sumformula_adduct_list(ground_truth)
        # Results
        self.results = results

    def check_result(self,sf_a,distribution=[]):
        """
        Checks a single ion + distribution against the ground truth
        :param sf_a:
            string: sumformula_adduct
        :param distribution:
            optional: image of distribution
        :return:
            tuple of scores
        """
        in_global_list = sf_a in self.true_sf_a
        if distribution == []:
            return (in_global_list,[])
        assert np.shape(distribution) == (self.n_y,self.n_x) #check image dimensions match
        ground_truth_im = get_sumformula_adduct_abudnace(self.ground_truth,sf_a)
        spatial_scores=score_spatial(ground_truth_im,distribution)
        return (in_global_list,spatial_scores)

    def check_all_results(self):
        """
        Iterate over all results and check how good they are
        :return:
            a dictionary of scores
        """
        results_dict = {}
        for sf_a in self.results:
            results_dict[sf_a] = self.check_result(sf_a,self.results[sf_a])
        return results_dict