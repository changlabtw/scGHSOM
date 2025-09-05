import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import argparse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data_processing')))
import get_ghsom_dim
import numpy as np

# ============ 參數解析 ============
parser = argparse.ArgumentParser(description='Cluster Feature Map Dashboard')
parser.add_argument('--data', type=str, required=True)
parser.add_argument('--tau1', type=float, default=0.1)
parser.add_argument('--tau2', type=float, default=0.01)
parser.add_argument('--feature', type=str, default='mean')
args = parser.parse_args()

prefix = args.data
tau1 = args.tau1
tau2 = args.tau2
feature = args.feature

# ============ 載入資料 ============
path_feature = f'./applications/{prefix}-{tau1}-{tau2}/data/{prefix}_with_clustered_label-{tau1}-{tau2}.csv'
df_feature = pd.read_csv(path_feature)
path_label = f'./raw-data/label/{prefix}_label.csv'
df_label = pd.read_csv(path_label)
df_feature['label'] = df_label['label'].values
df = df_feature

# ============ 看有幾層 ============
layers, max_layer, number_of_digits = get_ghsom_dim.layers(f'{prefix}-{tau1}-{tau2}')

# ============ 動態生成 pathlist ============
pathlist = []
for i in range(1, max_layer + 1):
    col = f'clusterL{i}'
    if col in df.columns and df[col].nunique() > 1:
        pathlist.append(col)

df = df.fillna('')

# ============ 建立 Treemap ============
fig = px.treemap(
    df,
    path=pathlist,
    color=feature,
    color_continuous_scale='RdBu',
    branchvalues='remainder',
)

# ============ Dash App ============
app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        dcc.Graph(id='treemap', figure=fig, style={'height': '90vh'})
    ], style={'width': '60%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='pie-chart'),
        dcc.Graph(id='feature-bar')
    ], style={'width': '35%', 'display': 'inline-block', 'verticalAlign': 'top'})
])

# ============ Callback ============
@app.callback(
    [Output('feature-bar', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('treemap', 'clickData')]
)
def update_bar(clickData):
    if clickData is None:
        raise dash.exceptions.PreventUpdate

    clicked_id = clickData['points'][0]['id'].rstrip('/')
    levels = clicked_id.split('/')
    depth = len(levels)
    last_cluster = levels[-1]

    target_col = f'clusterL{depth}'
    mask = df[target_col] == last_cluster
    sub_df = df[mask]
    out_df = df[~mask]

    if sub_df.empty:
        return go.Figure(), go.Figure()

    feature_cols = [col for col in df.columns if col not in pathlist + 
                    ['Event', 'label', 'clustered_label', 'x_y_label', 'point_x', 'point_y', 'mean', 'median']]

    sig_scores = {}
    cluster_col = f'clusterL{depth}'
    cluster_means_df = df.groupby(cluster_col)[feature_cols].mean()
    all_clusters = cluster_means_df.index.tolist()

    for col in feature_cols:
        cluster_mean = sub_df[col].mean()
        sigma_I = np.sqrt(((sub_df[col] - cluster_mean) ** 2).sum() / len(sub_df))

        other_clusters = [c for c in all_clusters if c != last_cluster]
        m_c = cluster_means_df.loc[last_cluster, col]
        m_c_primes = cluster_means_df.loc[other_clusters, col]
        sigma_B = np.sqrt(((m_c - m_c_primes) ** 2).sum() / len(other_clusters))

        sig_scores[col] = sigma_B - sigma_I

    sorted_features = sorted(sig_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    top_features = [f[0] for f in sorted_features]
    top_means = [sub_df[f].mean() for f in top_features]

    fig_bar = go.Figure([
        go.Bar(
            x=top_means,
            y=top_features,
            orientation='h'
        )
    ])
    fig_bar.update_layout(
        title='Top 5 Significant Features',
        xaxis_title='Average Expression',
        yaxis_title='Protein Features',
        yaxis={'autorange': 'reversed'},
        height=400
    )

    label_counts = sub_df['label'].value_counts()
    total_count = label_counts.sum()
    label_counts = label_counts[label_counts / total_count >= 0.05]
    if len(label_counts) > 5:
        label_counts = label_counts[:5]
    others_count = total_count - label_counts.sum()
    if others_count > 0:
        label_counts['Others'] = others_count

    blue_colors = [
        'rgb(198,219,239)', 'rgb(158,202,225)', 'rgb(107,174,214)',
        'rgb(49,130,189)', 'rgb(8,81,156)', 'rgb(200,200,200)'
    ]

    fig_pie = go.Figure(
        go.Pie(
            labels=label_counts.index,
            values=label_counts.values,
            hole=0.5,
            marker_colors=blue_colors[:len(label_counts)],
            textinfo='percent+label',
            hoverinfo='label+percent+value'
        )
    )
    fig_pie.update_layout(title='Cell Type Distribution', height=400)

    return fig_bar, fig_pie

# ============ Run App ============
if __name__ == '__main__':
    app.run(debug=True)

















