import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import webbrowser
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

app = dash.Dash(__name__)

df = pd.read_csv('./applications/shinyEff-Sele/data/shinyEff-Sele_with_eff_sele_map.csv', encoding='utf-8')
print(df)
groupL1 = df.groupby('essential')
print(groupL1)
scatter = px.scatter(
    #groupL1.get_group("1x0"),
    df,
    x='efficacy', 
    y='selectivity', 
    color='clusterL1'
)

fig = go.Figure(scatter)
app.layout = html.Div([
        dcc.Graph(
            figure=fig,
            ),
        ]
        )


if __name__ == '__main__':
    app.run_server(debug=True)