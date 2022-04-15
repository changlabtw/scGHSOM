import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score, adjusted_rand_score, normalized_mutual_info_score, davies_bouldin_score, calinski_harabasz_score
import math
import argparse
import csv 

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--name', type=str, default = None)
parser.add_argument('--tau1', type=float, default = 0.1)
parser.add_argument('--tau2', type=float, default=0.01)

# parser.add_argument('--index', type=str, default = None)
args = parser.parse_args()

prefix = args.name
t1 = args.tau1
t2 = args.tau2

df = pd.read_csv('./applications/%s-%s-%s/data/%s_with_clustered_label-%s-%s.csv' % (prefix, t1, t2, prefix, t1, t2), encoding='utf-8')
label = pd.read_csv('./raw-data/label/%s_label.csv' % prefix, encoding='utf-8')
sample = pd.read_csv('./raw-data/%s.csv' % prefix, encoding='utf-8')
sample.drop(columns=['ID'], inplace=True)
celltype=label['type']

a_score = adjusted_rand_score(celltype, df['x_y_label']) 

#NMI
n_score = normalized_mutual_info_score(celltype, df['x_y_label'])
d_score = davies_bouldin_score(sample, df['x_y_label']) 

# Calculate CH
c_score = calinski_harabasz_score(sample, df['x_y_label'])
with open('./applications/%s-%s-%s/data/clustering_score.txt'% (prefix, t1, t2), 'w') as f:
    f.write('External---\n')
    f.write('ARI Scores: %.3f \n' % a_score)
    f.write('NMI Scores: %.3f \n' % n_score)
    f.write('Internal---\n')
    f.write('CH Scores: %.3f \n' % math.log10(c_score))
    f.write('DB Scores: %.3f' % d_score)
    f.write('leaf number:%s'%len(df.groupby('x_y_label').groups.keys()))


# Print the score
#print('S Scores: %.3f' % s_score)
print('External---')
print('A Scores: %.3f' % a_score)
print('N Scores: %.3f' % n_score)
 

# Print the score
#
print('Internal---')
print('CH Scores: %.3f' % math.log10(c_score))
print('DB Scores: %.3f' % d_score)

print('leaf num:', len(df.groupby('x_y_label').groups.keys()))
