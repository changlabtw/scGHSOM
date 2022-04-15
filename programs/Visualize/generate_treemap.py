import plotly.express as px
import plotly.offline as of
import pandas as pd
import argparse
import get_ghsom_dim


parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--name', type=str, default = None)
parser.add_argument('--tau1', type=float, default = 0.1)
parser.add_argument('--tau2', type=float, default = 0.01)
parser.add_argument('--feature', type=str, default = 'mean')

# parser.add_argument('--index', type=str, default = None)
args = parser.parse_args()

prefix = args.name
t1 = args.tau1
t2 = args.tau2
feature = args.feature

layers,max_layer,number_of_digits = get_ghsom_dim.layers(prefix)
pathlist = list()


df = pd.read_csv('./applications/%s-%s-%s/data/%s_with_clustered_label-%s-%s.csv' % (prefix,t1,t2, prefix,t1,t2), encoding='utf-8')
for i in range(1,max_layer+2):
    pathlist.append('clusterL'+str(i))

df = df.fillna('')

fig = px.treemap(df, path=pathlist,
          color = feature,
          color_continuous_scale = 'RdBu',
          branchvalues = 'remainder'
          )
of.plot(fig, filename=('./applications/%s/graphs/%s_map.html' % (prefix, prefix)))
fig.show()


