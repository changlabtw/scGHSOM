import os
import sys
import argparse
import csv 
from programs.data_processing.format_ghsom_input_vector import format_ghsom_input_vector
from programs.data_processing.get_disease_column import extract_disease_input_vector

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--tau1', type=float, default = 0.1)
parser.add_argument('--tau2', type=float, default=0.01)
parser.add_argument('--data', type=str, default=None)
parser.add_argument('--train_column', type=str, default = None)
parser.add_argument('--index', type=str, default=None)
parser.add_argument('--disease',type=str, default=None)


args = parser.parse_args()
#disease_name = args.data + '_' + args.disease
print('tau1 = %s, tau2 = %s' % (args.tau1, args.tau2))
print('data = %s, index = %s' % (args.data,args.index))
current_path = os.getcwd()
print('Current:',current_path)
##############################
# GHSOM Settings
##############################
# create ghsom input vector file 
#Ref: http://www.ifs.tuwien.ac.at/~andi/somlib/download/SOMLib_Datafiles.html#input_vectors
def save_ghsom_cluster_label(name,tau1,tau2,index):
    os.system('python ./programs/data_processing/save_cluster_with_clustered_label.py --name=%s --tau1=%s --tau2=%s --index=%s' % (name,tau1,tau2,index))
    print('Success transfer cluster label of item sequence data.')




def clustering_evaluation(name,tau1=0.1,tau2=0.01):
    #os.system('python ./programs/data_processing/map_cluster_center_ponit.py --name=%s' % (name))
    os.system('python ./programs/evaluation/clustering_scores.py --name=%s --tau1=%s --tau2=%s' % (name,tau1,tau2))
    print('Success evaluating.')    

save_ghsom_cluster_label(args.data, args.tau1, args.tau2, args.index)
clustering_evaluation(args.data, args.tau1, args.tau2)
