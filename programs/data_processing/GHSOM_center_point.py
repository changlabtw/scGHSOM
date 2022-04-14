from fractions import Fraction
import pandas as pd
import argparse
import plotly.express as px


parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--name', type=str, default = None)
parser.add_argument('--tau1', type=float, default = 0.1)
parser.add_argument('--tau2', type=float, default=0.01)


# parser.add_argument('--index', type=str, default = None)
args = parser.parse_args()

prefix = args.name
t1 = args.tau1
t2 = args.tau2
source_path = args.name.replace('-item-seq','')

def GHSOM_center_point(df):
    Bx = By = 1
    Bx_list = []
    By_list = []
    Point_list = []
    for i in range(df.shape[0]):
        Bx = Bx * (Fraction(1, df.loc[i]['XDIM']))
        Bx_list.append(Bx)
        By = By * (Fraction(1, df.loc[i]['YDIM']))
        By_list.append(By)

        Point = [ Bx * df.loc[i]['X'], By * df.loc[i]['Y']]
        Point_list.append(Point)

    Px = Fraction(0, 1)
    for j in Point_list:
        Px = Px + j[0]
    Px = Px + Bx_list[-1]* 1/2

    Py = Fraction(0, 1)
    for j in Point_list:
        Py = Py + j[1]
    Py = Py + By_list[-1]* 1/2
    return ([Px,Py])

df_source = pd.read_csv('./applications/%s/data/%s_with_clustered_label-%s-%s.csv' % (source_path, prefix,t1,t2))

#df_source = pd.read_csv('./applications/%s/data/%s_with_coordinate_representation.csv' % (source_path,prefix))
def map_cluster_to_ghsom(df_source):
    point_label_x = []
    point_label_y = []
    for i in df_source['clustered_label']:
        # print(i.split(';'))
        pointarray = i.split(';')
        point = []
        dimension_list = []
        for i in range(0,len(pointarray),4):
            # pointarray[i] = int(pointarray[i])
            dimension_list.append([pointarray[i],pointarray[i+1],pointarray[i+2],pointarray[i+3]])
        # print(dimension_list)
        dimension_df = pd.DataFrame(dimension_list,columns=['XDIM', 'YDIM', 'X', 'Y'])
        # print(dimension_df)

        point = GHSOM_center_point(dimension_df.astype('int64'))
        # print([point])
        point_label_x.append(point[0])
        point_label_y.append(point[1])
    df_source['point_x'] = point_label_x
    df_source['point_y'] = point_label_y
    
    return(df_source)
    
df_source = map_cluster_to_ghsom(df_source)
#df_raw['point_x'] = df_source['point_x']
#df_raw['point_y'] = df_source['point_y']
df_source.to_csv('./applications/%s/data/%s_with_clustered_label-%s-%s.csv' % (source_path, prefix,t1,t2), index=False)
'''
leaf = df_source.groupby('leaf')
leaf_group = leaf.groups.keys()
x = []
y = []
for g in leaf_group:
  filter = (df_source["leaf"] == g)
  x.append(float(df_source[filter].iloc[0,-4]))
  y.append(float(df_source[filter].iloc[0,-3]))

leaf_size = leaf.size()
leaf_mean = leaf.mean()['mean'].tolist()

df = pd.DataFrame()
df['leaf'] = leaf_size.index
df['size'] = leaf_size.values
df['point_x'] = x
df['point_y'] = y
df['mean'] = leaf_mean

listlen = []
for i in df['leaf']:
  listlen.append(len(i)/4)

df['level number'] = listlen

fig = px.scatter(df, x="point_x", y="point_y",
	         size="size", color="mean", hover_data=["leaf"])
fig.show()
of.plot(fig, filename=('./applications/%s/graphs/%s_bubblemap.html' % (prefix, prefix)))
'''
print(df_source)




