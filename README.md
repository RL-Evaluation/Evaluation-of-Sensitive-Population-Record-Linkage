<div align="center">
  
**Privacy Preserving Evaluation of Sensitive Population Record Linkage Without Ground Truth Data**
</div>

This repository hosts the code and data used in an experimental evaluation, which applies a novel method to estimate the quality of group record linkage results in situations where no ground truth data are available.

Notably, our experimental results showed that the estimated quality evaluations are comparable to those obtained using ground truth data provided by domain experts.


## Overview of Our Evaluation Method

This experiment used four real-world census data sets (the public data sets) and one birth dataset (the census data set), and each cluster in both datasets was encoded into a vector representation using Bloom Filters. The process includes the following four key steps:

-  Compare pairs of encoded Bloom Filters from the census and birth datasets to obtain a similarity score for each compared cluster pair, and then apply a greedy many-to-many matching across the compared cluster pairs.

-  Calculate the estimated counts for true positives, false positives, and false negatives, which are then used to estimate precision (EP) and recall (ER).

-  Assessing the quality of cluster matching using the ground truth links records from census to birth 

-  Compare the quality estimations obtained in the second step with the supervised quality evaluation conducted using the sibling ground truth clusters in the birth dataset.

## Preparing
To reproduce the results of the paper, please set up the Python environment. The Python version used in this experiment:
```bash
Python 3.9.12
```

## Datasets
All data used in this experiment are placed in the /data folder:
```bash
/data/birth 

 - Each file tores records from the birth dataset with three columns: unique record ID, cluster ID linked with the group linkage algorithm and the cluster ID provided by domain experts. The files are filtered based on different parameter combinations as indicated by their names. For example, birth1871_0.8_10.csv contains records of children up to 10 years old in the census year 1871 and 0.8 is the clustering threshold used in group linkage method

 /data/census

  - Each file stores records from the census dataset, where each row contains two values: a unique record ID and a cluster ID. The file names indicate the census year and the maximum age of the records included.

  /data/encoded

  - Stores encoded clusters from birth and census dataset in dictionary form, where keys indicate different parameter settings

  /data/gt

  - Stores the ground truth links between the census and birth datasets, comprising two columns: unique birth record ID and census record ID.

```

## Running Code
```
run quick_start.ipynb
```

## Displaying Result
```
run plot.ipynb
```