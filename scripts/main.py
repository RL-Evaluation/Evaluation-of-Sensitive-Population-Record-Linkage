import time
import pandas as pd
from scripts.match_and_estimate import *
from scripts.evaluate import *
from utils.config import *

def run(star_threshold, year, max_age, hash_num):
  '''Fetching and matching clusters from census and birth dataset;
     Estimate cluster matching quality 
     Calculate matching quality based on ground truth 

     Input:
       - star_threshold: threshold used in cluster matching algorithm
       - year: census year
       - max_age: maximum age to filter
       - hash_num: the number of hash functions used in bloom filter 
  '''
  #get both public and sensitive cluster IDs to compare
  sensitive_df = pd.read_csv(s_path+str(year)+'_'+str(star_threshold)+'_'+str(max_age)+'.csv')
  public_df = pd.read_csv(p_path+str(year)+'_'+str(max_age)+'.csv')

  #get encoded clusters from both public and sensitive dataset 
  filtered_sensitive_bf_dict, filtered_public_bf_dict = load_bf_collection(star_threshold, year, max_age, hash_num)

  # get the time to start matching and evaluation
  start_time = time.time()

  #get cluster size for both birth and census dataset
  sensitive_size_dic = sensitive_df['linkage_cluster_id'].value_counts().to_dict()
  public_size_dic = public_df['c_gt_cluster_id'].value_counts().to_dict()

  #matching clusters
  match_dic, sensitive_edges_dic, public_edges_dic = cluster_matching(sensitive_size_dic, public_size_dic, filtered_sensitive_bf_dict, filtered_public_bf_dict)
  
  #calculate recall based on census to birth ground truth matches
  gt_recall = gt_evaluate(year, sensitive_df, public_df, match_dic)

  #estimate linkage quality
  ETP, EFP, EFN, EPrecision, ERecall = estimate_linkage_quality(match_dic, sensitive_edges_dic, public_edges_dic)

  #calculate linkage quality using the sibling ground truth data in birth dataset
  supervised_prec, supervised_rec = sibling_gt_evaluate(star_threshold, sensitive_df)

  # run time for cluster matching and linkage estimation
  duration = time.time() - start_time

  print(f'Estimated Precision: {EPrecision}')
  print(f'Estimated Recall: {ERecall}')
  print(f'Supervised Precision: {supervised_prec}')
  print(f'Supervised Recall: {supervised_rec}')
  print(f"Census-to-birth GT Recall: {gt_recall}")
  
  print("Total runtime required for matching and evaluation: %.2f sec" % (duration))
  return (EPrecision, ERecall, supervised_prec, supervised_rec, gt_recall, ETP, EFP, EFN)