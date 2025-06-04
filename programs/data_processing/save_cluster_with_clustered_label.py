import numpy as np
import pandas as pd
from pandas import ExcelWriter
from fractions import Fraction
#import pymongo
import argparse
import get_ghsom_dim

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--name', type=str, default=None)
parser.add_argument('--tau1', type=float, default=0.1)
parser.add_argument('--tau2', type=float, default=0.01)
parser.add_argument('--index', type=str, default=None)

args = parser.parse_args()

prefix = args.name
t1 = args.tau1
t2 = args.tau2
index = args.index
file = f'{prefix}-{t1}-{t2}'

layers, max_layer, number_of_digits = get_ghsom_dim.layers(file)
df_source = pd.read_csv('./raw-data/%s.csv' % prefix, encoding='utf-8')

median = df_source.iloc[:, 1:].median(axis=1)
mean = df_source.iloc[:, 1:].mean(axis=1)

df_source['mean'] = mean
df_source['median'] = median
df_source['clustered_label'] = np.nan
df_source['x_y_label'] = np.nan
for i in range(1, max_layer + 1):
    df_source['clusterL' + str(i)] = np.nan

def get_cluster_flag(text_file):
    get_cluster_flag = [i for i, x in enumerate(text_file) if x == '$POS_X']
    get_cluster_flag.append(len(text_file) + 1)
    return get_cluster_flag

def format_cluster_info_to_dict(unit_file_name, source_data, saved_data_type=None, structure_type=None, parent_name=None, parent_file_position=None, parent_clustered_string=None, x_y_clustered_string=None):
    Groups_info = []
    unit_file_path = ('./applications/%s/GHSOM/output/%s/' % (file, file)) + unit_file_name + '.unit'
    print(unit_file_path)
    text_file = open(unit_file_path).read().split()
    flag = get_cluster_flag(text_file)

    if 'lvl' in unit_file_name:
        layer_index = int(unit_file_name.split('lvl')[1][0])
    else:
        layer_index = 1

    XDIM = text_file[text_file.index('$XDIM') + 1]
    YDIM = text_file[text_file.index('$YDIM') + 1]
    map_size = int(XDIM) * int(YDIM)

    if parent_name is None:
        parent_name = 'Root'
    else:
        parent_name = str(parent_name) + '-' + str(parent_file_position)

    if x_y_clustered_string is None:
        x_y_clustered_string = ''

    if parent_clustered_string is None:
        parent_clustered_string = ''

    for i, map_index in zip(range(len(flag) - 1), range(map_size)):
        start_index = flag[i]
        end_index = flag[i + 1]
        currentSection = text_file[flag[i]:flag[i + 1]]

        x_position = currentSection[currentSection.index('$POS_X') + 1]
        y_position = currentSection[currentSection.index('$POS_Y') + 1]

        group_position = x_position + y_position

        group_data_index = currentSection[currentSection.index(
            '$MAPPED_VECS') + 1:currentSection.index('$MAPPED_VECS_DIST')] if '$MAPPED_VECS' in currentSection else []

        sub_map_file_name = currentSection[currentSection.index(
            '$URL_MAPPED_SOMS') + 1] if '$URL_MAPPED_SOMS' in currentSection else 'None'

        map_index_int = map_index + 1

        digit = 1
        while True:
            if (map_index_int // 10) != 0:
                digit += 1
                map_index_int = map_index_int // 10
            else:
                break

        zero = ''
        for i in range(number_of_digits[layer_index - 1] - digit):
            zero += '0'

        cluster_string = str(parent_clustered_string) + str(XDIM) + ';' + str(YDIM) + ';' + x_position + ';' + y_position + ';'
        x_y_string = str(x_y_clustered_string) + '-' + x_position + 'x' + y_position

        index = np.array(group_data_index, dtype='int64')
        current_group_source = df_source.iloc[index, :]

        current_group_statistic_info = current_group_source.describe().to_dict()

        if sub_map_file_name != 'None':
            format_cluster_info_to_dict(sub_map_file_name, source_data, saved_data_type, structure_type, unit_file_name, group_position, cluster_string, x_y_string)
            leaf_node = 0
        else:
            leaf_node = 1
            dimension_list = []
            df_source.loc[index, 'clustered_label'] = cluster_string
            df_source.loc[index, 'x_y_label'] = x_y_string
            cluster_string = cluster_string.strip(';')
            clusters_list = cluster_string.split(';')
            levels = x_y_string.split('-')
            for i in range(0, len(clusters_list), 4):
                dimension_list.append([clusters_list[i], clusters_list[i + 1], clusters_list[i + 2], clusters_list[i + 3]])
            for e in range(1, len(levels)):
                df_source.loc[index, 'clusterL' + str(e)] = levels[e]
            # 【修正-保護】加上 dimension_list 判斷，避免空list導致 IndexError
            if len(dimension_list) > 0:
                point = GHSOM_center_point(dimension_list)
                df_source.loc[index, 'point_x'] = point[0]
                df_source.loc[index, 'point_y'] = point[1]
            else:
                pass  # 【修正-保護】如果 dimension_list 為空，不做中心點處理

        if str(saved_data_type) == 'tree_structure':
            structure = {
                'name': unit_file_name + '-' + group_position,
                'parent': parent_name
            }
            if sub_map_file_name != 'None':
                sub_map_info = format_cluster_info_to_dict(sub_map_file_name, source_data, saved_data_type, structure_type, unit_file_name, group_position, cluster_string, x_y_string)
                leaf_node = 0

        elif str(saved_data_type) == 'result_detail':
            structure = {
                'name': unit_file_name,
                'group_position': group_position,
                'parent_name': parent_name,
                'sub_map_file_name': sub_map_file_name,
                'leaf_node_or_note': leaf_node,
                'statistic_info': current_group_statistic_info,
                'group_data_index': group_data_index,
                'cluster_string': cluster_string
            }

            if str(structure_type) == 'flat':
                Groups_info.append(structure)

    return Groups_info

def GHSOM_center_point(data_list):
    Bx = By = 1
    Bx_list = []
    By_list = []
    Point_list = []
    for i in range(len(data_list)):
        Bx = Bx * (Fraction(1, int(data_list[i][0])))
        Bx_list.append(Bx)
        By = By * (Fraction(1, int(data_list[i][1])))
        By_list.append(By)
        Point = [Bx * int(data_list[i][2]), By * int(data_list[i][3])]
        Point_list.append(Point)

    Px = sum([p[0] for p in Point_list]) + Bx_list[-1] * Fraction(1, 2)
    Py = sum([p[1] for p in Point_list]) + By_list[-1] * Fraction(1, 2)

    return [Px, Py]

saved_file_type = 'result_detail'
result = format_cluster_info_to_dict(prefix, df_source, saved_file_type, 'flat')

result_frame = pd.DataFrame(result)

df_source.to_csv('./applications/%s/data/%s_with_clustered_label-%s-%s.csv' % (file, prefix, t1, t2), index=False)




