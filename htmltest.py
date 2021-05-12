import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc                  # 交互式组件
import dash_html_components as html                 # 代码转html
from dash.dependencies import Input, Output         # 回调


diseases = ['Brain_Cancer', 'Breast_Cancer', 'Leukemia', 'Lung_Cancer', 'Myeloma']

all_data = pd.read_csv('./applications/shinyEff-Sele/data/shinyEff-Sele_with_eff_sele_map.csv', encoding='utf-8')
all_data = all_data.fillna('')
brain_data = pd.read_csv('./applications/shinyEff-Sele_Brain_Cancer/data/shinyEff-Sele_Brain_Cancer_with_eff_sele_map.csv', encoding='utf-8')
brain_data = brain_data.fillna('')
breast_data = pd.read_csv('./applications/shinyEff-Sele_Breast_Cancer/data/shinyEff-Sele_Breast_Cancer_with_eff_sele_map.csv', encoding='utf-8')
breast_data = breast_data.fillna('')
leu_data = pd.read_csv('./applications/shinyEff-Sele_Leukemia/data/shinyEff-Sele_Leukemia_with_eff_sele_map.csv', encoding='utf-8')
leu_data = leu_data.fillna('')
lung_data = pd.read_csv('./applications/shinyEff-Sele_Lung_Cancer/data/shinyEff-Sele_Lung_Cancer_with_eff_sele_map.csv', encoding='utf-8')
lung_data = lung_data.fillna('')
mye_data = pd.read_csv('./applications/shinyEff-Sele_Myeloma/data/shinyEff-Sele_Myeloma_with_eff_sele_map.csv', encoding='utf-8')
mye_data = mye_data.fillna('')

pathlist = ['clusterL1','clusterL2','clusterL3']
fig = px.treemap(all_data, path=pathlist,
          color = 'efficacy',
          color_continuous_scale = 'RdBu',
          )


app = dash.Dash('Hello Dash', )
app.layout = html.Div(                              # dash布局
  children = [
      html.H1('Hello，Gene Cluster'),
      html.Div('''please pick one disease by the drop down list.'''),
      html.Div(children=[
          html.Div(children=[
              dcc.Dropdown(                       # 创建下拉菜单
                  id="choice_line",
                  options=[
                      {'label': 'ALL', 'value': 'all_data'},
                      {'label': diseases[0], 'value': 'fig2'},
                      {'label': diseases[1], 'value': 'fig3'},
                      {'label': diseases[2], 'value': 'fig4'},
                      {'label': diseases[3], 'value': 'fig5'},
                      {'label': diseases[4], 'value': 'fig6'},
                  ],
                  placeholder="choice",
              )
          ],style={"display":"inline-block","width":'100px',"height":"100px","position":"absolute","left":"40px","top":"200px"}),#用style确定绝对位置
          html.Div(children=[
              dcc.Graph(
                  id = 'graph'             # 这里没用figure是因为后面用了回调
              ),
          ],style={"display":"inline-block","width":"1000px","position":"absolute","left":"150px","top":"100px"}),
      ],style={"height":500,"width":1400}),
  ],style={'color': '#454545', 'fontSize': 14, }
)
@app.callback(Output('graph','figure'),[Input('choice_line', 'value')])
def update_figure(choice):
  print(choice)                                   # 打印验证一下，如果有多个Input，参数是列表
  if choice !='choice':
      fig = choice
  return fig

if __name__ =='__main__':
  app.run_server(debug=True)  


