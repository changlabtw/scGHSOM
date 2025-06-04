import plotly.express as px
import plotly.offline as of
import pandas as pd
import argparse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data_processing'))) #修改一
import get_ghsom_dim
import os

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--name', type=str, default = None)
parser.add_argument('--tau1', type=float, default = 0.1)
parser.add_argument('--tau2', type=float, default = 0.01)
parser.add_argument('--feature', type=str, default = 'mean')

args = parser.parse_args()

# 自動拼接完整 prefix
prefix = args.name
t1 = args.tau1
t2 = args.tau2
feature = args.feature

# 拼接帶參數的完整名字
full_name = f"{prefix}-{t1}-{t2}"

layers,max_layer,number_of_digits = get_ghsom_dim.layers(full_name)

pathlist = list()

df = pd.read_csv(f'./applications/{full_name}/data/{prefix}_with_clustered_label-{t1}-{t2}.csv', encoding='utf-8')
for i in range(1,max_layer+1):
    pathlist.append('clusterL'+str(i))

df = df.fillna('')

fig = px.treemap(df, path=pathlist,
          color = feature,
          color_continuous_scale = 'RdBu',
          branchvalues = 'remainder'
          )
os.makedirs(f'./applications/{full_name}/graphs/', exist_ok=True)
of.plot(fig, filename=(f'./applications/{full_name}/graphs/{prefix}_map.html'))
# fig.show()

