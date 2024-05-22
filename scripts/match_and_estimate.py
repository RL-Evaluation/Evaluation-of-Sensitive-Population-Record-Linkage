from utils.utils import *


def cluster_matching(sensitive_size_dic, public_cluster_size_dic, sensitive_bf_dic, public_bf_dic):
   '''Function for performing cluster matching
   Input: 
      - sensitive_size_dic, public_cluster_size_dic: dictionary, key is cluster ID and value is the cluster size
      - sensitive_bf_dic, public_bf_dic: dictionary, key is cluster ID, value is the encoded bloom filter for each cluster
   '''
   print('Start cluster matching...')
   #Compare every pair of BF
   similarity_dic = compareBF(sensitive_bf_dic, public_bf_dic)

   #Obtain the total number of edges in each cluster
   sensitive_edge_dic = getEdgeCount(sensitive_size_dic)
   public_edge_dic = getEdgeCount(public_cluster_size_dic)

   match_dic = {}

   #sort by highest similarity values
   sorted_similarity_dic = dict(sorted(similarity_dic.items(), key=lambda item: item[1], reverse=True))
   for bid, cid in sorted_similarity_dic.keys():
      #get the number of matched records
      n = min(sensitive_size_dic[bid], public_cluster_size_dic[cid])

      assert n >= 0

      #only consider clusters with size larger than 1
      if n > 1:
        match_dic[(bid, cid)] = n
        public_cluster_size_dic[cid] -= n
        sensitive_size_dic[bid] -= n

   return match_dic, sensitive_edge_dic, public_edge_dic


def estimate_linkage_quality(match_dic, sensitive_edge_dic, public_edge_dic):
  '''Function for Estimating Linkage Quality
  '''
  print('Estimate linkage quality...')
  #Initialise TP, FP and FN estimations
  ETP = 0
  EFP = 0
  EFN = 0

  for n in match_dic.values():
     ETP = ETP + n*(n-1) / 2
    
  EFP = sensitive_edge_dic - ETP
  EFN = public_edge_dic - ETP

  #calculate estimated Precision and Recall
  EPrecision = round(ETP / sensitive_edge_dic, 2)
  ERecall = round(ETP / public_edge_dic, 2)

  return ETP, EFP, EFN, EPrecision, ERecall



