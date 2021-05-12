import pandas as pd
import csv
import numpy as np

def extract_disease_input_vector(disease):
    disease_file = pd.read_csv('./raw-data/shiny_disease.csv', encoding='utf-8')
    disease_true = disease_file['primary_disease'] == disease

    train_column = disease_file[disease_true]['ID']
    return train_column