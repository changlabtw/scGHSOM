import plotly.express as px
import plotly.offline as of
import pandas as pd
import numpy as np
import argparse


parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--name', type=str, default = None)
# parser.add_argument('--index', type=str, default = None)
args = parser.parse_args()

prefix = args.name

label_file = pd.read_csv('./applications/%s/data/%s_with_clustered_label.csv' % (prefix, prefix), encoding='utf-8')
label_file = label_file.fillna('')

pathlist=['clusterL1','clusterL2','clusterL3']
print(label_file)

fig = px.treemap(label_file, path=pathlist,
          color = 'Mean',
          color_continuous_scale = 'RdBu',
          )
fig.show()
of.plot(fig, filename=('./applications/%s/graphs/%s_map.html' % (prefix, prefix)))