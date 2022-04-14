import pandas as pd
import csv
import numpy as np
# import argparse

# parser = argparse.ArgumentParser(description='manual to this script')
# parser.add_argument('--name', type=str, default = None)
# parser.add_argument('--index', type=str, default = None)
# parser.add_argument('--train_column', type=str, default = None)
# args = parser.parse_args()

def format_ghsom_input_vector(name, file, index, subnum):
    #source_path = name.replace('-item-seq','')
    print(subnum)
    dataf = pd.read_csv('./raw-data/%s.csv' % name, encoding='utf-8')
    #label_df = pd.read_csv('./raw-data/label/%s_label.csv' % name, encoding='utf-8')

    df = pd.DataFrame(dataf)
    #if train_column
    df = dataf.fillna(0)
    #df['type'] = label_df['type']
    #sub samples
    if subnum != None:
        df = df.sample(n=subnum)


    #lb = label_df[(label_df['ID'] == df['ID'])]
    #all as train_column
    #lb = df['type']
    df = df.drop(index,axis=1)

    # data shape
    print('rows=',df.shape[0])
    print('columns=',df.shape[1])

    #save labels
    rows_amount = df.shape[0]
    columns_amount = df.shape[1]
    df[index] = range(0,rows_amount)
    
    #if subsample
    #lb.to_csv('./applications/%s/data/%s_label.csv' % (name,name),index=False) #subsam#df = df.drop(columns=['type'])
    #df.to_csv('./applications/%s/data/%s_raw.csv' % (name,name),index=False) 
    df.to_csv('./applications/%s/GHSOM/data/%s_ghsom.csv' % (file, name), sep=' ',index=False, header=False)

    # set ghsom input data format
    # format information : http://www.ifs.tuwien.ac.at/~andi/somlib/download/SOMLib_Datafiles.html#input_vectors
    data_type = 'inputvec'
    x_dim = rows_amount
    y_dim = 1
    vec_dim = columns_amount

    with open('./applications/%s/GHSOM/data/%s_ghsom.in' % (file, name), 'w', newline='',encoding='utf-8') as csvfile:
        # 建立 CSV 檔寫入器 , 設定空白切割
        writer = csv.writer(csvfile)

        # Parameter settings
        writer.writerow(['$TYPE %s' % data_type])
        writer.writerow(['$XDIM %s' % x_dim])
        writer.writerow(['$YDIM %s' % y_dim])
        writer.writerow(['$VECDIM %s' % vec_dim])
        
        # Data settings
        with open('./applications/%s/GHSOM/data/%s_ghsom.csv' % (file, name),'r', newline='',encoding='utf-8') as rawfile:
            # 讀取 CSV 檔案內容
            rows = csv.reader(rawfile)
            writer.writerow([])
        
            # 以迴圈輸出每一列
            for row in rows:
                #print(row)
                writer.writerow(row)
        rawfile.close()