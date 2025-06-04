import pandas as pd
import numpy as np
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, davies_bouldin_score, calinski_harabasz_score
import math
import argparse

# ============ 參數解析 ============
parser = argparse.ArgumentParser(description='Clustering evaluation script')
parser.add_argument('--name', type=str, required=True)
parser.add_argument('--tau1', type=float, default=0.1)
parser.add_argument('--tau2', type=float, default=0.01)
args = parser.parse_args()

prefix = args.name
t1 = args.tau1
t2 = args.tau2

# ============ 載入資料 ============
df = pd.read_csv(f'./applications/{prefix}-{t1}-{t2}/data/{prefix}_with_clustered_label-{t1}-{t2}.csv', encoding='utf-8')
label = pd.read_csv(f'./raw-data/label/{prefix}_label.csv', encoding='utf-8')
sample = pd.read_csv(f'./raw-data/{prefix}.csv', encoding='utf-8')
sample.drop(columns=['Event'], inplace=True)

celltype = label['label']

# ============ 外部指標：僅使用有 label 的細胞 ============
mask = ~celltype.isna()
new_df = df[mask].copy()
new_celltype = celltype[mask].copy()

# ARI & NMI (只用 new_df & new_celltype)
a_score = adjusted_rand_score(new_celltype, new_df['x_y_label']) 
n_score = normalized_mutual_info_score(new_celltype, new_df['x_y_label'])

# ============ 內部指標：使用所有細胞 ============
d_score = davies_bouldin_score(sample, df['x_y_label']) 
c_score = calinski_harabasz_score(sample, df['x_y_label'])

# ============ 輸出結果 ============
with open(f'./applications/{prefix}-{t1}-{t2}/data/clustering_score.txt', 'w') as f:
    f.write('External---\n')
    f.write('ARI Scores: %.3f \n' % a_score)
    f.write('NMI Scores: %.3f \n' % n_score)
    f.write('Internal---\n')
    f.write('CH Scores: %.3f \n' % math.log10(c_score))
    f.write('DB Scores: %.3f\n' % d_score)
    f.write('Leaf number (based on x_y_label in df): %s\n' % df['x_y_label'].nunique())

# ============ Print ============
print('External---')
print('ARI Scores: %.3f' % a_score)
print('NMI Scores: %.3f' % n_score)
print('Internal---')
print('CH Scores: %.3f' % math.log10(c_score))
print('DB Scores: %.3f' % d_score)
print('Leaf num:', df['x_y_label'].nunique())
