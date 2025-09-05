import os
import argparse
import pandas as pd
import plotly.express as px
from fractions import Fraction
from collections import Counter

def GHSOM_center_point(dimension_df):
    Bx = By = Fraction(1, 1)
    Bx_list, By_list, Point_list = [], [], []

    for i in range(dimension_df.shape[0]):
        Bx *= Fraction(1, dimension_df.loc[i, 'XDIM'])
        By *= Fraction(1, dimension_df.loc[i, 'YDIM'])
        Bx_list.append(Bx)
        By_list.append(By)

        pos_x = Bx * dimension_df.loc[i, 'X']
        pos_y = By * dimension_df.loc[i, 'Y']
        Point_list.append([pos_x, pos_y])

    Px = sum(p[0] for p in Point_list) + Bx_list[-1] * Fraction(1, 2)
    Py = sum(p[1] for p in Point_list) + By_list[-1] * Fraction(1, 2)
    return [float(Px), float(Py)]

def parse_cluster_string(cluster_string):
    parts = cluster_string.strip().split(';')
    dimension_list = []
    for i in range(0, len(parts), 4):
        try:
            xdim = int(parts[i])
            ydim = int(parts[i+1])
            x = int(parts[i+2])
            y = int(parts[i+3])
            dimension_list.append([xdim, ydim, x, y])
        except:
            continue
    return dimension_list

def safe_convert(val):
    try:
        return float(Fraction(val))
    except:
        return None

def cluster_distribution_map(name, tau1, tau2):
    file_prefix = f"{name}-{tau1}-{tau2}"
    csv_path = f"./applications/{file_prefix}/data/{name}_with_clustered_label-{tau1}-{tau2}.csv"
    label_path = f"./raw-data/label/{name}_label.csv"
    output_path = f"./applications/{file_prefix}/graphs/CDM_{name}_{tau1}_{tau2}.html"

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"❌ 找不到輸入檔案：{csv_path}")
    df = pd.read_csv(csv_path)

    # 若無座標，重新從 clustered_label 計算
    if 'point_x' not in df.columns or 'point_y' not in df.columns:
        print("🔄 正在從 clustered_label 計算投影座標 (Eq.7 & 8)...")
        point_x, point_y = [], []
        for label in df['clustered_label']:
            dim_list = parse_cluster_string(label)
            if dim_list:
                dim_df = pd.DataFrame(dim_list, columns=['XDIM', 'YDIM', 'X', 'Y'])
                px_val, py_val = GHSOM_center_point(dim_df)
            else:
                px_val, py_val = None, None
            point_x.append(px_val)
            point_y.append(py_val)
        df['point_x'] = point_x
        df['point_y'] = point_y
        df.to_csv(csv_path, index=False)
        print(f"✅ 已寫入新座標至 {csv_path}")

    # 將 Fraction 格式轉換為 float
    df['point_x'] = df['point_x'].apply(safe_convert)
    df['point_y'] = df['point_y'].apply(safe_convert)
    df = df.dropna(subset=['point_x', 'point_y'])

    # 合併 label（若存在）
    if os.path.exists(label_path):
        label_df = pd.read_csv(label_path)
        df['label'] = label_df['label']
    else:
        df['label'] = df['clustered_label']

    df = df.dropna(subset=['label'])

    # 聚合：以座標 groupby，統計 count 與最多 label（多數決）
    df['coord'] = list(zip(df['point_x'], df['point_y']))
    grouped = df.groupby('coord')

    cluster_rows = []
    for coord, g in grouped:
        x, y = coord
        label_list = g['label'].tolist()
        count = len(label_list)
        most_common_label = Counter(label_list).most_common(1)[0][0]
        cluster_rows.append({
            'point_x': x,
            'point_y': y,
            'label': most_common_label,
            'count': count
        })

    cluster_df = pd.DataFrame(cluster_rows)
    cluster_df['label'] = cluster_df['label'].astype(str)  # ✅ 類別型顏色處理

    # 畫圖
    fig = px.scatter(
        cluster_df,
        x='point_x',
        y='point_y',
        size='count',
        color='label',  # 顏色以類別分
        hover_data={
            'point_x': ':.3f',
            'point_y': ':.3f',
            'label': True,
            'count': True
        },
        title=f'Cluster Distribution Map (τ₁={tau1}, τ₂={tau2})',
    )

    fig.update_layout(height=700, width=900)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_html(output_path)
    print(f"📍 已輸出互動圖至：{output_path}")
    fig.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot Cluster Distribution Map for scGHSOM')
    parser.add_argument('--data', type=str, required=True)
    parser.add_argument('--tau1', type=float, required=True)
    parser.add_argument('--tau2', type=float, required=True)
    args = parser.parse_args()

    cluster_distribution_map(args.data, args.tau1, args.tau2)
