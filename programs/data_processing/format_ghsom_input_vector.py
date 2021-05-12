import pandas as pd
import csv
import numpy as np
# import argparse

# parser = argparse.ArgumentParser(description='manual to this script')
# parser.add_argument('--name', type=str, default = None)
# parser.add_argument('--index', type=str, default = None)
# parser.add_argument('--train_column', type=str, default = None)
# args = parser.parse_args()

def format_ghsom_input_vector(name, index):
    #source_path = name.replace('-item-seq','')
    dataf = pd.read_csv('./raw-data/%s.csv' % name, encoding='utf-8')
    
    #if train_column
    #dataf = dataf.fillna(0)
    df = dataf.fillna(0)
    df = pd.DataFrame(df)

    #all as train_column
    df = df.drop(index,axis=1)

    # data shape
    print('rows=',df.shape[0])
    print('columns=',df.shape[1])

    rows_amount = df.shape[0]
    columns_amount = df.shape[1]
    df[index] = range(0,rows_amount)
    print('./applications/%s/GHSOM/data/%s_ghsom.csv' % (name,name))
    df.to_csv('./applications/%s/GHSOM/data/%s_ghsom.csv' % (name,name),sep=' ',header=False,index=False)

    # set ghsom input data format
    # format information : http://www.ifs.tuwien.ac.at/~andi/somlib/download/SOMLib_Datafiles.html#input_vectors
    data_type = 'inputvec'
    x_dim = rows_amount
    y_dim = 1
    vec_dim = columns_amount

    with open('./applications/%s/GHSOM/data/%s_ghsom.in' % (name,name), 'w', newline='',encoding='utf-8') as csvfile:
        # 建立 CSV 檔寫入器 , 設定空白切割
        writer = csv.writer(csvfile)

        # Parameter settings
        writer.writerow(['$TYPE %s' % data_type])
        writer.writerow(['$XDIM %s' % x_dim])
        writer.writerow(['$YDIM %s' % y_dim])
        writer.writerow(['$VECDIM %s' % vec_dim])
        
        # Data settings
        with open('./applications/%s/GHSOM/data/%s_ghsom.csv' % (name,name),'r', newline='',encoding='utf-8') as rawfile:
            # 讀取 CSV 檔案內容
            rows = csv.reader(rawfile)
            writer.writerow([])
        
            # 以迴圈輸出每一列
            for row in rows:
                #print(row)
                writer.writerow(row)
        rawfile.close()