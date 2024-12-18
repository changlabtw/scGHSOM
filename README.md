# scGHSOM
scGHSOM: A Hierarchical Framework for Single-Cell Data Clustering and Visualization

### Prerequisites
Currently running using the WSL terminal in VS Code.
- Requires **JRE (Java Runtime Environment)**  
- Python version **3.6 or higher**


### Operation Description

- **Input data** must be in **CSV format**.
- **Columns**: Represent training attributes (all columns).  
- **Rows**: Represent data to be clustered.  
- Before starting clustering, **name the index column** (the index name must be passed in the command).

#### File Structure:

- Create a folder named **`raw-data`** (at the same level as the application) and place raw data files in it.
- Place labels in the **`raw-data/label`** folder.  
  - Labels must also be in **CSV format** and the label column should be named **`type`**.


### Command

Run the following command in the terminal, replacing placeholders with your parameters:

```
python3 execute.py --index=$index --data=$file_name --tau1=$tau1 --tau2=$tau2
```

#### Notes:
- **`data`** and **`index`** are mandatory parameters (ensure the index column is named and not empty).  
- If **`tau1`** and **`tau2`** are not provided:  
  - **`tau1`** defaults to **0.1**  
  - **`tau2`** defaults to **0.01**


### File Description

- **`raw-data` (folder)**: Stores data to be clustered.  
- **`raw-data/label` (folder)**: Stores labels for clustering data.  
  - File names should have the same prefix as the data file, with `_label` appended.

#### Scripts:

- **`execute.py`**: Runs all the process steps.  
- **`format_ghsom_input_vector.py`**: Generates data in a format compatible with GHSOM.  
- **`get_ghsom_dim.py`**: Retrieves the dimensions of the clustering results.  
- **`save_cluster_with_clustered_label.py`**: Produces a data frame with clustering results (Leaf and each Layer) and saves it to the `data` folder.  

#### Evaluation:

- **`evaluation/clustering_scores`**: Calculates **external** and **internal** evaluation scores.  

### Reference

* Shang-Jung Wen*, Jia-Ming Chang*, Fang Yu [scGHSOM: A Hierarchical Framework for Single-Cell Data Clustering and Visualization.](https://doi.org/10.48550/arXiv.2407.16984) arXiv:2407.16984 (2024). *joint-first author
