import pandas as pd
from utils.utils import *
from itertools import combinations
from utils.config import *

def gt_evaluate(year, sensitive_df, public_df, match_dic):
    '''Calculate the percentage of census to birth ground truth links identified with BF based cluster matching

       Input: 
       - year: int, Census year
       - sensitive_df: DataFrame, sensitive clusters 
       - public_df: DataFrame, public clusters 
       - match_dic: Dictionary, Matching result generated from cluster matching
    '''
    #remove singletons
    filtered_birth = remove_singleton_df(sensitive_df, 'linkage_cluster_id')
    filtered_census = remove_singleton_df(public_df, 'c_gt_cluster_id')

    gt = pd.read_csv(gt_path + str(year)+".csv")
    gt = pd.merge(gt, filtered_birth, left_on = 'birth_id', right_on = 'birth_id', how = 'inner')
    gt = pd.merge(gt, filtered_census, left_on = 'census_id', right_on = 'census_id', how = 'inner')
    gt_count = gt.shape[0]
    
    assert gt_count != 0

    #Initialise TP value
    TP = 0

    #Count the number of cluster pairs identified in cluster matching result
    for _, row in gt.iterrows():
        cluster_id = row['linkage_cluster_id']
        hid = row['c_gt_cluster_id']
        if (cluster_id, hid) in match_dic:
            TP += 1

    #Calculate recall value 
    recall = round(TP/gt_count, 2)

    return recall




def sibling_gt_evaluate(star_threshold, sensitive_df):
    '''Calculate linkage quality using sibling ground truth data in birth dataset
    
       Input:
       - star_threshold: float, similarity threshold used in the group linkage algorithm
       - sensitive_df: DataFrame, containing clusters linked by demographers as ground truth and clusters to be evaluated
    '''
    #Set precision and recall as 1 and 0 for clusters generated with threshold value=0.5 to save the execution time, only applied for this algorithm because all records belong to a single cluster
    if star_threshold==0.5:
        precision = 0
        recall = 1
        return precision, recall

    #Initialise pair sets for algorithm linked clusters and ground truth clusters
    cluster_pairs=[]
    gt_pairs=[]
    for _,g in sensitive_df.groupby(['linkage_cluster_id']):
        sort_g = g.sort_values(by=['birth_id'])['birth_id'].tolist()
        pair = list(combinations(sort_g, 2))
        cluster_pairs.extend(pair)
    cluster_pairs = set(cluster_pairs)

    for _,g in sensitive_df.groupby(['b_gt_cluster_id']):
        sort_g = g.sort_values(by=['birth_id'])['birth_id'].tolist()
        pair = list(combinations(sort_g, 2))
        gt_pairs.extend(pair)
    gt_pairs = set(gt_pairs)

    #Set the number of pairs appearing in both sets as true positive
    TP = len(cluster_pairs.intersection(gt_pairs))
    FP = len(cluster_pairs - gt_pairs)
    FN = len(gt_pairs - cluster_pairs)

    #Calculate Precision and Recall
    precision = round(TP / (TP + FP), 2)
    recall = round(TP / (TP + FN), 2)

    return precision, recall



