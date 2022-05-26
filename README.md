# GHSOM
目前用VS Code 的wsl終端機執行～

### Prerequisites
需要安裝JRE(java runtime environment)、Python3.6以上

### Operation description
input data須為csv檔

columnss為training attributes(全部)

rows為欲分群Data

開始分群前請先將index column命名（command須代入index名稱）


*raw data請創資料夾名為"raw-data" (與application同層)並放置於此

資料label請放於raw-data/label資料夾 (一樣須為csv檔，並命名label column為"type")


### Command
於terminal輸入以下command並代入自己的參數
```
python execute.py --index=$index --data=$file_name --tau1=$tau1 --tau2=$tau2
```
*data, index一定要給(所以要先命名index column，不為空)

*若沒有給tau1,2，tau1預設0.1、 tau2預設0.01

### File description
raw-data(folder)：放要分群的資料

raw-data/label(folder)：放要分群的資料label（檔名前面部分要一樣，加上_label）

execute.py：全部步驟執行

format_ghsom_input_vector.py：產生GHSOM能吃的資料類型

get_ghsom_dim.py：取得分群結果dimension

save_cluster_with_clustered_label：產生有clustering結果(Leaf及各Layer)dataframe，並存於data

evaluation/clustering_scores：計算External, Internal evaluation分數



